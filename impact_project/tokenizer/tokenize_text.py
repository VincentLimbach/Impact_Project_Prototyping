import re
from impact_project.datasets.utils import extensive_split

def load_vocabulary(vocab_path):
    """ Load vocabulary from a file and create a token to index mapping. """
    with open(vocab_path, 'r', encoding='utf-8') as file:
        vocab = file.read().splitlines()
    vocab_to_index = {token: idx for idx, token in enumerate(vocab)}
    return vocab_to_index

def number_to_tokens(number, vocab_to_index):
    """ Convert numeric strings, including scientific notation, to tokens based on position. """
    tokens = []

    if number[0] == '-':
        tokens.append('-')
        number = number[1:]

    parts = re.split(r'([eE][-+]?\d+)', number)
    for part in parts:
        if part.startswith(('e', 'E')):
            exponent = part[1:]
            tokens.append('_e_')
            for index, char in enumerate(exponent):
                if char in '+-':
                    tokens.append(f"_{char}_")
                else:
                    sign = '-' if exponent[0] == '-' else ''
                    token = f"_{char}_{sign}{index}_"
                    if token in vocab_to_index:
                        tokens.append(token)
                    else:
                        tokens.append('[UNK]')
        else:
            if '.' in part:
                integer_part, decimal_part = part.split('.')
            else:
                integer_part, decimal_part = part, ''
            
            for index, char in enumerate(integer_part):
                token = f"_{char}_{len(integer_part)-index-1}_"
                if token in vocab_to_index:
                    tokens.append(token)
                else:
                    tokens.append('[UNK]')
            
            for index, char in enumerate(decimal_part):
                token = f"_{char}_-{index + 1}_"
                if token in vocab_to_index:
                    tokens.append(token)
                else:
                    tokens.append('[UNK]')

    return tokens

def longest_match_tokenize(word, vocab_to_index, number_regex):
    """ Tokenize a word by finding the longest prefixes in the vocabulary, handling numbers appropriately. """
    tokens = []
    i = 0
    while i < len(word):
        max_len = 0
        number_match = ''
        for j in range(i + 1, len(word) + 1):
            candidate = word[i:j]
            if number_regex.match(candidate):
                if len(candidate) > max_len:
                    max_len = len(candidate)
                    number_match = candidate

        if number_match:
            tokens.extend(number_to_tokens(number_match, vocab_to_index))
            i += len(number_match)
        else:
            match = None
            for j in range(len(word), i, -1):
                possible_match = word[i:j]
                if possible_match in vocab_to_index:
                    match = possible_match
                    break
            if match:
                tokens.append(match)
                i += len(match)
            else:
                tokens.append('[UNK]')
                i += 1
    return tokens

def tokenize_text(strings, vocab_path):
    vocab_to_index = load_vocabulary(vocab_path)
    tokenized_texts = []

    number_regex = re.compile(r'^-?\d*\.?\d+([eE][-+]?\d+)?$')

    for text in strings:
        tokens = []
        for word in extensive_split(text):
            if number_regex.match(word):
                tokens.extend(number_to_tokens(word, vocab_to_index))
            else:
                tokens.extend(longest_match_tokenize(word, vocab_to_index, number_regex))
        tokenized_texts.append(tokens)

    return tokenized_texts

