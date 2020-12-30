import time
import math
import random

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

from . import DataPreprocessor
from . import EncoderRNN, AttnDecoderRNN
from .params import *

SOS_token = 0
EOS_token = 1
MAX_LENGTH = 50

class TrainingSettings():
    # device: "cpu" / "cuda"
    def __init__(self, data_path="data/", load_model=False, device="cpu", lang1="eng", lang2="fin", max_length=50, epochs=5000, save_every=5000):
        # User settings
        self.data_path = data_path    # where weights are saved, where data is read from ?
        self.load_model = load_model  # continue training ?
        self.device = torch.device(device) # cpu / cuda
        self.epochs = epochs          # how many epochs shall run
        self.save_every = save_every  # how often weights are saved
        self.plot_every = self.save_every

        # Language settings
        self.lang1 = lang1 #input language
        self.lang2 = lang2 # output language
        self.max_length = max_length # maximum length for sentences

        # Tune parameters
        self.teacher_forcing_ratio = 0.5
        self.learning_rate = 0.01

def indexesFromSentence(lang, sentence):
    """
    Assigns indices for each word in given sentence. This allows computers to handle text data.
    In case of unknown word, -1 is appended to the index list. Otherwise values are positive.
    Input: lang (Lang): Language class
           sentence (str): sentence that shall be transformed to more mathematical form.
    Return List of indices and a separate index telling position of unknown word.
    """
    indexes = []
    unknown_idx = -1
    for i, word in enumerate(sentence.split(' '), start=0):
        try:
            idx = lang.word2index[word]
            indexes.append(idx)
        except KeyError:
            print(f"Unknown word: {word}, idx: {i}")
            unknown_idx = i
            indexes.append(-1)
    return indexes, unknown_idx

def tensorFromSentence(lang, sentence, device):
    """
    Input lang (Lang)
        sentence (str)
        device (torch.device ?)
    Return Sentence tensor and index of last unkown word.
    """
    indexes, unknown_idx = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1), unknown_idx

def tensorsFromPair(pair, input_lang, output_lang, device):
    input_tensor, _ = tensorFromSentence(input_lang, pair[0], device)
    target_tensor, _ = tensorFromSentence(output_lang, pair[1], device)
    return (input_tensor, target_tensor)

# @param cfg (TrainingSettings): configuration used for training 
def runTraining(cfg):
    data_processor = DataPreprocessor(data_path=cfg.data_path)
    train_data = data_processor.prepareData(cfg.lang1, cfg.lang2, cfg.max_length)
    print("Random line:", random.choice(train_data.pairs)) # to show if data is ok

    hidden_size = 256
    encoder1 = EncoderRNN(train_data.input_lang.n_words, hidden_size, cfg.device).to(cfg.device)
    attn_decoder1 = AttnDecoderRNN(hidden_size, train_data.output_lang.n_words, cfg.max_length, cfg.device, dropout_p=0.1).to(cfg.device)

    if cfg.load_model:
        print("Loading weights from:", cfg.data_path)
        encoder1.load_state_dict(torch.load(cfg.data_path + "encoder.pt"))
        attn_decoder1.load_state_dict(torch.load(cfg.data_path + "decoder.pt"))

    trainIters(train_data, encoder1, attn_decoder1, cfg)

    evaluateRandomly(train_data, encoder1, attn_decoder1, device=cfg.device)

def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, teacher_forcing_ratio, device, max_length=MAX_LENGTH):
    encoder_hidden = encoder.initHidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)
    target_length = target_tensor.size(0)

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

    loss = 0

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]

    decoder_input = torch.tensor([[SOS_token]], device=device)

    decoder_hidden = encoder_hidden

    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False

    if use_teacher_forcing:
        # Teacher forcing: Feed the target as the next input
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            loss += criterion(decoder_output, target_tensor[di])
            decoder_input = target_tensor[di]  # Teacher forcing

    else:
        # Without teacher forcing: use its own predictions as the next input
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            topv, topi = decoder_output.topk(1)
            decoder_input = topi.squeeze().detach()  # detach from history as input

            loss += criterion(decoder_output, target_tensor[di])
            if decoder_input.item() == EOS_token:
                break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_length

def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))

def trainIters(train_data, encoder, decoder, cfg):
    start = time.time()
    n_iters = cfg.epochs
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = optim.SGD(encoder.parameters(), lr=cfg.learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=cfg.learning_rate)
    training_pairs = [tensorsFromPair(random.choice(train_data.pairs), train_data.input_lang, train_data.output_lang, cfg.device)
                      for i in range(n_iters)]
    criterion = nn.NLLLoss()

    for iter in range(1, n_iters + 1):
        training_pair = training_pairs[iter - 1]
        input_tensor = training_pair[0]
        target_tensor = training_pair[1]

        loss = train(input_tensor, target_tensor, encoder,
                     decoder, encoder_optimizer, decoder_optimizer, criterion, cfg.teacher_forcing_ratio, cfg.device)
        print_loss_total += loss
        plot_loss_total += loss

        if iter % cfg.save_every == 0:
            print_loss_avg = print_loss_total / cfg.save_every
            print_loss_total = 0
            print('%s (%d %d%%) %.4f' % (timeSince(start, iter / n_iters),
                                         iter, iter / n_iters * 100, print_loss_avg))
            torch.save(encoder.state_dict(), cfg.data_path + "encoder.pt")
            torch.save(decoder.state_dict(), cfg.data_path + "decoder.pt")

        if iter % cfg.plot_every == 0:
            plot_loss_avg = plot_loss_total / cfg.plot_every
            plot_losses.append(plot_loss_avg)
            plot_loss_total = 0

def evaluate(encoder, decoder, sentence, input_lang, output_lang, device, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor, unknown_idx = tensorFromSentence(input_lang, sentence, device)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()
        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            if input_tensor[ei] > -1: # Feed only known word indices to encoder, otherwise crashes
                encoder_output, encoder_hidden = encoder(input_tensor[ei], encoder_hidden)
                encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS
        decoder_hidden = encoder_hidden
        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        return decoded_words, decoder_attentions[:di + 1], unknown_idx

# Lang class, attrs: pairs, input_lang, output_lang
def evaluateRandomly(train_data, encoder, decoder, device, n=10):
    for i in range(n):
        pair = random.choice(train_data.pairs)
        print("pair:", pair)
        print('>', pair[0])
        print('=', pair[1])
        output_words, attentions, unknown_idx = evaluate(encoder, decoder, pair[0], train_data.input_lang, train_data.output_lang, device)
        output_sentence = ' '.join(output_words)
        print('<', output_sentence)
        print("attentions:", attentions)
        print('')
