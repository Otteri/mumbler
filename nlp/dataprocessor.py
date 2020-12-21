import unicodedata
import re
import glob

from .params import *

class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

# Class for storing processed training data and its settings
class TrainingData:
    def __init__(self, in_lang, out_lang, pairs, max_length=50):
        self.input_lang = in_lang
        self.output_lang = out_lang
        self.pairs = pairs # Processed training data
        self.max_length = max_length

# Preprocesses data
class DataPreprocessor:
    def __init__(self, data_path="data/", verbose=False):
        self.data_path = data_path
        self.verbose = verbose

    # Turn a Unicode string to plain ASCII, thanks to
    # https://stackoverflow.com/a/518232/2809427
    def _unicodeToAscii(self, s):
        return ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )

    # Lowercase, trim, and remove non-letter characters
    def _normalizeString(self, s):
        s = self._unicodeToAscii(s.lower().strip())
        s = re.sub(r"([.!?])", r" \1", s)
        s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
        return s

    def _filterPair(self, p, max_length):
        return len(p[0].split(' ')) < max_length and \
            len(p[1].split(' ')) < max_length

    def _filterPairs(self, pairs, max_length):
        return [pair for pair in pairs if self._filterPair(pair, max_length)]

    # Reads pairs from datafile
    def _readData(self, data_files):
        lines = []
        for file in data_files:
            if self.verbose:
                print("Reading data from: ", file)
            lines += open(file, encoding='utf-8').read().strip().split('\n')
        # Split every line into pairs and normalize
        pairs = [[self._normalizeString(s) for s in l.split('\t')] for l in lines]
        return pairs

    # Lists all files with given extension in the directory
    def _listFiles(self, directory, extension):
        return glob.glob(f"{directory}/*{extension}", recursive=True)

    def prepareData(self, lang1, lang2, max_length):
        self.input_lang = Lang(lang1)
        self.output_lang = Lang(lang2)
        
        # Get all text files from the directory
        data_files = self._listFiles(self.data_path, ".txt")

        read_pairs = self._readData(data_files)
        pairs = self._filterPairs(read_pairs, max_length)
        for pair in pairs:
            #print("pair: ", pair[0], " - ", pair[1])
            self.input_lang.addSentence(pair[0])
            self.output_lang.addSentence(pair[1])
        if self.verbose:
            print("Read {} sentence pairs. Trimmed to {} pairs.".format(len(read_pairs), len(pairs)))
            print("{}: {} words and {}: {} words".format(lang1, self.input_lang.n_words, lang2, self.output_lang.n_words))
        self.pairs = pairs

        # Put to a class struct and share it
        train_data = TrainingData(self.input_lang, self.output_lang, pairs)
        return train_data

    # Writes sentence and its translation to 'teached.txt' file.
    # This file can be then used for training.
    def writeNewSentencePair(self, sentence1, sentence2, verbose=False):
        file_path = self.data_path + "teached"
        print("file path:", file_path)
        with open(file_path, "a", encoding='utf-8') as file:
            s1 = self._normalizeString(sentence1)
            s2 = self._normalizeString(sentence2)
            if len(s1) > 2 and len(s2) > 2: # sentance must be at least two chars
                string = "{}.\t{}.\n".format(s1, s2)
                file.write(string)
                if verbose:
                    print("< Added: ", string)
        return True
