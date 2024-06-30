import os
import pickle
from collections import Counter, defaultdict
import re

def pre_tokenize(sentence):
    """ Tokenize a sentence into word-like and punctuation units. """
    return re.findall(r'\w+|[^\w\s]', sentence, re.UNICODE)

def compute_frequencies(file_path):
    """ Compute frequency of each word in the file. """
    word_freq = Counter()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word_freq.update(pre_tokenize(line.strip()))
    return word_freq

def create_splits(words):
    """ Split words into characters. """
    return {word: list(word) for word in words}

def compute_pair_freq(splits, word_freq):
    """ Compute frequency of adjacent character pairs in word splits. """
    pair_freq = defaultdict(int)
    for word, freq in word_freq.items():
        symbols = splits[word]
        for i in range(len(symbols) - 1):
            pair_freq[(symbols[i], symbols[i+1])] += freq
    return pair_freq

def merge_pairs(splits, best_pair):
    """ Merge best pair in all splits. """
    a, b = best_pair
    new_token = a + b
    new_splits = {}
    for word, split in splits.items():
        new_split = []
        i = 0
        while i < len(split):
            if i < len(split) - 1 and split[i] == a and split[i+1] == b:
                new_split.append(new_token)
                i += 2
            else:
                new_split.append(split[i])
                i += 1
        new_splits[word] = new_split
    return new_splits

def train_byte_pair_tokenizer(file_path, vocab_size):
    """ Train a BytePairTokenizer to a specific vocabulary size. """
    word_freq = compute_frequencies(file_path)
    splits = create_splits(word_freq)
    vocab = set(char for word in word_freq for char in word)
    
    while len(vocab) < vocab_size:
        pair_freq = compute_pair_freq(splits, word_freq)
        best_pair = max(pair_freq, key=pair_freq.get)
        vocab.add(best_pair[0] + best_pair[1])
        splits = merge_pairs(splits, best_pair)
    
    return list(vocab)

def add_numerical_and_special_tokens(vocab, max_exponent):
    """ Add numerical tokens and special tokens to the vocabulary. """
    digits = list(range(10))
    numerical_tokens = [f"_{digit}_{exponent}_" for exponent in range(max_exponent + 1) for digit in digits] + \
                       [f"_{digit}_-{exponent}_" for exponent in range(max_exponent + 1) for digit in digits]

    special_tokens = ["[PAD]", "[unused1]", "[unused2]", "[unused3]", "[unused4]", "[unused5]",
                      "[unused6]", "[unused7]", "[unused8]", "[unused9]", "[unused10]",
                      "[UNK]", "[CLS]", "[SEP]", "[MASK]"]

    return vocab + numerical_tokens + special_tokens

def create_vocabulary(input_file_path, output_file_path, vocab_size=2000, max_exponent=12):
    """ Create a vocabulary with BytePairTokenizer and save it. """
    vocab = train_byte_pair_tokenizer(input_file_path, vocab_size)
    vocab = [token for token in vocab if not token.isdigit()] 

    vocab = add_numerical_and_special_tokens(vocab, max_exponent)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(vocab))

if __name__ == "__main__":
    create_vocabulary('impact_project/corpus.txt', 'impact_project/vocabulary.txt')
