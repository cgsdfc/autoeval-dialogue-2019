# MIT License
# 
# Copyright (c) 2022 cgsdfc
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pickle

from eval.config_parser import parse_dataset
from eval.repo import all_datasets
from eval.utils import Dataset


def unpickle(path):
    return pickle.load(open(path, 'rb'))


class DatasetStats:
    class CorpusStats:
        def __init__(self, corpus):
            self.corpus = corpus
            pass

        @property
        def n_examples(self):
            return len(self.corpus)

        @property
        def n_tokens(self):
            return sum(len(u) for u in self.corpus)

    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.train_set_data = None
        self.test_set_data = None
        self.vocab_data = None

    @property
    def vocab_size(self):
        if self.vocab_data is None:
            self.vocab_data = unpickle(self.dataset.vocabulary)
        return len(self.vocab_data)

    @property
    def train_stats(self):
        if self.train_set_data is None:
            self.train_set_data = unpickle(self.dataset.train_set)
        return self.CorpusStats(self.train_set_data)

    @property
    def test_stats(self):
        if self.test_set_data is None:
            self.test_set_data = unpickle(self.dataset.test_dialogues)
        return self.CorpusStats(self.test_set_data)


def train_stats():
    for ds in parse_dataset(all_datasets):
        ds_stats = DatasetStats(ds)
        print(ds.name)
        print('vocab_size {}'.format(ds_stats.vocab_size))
        print('train.n_examples {}'.format(ds_stats.train_stats.n_examples))
        print('train.n_tokens {}'.format(ds_stats.train_stats.n_tokens))
        print()


def test_stat():
    for ds in parse_dataset(all_datasets):
        ds_stats = DatasetStats(ds)
        print(ds.name)
        print('test.n_examples {}'.format(ds_stats.test_stats.n_examples))
        print('test.n_tokens {}'.format(ds_stats.test_stats.n_tokens))
        print()


if __name__ == '__main__':
    test_stat()
