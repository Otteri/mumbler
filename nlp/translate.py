import sys
import torch
import sys, select # 30s timeout

from . import DataPreprocessor
from . import EncoderRNN, AttnDecoderRNN
from . import evaluate

device = torch.device("cpu") # for translations, cpu is enough

def teachSentence(input_sentence, data_path="data/"):
    info_text = ("< I have not heard that sentence or word before.\n"
                 "< You can help me to understand it by typing a translation within 30s using the (>) prefix.")
    print(info_text)

    i, o, e = select.select( [sys.stdin], [], [], 30 )

    if (i):
        translation = sys.stdin.readline().strip()
        if translation[0] == '/teach':
            data_processor = DataPreprocessor(data_path=data_path)
            data_processor.writeNewSentencePair(input_sentence, translation, verbose=True)

# Data path allows to group certain data + weights, which allows use of multiple different networks.
def translate(input_sentence, max_length=50, data_path="data/", verbose=False):
    output_sentence = ""
    data_processor = DataPreprocessor(data_path=data_path, verbose=verbose)
    train_data = data_processor.prepareData('eng', 'fin', max_length)

    # Load models
    hidden_size = 256
    encoder1 = EncoderRNN(train_data.input_lang.n_words, hidden_size, device).to(device)
    attn_decoder1 = AttnDecoderRNN(hidden_size, train_data.output_lang.n_words, max_length, device, dropout_p=0.1).to(device)
    
    try:
        encoder1.load_state_dict(torch.load(data_path + "encoder.pt"))
        attn_decoder1.load_state_dict(torch.load(data_path + "decoder.pt"))
    except RuntimeError:
        error_text = ("Make sure you are not trying to mix weights with different vocabulary.\n"
                      "Did you provide correct data path? Has vocabulary size changed and model requires retraining?")
        print(error_text)
        return 1

    output_words, _, unknown_idx = evaluate(encoder1, attn_decoder1, input_sentence, train_data.input_lang, train_data.output_lang, device)
    output_sentence = ' '.join(output_words)
    return output_sentence, unknown_idx

