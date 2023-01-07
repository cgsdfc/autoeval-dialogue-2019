# MIT License
# 
# Copyright (c) 2019 Cong Feng
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

import logging

from eval.config_parser import parse_dataset
from eval.consts import *
from eval.utils import Dataset
from eval.models import find_serban_models, find_random_models

logger = logging.getLogger(__name__)


def get_model(name, trained_on):
    for model in all_models:
        if name == model.name and trained_on == model.trained_on:
            return model
    raise ValueError('unknown model: {} trained on {}'.format(name, trained_on))


def get_dataset(name):
    try:
        params = dataset_repo[name]
    except KeyError as e:
        raise ValueError('unknown dataset: {}'.format(name)) from e
    return Dataset(name=name, **params)


def get_config(models=None, datasets=None, metrics=None):
    return {
        'models': models or all_models,
        'datasets': datasets or all_datasets,
        'metrics': metrics or all_metrics,
    }


all_models = find_serban_models() + find_random_models()

dataset_repo = {
    'ubuntu': {
        CONTEXTS: '/home/cgsdfc/UbuntuDialogueCorpus/ResponseContextPairs/raw_testing_contexts.txt',
        REFERENCES: '/home/cgsdfc/UbuntuDialogueCorpus/ResponseContextPairs/raw_testing_responses.txt',
        TEST_DIALOGUES: '/home/cgsdfc/UbuntuDialogueCorpus/Test.dialogues.pkl',
        VOCABULARY: '/home/cgsdfc/UbuntuDialogueCorpus/Dataset.dict.pkl',
        TRAIN_SET: '/home/cgsdfc/UbuntuDialogueCorpus/Training.dialogues.pkl',
    },
    'opensub': {
        CONTEXTS: '/home/cgsdfc/SerbanOpenSubData/dialogue_length3_6/eval/test.context.txt',
        REFERENCES: '/home/cgsdfc/SerbanOpenSubData/dialogue_length3_6/eval/test.response.txt',
        TEST_DIALOGUES: '/home/cgsdfc/SerbanOpenSubData/dialogue_length3_6/eval/test.dialogues.pkl',
        VOCABULARY: '/home/cgsdfc/SerbanOpenSubData/dialogue_length3_6/train.dict.pkl',
        TRAIN_SET: '/home/cgsdfc/SerbanOpenSubData/dialogue_length3_6/train.dialogues.pkl',
    },
    'lsdscc': {
        CONTEXTS: '/home/cgsdfc/SerbanLSDSCC/raw_test_dialogues.context',
        REFERENCES: '/home/cgsdfc/SerbanLSDSCC/raw_test_dialogues.response',
        TEST_DIALOGUES: '/home/cgsdfc/SerbanLSDSCC/vocab_35000/Test.dialogues.pkl',
        VOCABULARY: '/home/cgsdfc/SerbanLSDSCC/vocab_35000/Train.dict.pkl',
        TRAIN_SET: '/home/cgsdfc/SerbanLSDSCC/vocab_35000/Train.dialogues.pkl',
    }
}

all_datasets = parse_dataset(dataset_repo)

all_metrics = {
    'bleu': {
        'n': [1, 2, 3, 4],
        'smoothing': True,
    },
    'rouge': {
        'alpha': 0.9,
        'weight': 1.2,
        'n': [1, 2, 3, 4],
        'variants': [
            'rouge_n',
            'rouge_l',
            'rouge_w',
        ],
    },
    'distinct_n': {
        'n': [1, 2]
    },
    'embedding_based': {
        'variants': [
            'vector_average',
            'vector_extrema',
            'greedy_matching',
        ],
    },
    'adem': {},
    'meteor': {},
    # 'serban_ppl': {},
    'utterance_len': {},
}

default_config = {
    'models': all_models,
    'datasets': all_datasets,
    'metrics': all_metrics
}
