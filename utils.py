#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import random

import numpy as np


def read_data(filename):
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    data = list(data)
    return data


def index_data(sentences, dictionary):
    shape = sentences.shape
    sentences = sentences.reshape([-1])
    index = np.zeros_like(sentences, dtype=np.int32)
    for i in range(len(sentences)):
        try:
            index[i] = dictionary[sentences[i]]
        except KeyError:
            index[i] = dictionary['UNK']

    return index.reshape(shape)


def get_train_data(vocabulary, batch_size, num_steps):
    ##################
    # Your Code here
    ##################
    data_length = len(vocabulary)
    x_raw = vocabulary
    y_raw = x_raw[1:]
    y_raw.append(x_raw[-1]) 

    num_samples = data_length // num_steps
    num_batches = num_samples // batch_size

    x_data_sampled = [ x_raw[num_steps * i : num_steps * (i + 1)] for i in range(num_samples) ]
    y_data_sampled = [ y_raw[num_steps * i : num_steps * (i + 1)] for i in range(num_samples) ]

    for i in range(num_batches):
        x_data = x_data_sampled[batch_size * i : batch_size * (i + 1)]
        y_data = y_data_sampled[batch_size * i : batch_size * (i + 1)]
        yield (np.array(x_data), np.array(y_data))


def build_dataset(words, n_words):
    """Process raw inputs into a dataset."""
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(n_words - 1))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        index = dictionary.get(word, 0)
        if index == 0:  # dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reversed_dictionary
