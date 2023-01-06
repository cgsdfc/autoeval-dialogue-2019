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

import logging
import math
import re

from pandas import DataFrame, Series

logger = logging.getLogger(__name__)


def exact(string):
    return lambda s: s == string


def contains(string):
    return lambda s: string in s


def re_match(pattern):
    return lambda s: re.match(pattern, s)


class MetricGroup:

    @classmethod
    def num_groups(cls):
        return len(cls.group_matchers)

    group_matchers = {
        'Embedding': contains('embedding_based'),
        'BLEU': contains('bleu'),
        'Distinct-N': re_match(r'distinct_\d'),
        'ROUGE-N': re_match(r'rouge_\d'),
        'ROUGE-L/W': re_match(r'rouge_[lw]'),
        'ADEM': exact('adem'),
        '#words': exact('utterance_len'),
        'METEOR': exact('meteor'),
    }

    def assign_group(self, df: DataFrame):
        group_values = []
        for mc in df.metric.values:
            for name, matcher in self.group_matchers.items():
                if matcher(mc):
                    group_values.append(name)
                    break
            else:
                raise ValueError('unable to match {} against one of {}'.format(
                    mc, tuple(self.group_matchers.keys())))
        return Series(group_values)

    def check_group(self, df: DataFrame):
        errs = 0
        for metric, group in df.loc[:, ['metric', 'group']].values:
            logger.info('{} => {}'.format(metric, group))
            matcher = self.group_matchers[group]
            if not matcher(metric):
                errs += 1
                logger.error('mismatched metric {} to group {}'.format(metric, group))
        if errs:
            raise ValueError('there are mismatches')

    def add_group_column_to_df(self, df: DataFrame, col_name=None):
        if col_name is None:
            col_name = 'group'
        return df.reset_index().assign(**{col_name: self.assign_group})


def get_col_wrap(num_items):
    return int(math.sqrt(num_items + 1))
