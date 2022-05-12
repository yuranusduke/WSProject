# -*- coding: utf-8 -*-
"""
This file contains operations about data preprocessing to map them into
word embeddings(GLOVE).
In particular, we tend to implement this procedure first with
preprocessing and them using GLOVE word vectors to map them, finally, we use PCA to
do dimension reduction and visualize them to see if we have correctly scraped them
ref: https://nlp.stanford.edu/projects/glove/

Created by Kunhong Yu(444447)
Date: 2022/04/27
"""

import pandas as pd
import numpy as np
import re
import sys
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

#############################################
puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£',
 '·', '_', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',  '♥', '←', '×', '§', '″', '′', ' ', '█', '½', 'à', '…',
 '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─',
 '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾', 'Ã', '⋅', '‘', '∞',
 '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√', ]

contraction_dict = {"ain't": "is not", "aren't": "are not","can't": "cannot",
                    "'cause": "because", "could've": "could have",
                    "couldn't": "could not", "didn't": "did not",
                    "doesn't": "does not", "don't": "do not", "hadn't": "had not",
                    "hasn't": "has not", "haven't": "have not", "he'd": "he would",
                    "he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you",
                    "how'll": "how will", "how's": "how is",  "I'd": "I would", "I'd've": "I would have",
                    "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have",
                    "i'd": "i would", "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have",
                    "i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would",
                    "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have",
                    "it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not",
                    "might've": "might have","mightn't": "might not","mightn't've": "might not have",
                    "must've": "must have", "mustn't": "must not", "mustn't've": "must not have",
                    "needn't": "need not", "needn't've": "need not have", "o'clock": "of the clock",
                    "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not",
                    "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would",
                    "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have",
                    "she's": "she is", "should've": "should have", "shouldn't": "should not",
                    "shouldn't've": "should not have", "so've": "so have","so's": "so as",
                    "this's": "this is","that'd": "that would", "that'd've": "that would have",
                    "that's": "that is", "there'd": "there would", "there'd've": "there would have",
                    "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have",
                    "they'll": "they will", "they'll've": "they will have", "they're": "they are",
                    "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we would",
                    "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are",
                    "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have",
                    "what're": "what are",  "what's": "what is", "what've": "what have",
                    "when's": "when is", "when've": "when have", "where'd": "where did",
                    "where's": "where is", "where've": "where have", "who'll": "who will",
                    "who'll've": "who will have", "who's": "who is", "who've": "who have",
                    "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not",
                    "won't've": "will not have", "would've": "would have", "wouldn't": "would not",
                    "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would",
                    "y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
                    "you'd": "you would", "you'd've": "you would have", "you'll": "you will",
                    "you'll've": "you will have", "you're": "you are", "you've": "you have"}
#############################################

# 1. First, get rid of punctuation characters
def clean_text(x : str) -> str:
    """This function is used to clean text to get rid of punctuation characters
    Args :
        --x: one sentence
    return :
        --x: cleaned sentence
    """
    x = str(x)
    for punct in puncts:
        if punct in x:
            x = x.replace(punct, '')

    return x

# 2. clean numbers and replace them into #s
def clean_numbers(x : str) -> str:
    """This function is used to clean numbers
    Args :
        --x: input sentence
    return :
        --x: preprocessed sentence
    """
    if bool(re.search(r'\d', x)):
        x = re.sub('[0-9]{5,}', '#####', x)
        x = re.sub('[0-9]{4}', '####', x)
        x = re.sub('[0-9]{3}', '###', x)
        x = re.sub('[0-9]{2}', '##', x)

    return x

# 3. Removing contractions
def _get_contractions(contraction_dict : dict):
    """Get contractions
    Args :
        --contraction_dict
    return :
        --contraction_dict, contraction_re
    """
    contraction_re = re.compile('(%s)' % '|'.join(contraction_dict.keys()))
    return contraction_dict, contraction_re

def replace_contractions(x : str):
    contractions, contractions_re = _get_contractions(contraction_dict)
    def replace(match):
        return contractions[match.group(0)]

    return contractions_re.sub(replace, x)

# 4. Tokenizer
def tokenize(data : list, max_features : int) -> list:
    """This function is used to tokenize input data
    Args :
        --data: input data with Python list, each one is just one string
        --max_features: number of max features
    return :
        --data: preprocessed data
    """
    tokenizer = Tokenizer(num_words = max_features)
    tokenizer.fit_on_texts(data)
    data = tokenizer.texts_to_sequences(data)
    data = pad_sequences(data)

    return data


# 5. Load GLOVE
def load_glove_index(path = './processing/glove.6B.50d.txt') -> dict:
    """This function is used to load Glove word embedding
    return :
        --path: default is './processing/glove.6B.50d.txt'
    """
    EMBEDDING_FILE = path
    def get_coefs(word,*arr):
        return word, np.asarray(arr, dtype = 'float32')[:300]
    embeddings_index = dict(get_coefs(*o.split(" ")) for o in open(EMBEDDING_FILE))

    return embeddings_index

# 6. Get embedding matrix
def create_glove(word_index : dict, embeddings_index : dict) -> (np.ndarray, int):
    """This function is used to create GLOVE embedding matrix
    Args :
        --word_index
        --embedding_index
    return :
        --embedding_matrix
        --num_lines
    """
    # Prepare embedding matrix
    num_lines = 0
    embedding_matrix = np.zeros((max(list(word_index.values())) + 1, 50))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # Words not found in embedding index will be all-zeros.
            # This includes the representation for "padding" and "OOV"
            embedding_matrix[i] = embedding_vector
            num_lines += 1

    return embedding_matrix, num_lines

# 7. Combine them together
def preprocess(data, path = './processing/glove.6B.50d.txt'):
    """This function is used to simply preprocess csv data
    # here is logic, we first find title and abstract and map each one into embedding
    # matrix, and, we calculate mean of them, then for all papers, we
    # parse all papers' information
    Args :
        --data: data is stored in csv
        --path: default is './processing/glove.6B.50d.txt'
    return :
        --papers: all papers' embeddings in numpy arrary
    """
    # 1. clean x
    papers = []
    count = 0
    print("\033[0;36;40mStarting preprocessing papers to map GLOVE embeddings...\033[0m")
    print('Loading glove embedding...')
    emb_index = load_glove_index(path = path)
    for _, line in data.iterrows():
        # combine title and abstract together
        count += 1
        title = line['title']
        sys.stdout.write('\r>>Preprocessing %d / %d paper : %s.' % (count, data.shape[0], title))
        sys.stdout.flush()

        abstract = line['abstract']
        line = title + ' ' + abstract
        line = line.split()
        lines = []
        for x in line:
            # 1. clean punctuation
            x = clean_text(x)
            # 2. clean numbers
            x = clean_numbers(x)
            # 3. Removing contractions
            x = replace_contractions(x)
            lines.append(x)

        # 4. tokenizer
        word_lines = lines
        num_lines = tokenize([lines], max_features = len(lines))[0]
        # 5. load glove and map them
        lines = dict(zip(word_lines, num_lines))
        emb_matrix, num_lines = create_glove(lines, emb_index)
        # we compute its mean along the rows of emb matrix
        embedding = emb_matrix.sum(axis = 0) / num_lines # divided by number of lines without None
        papers.append(embedding)

    papers = np.asarray(papers)

    print()

    return papers


## unit test
if __name__ == '__main__':
    data = pd.read_csv('../soup/data/allinfo.csv', sep = '#')
    papers = preprocess(data)
    print(papers)
    print(papers.shape)
