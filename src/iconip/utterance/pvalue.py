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

"""
Compute the p-value for all correlation methods.

The smaller the p-value, the higher the significance.
"""
import logging
import json
import pandas
import pickle
from itertools import combinations, product
from collections import defaultdict
import numpy as np
from pandas import DataFrame
from scipy.stats import pearsonr, spearmanr, kendalltau

from eval.utils import make_parent_dirs
from iconip.utterance import load_all_scores, SAVE_ROOT


def compute_pvalue(scores: DataFrame, method):
    """
    Compute the p-value of the given correlation method.
    The correlation is *between two metrics*, not between *two examples*.

    :param scores: a df of score matrix.
    :return: a df of symmetric matrix of p-value.
    """

    items = defaultdict(dict)
    for x, y in product(scores.columns, repeat=2):
        corr, pvalue = method(scores[x], scores[y])
        if np.isnan(pvalue):
            pvalue = 0  # NaN handling?
        items[x][y] = pvalue

    return items


def get_output(method_name, *key):
    return make_parent_dirs(SAVE_ROOT / 'pvalue' / method_name / key[0] / key[1] / 'data.json')


def compute():
    method_dict = {
        'pearson': pearsonr,
        'spearman': spearmanr,
        'kendall': kendalltau,
    }
    for key, value in load_all_scores().items():
        for method_name, method in method_dict.items():
            output = get_output(method_name, *key)
            logging.info('computing pvalue for {}, method={}'.format(key, method_name))
            try:
                pvalue = compute_pvalue(value, method)
                json.dump(pvalue, output.open('w'))
            except OverflowError as e:
                logging.warning(e)


THESHOLD = 0.05


# The format we created in compute_pvalue() is just ok for pd.read_json().
def load_pvalue_for(method, model, dataset):
    """
    Load the p-value for the specific args.

    :param method:
    :param model:
    :param dataset:
    :return:
    """
    output = get_output(method, model, dataset)
    return pandas.read_json(output)


def find_high_value(method='pearson'):
    files = (SAVE_ROOT / 'pvalue').rglob('{}/**/data.json'.format(method))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    compute()
