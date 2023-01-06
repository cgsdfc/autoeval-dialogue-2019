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
Code for analysis of the system scores.
"""

from eval.data import load_system_score
from pandas import DataFrame
from iconip import cache_this, SAVE_ROOT


@cache_this(SAVE_ROOT / 'score' / 'cache.pkl')
def make_system_scores() -> DataFrame:
    """
    Create a df of (N, M) where N is the number of instances and M is the number of metrics.

    The `long_form_scores` returned by `load_system_score()` consists of (instance, score) records.
    With transformation it becomes records fields of instances. The fields are actually scores of
    various metrics. In this way, the df defines a matrix suitable for the analysis of
    pairwise correlation.

    :param long_form_scores: long-form systems scores by `load_system_score()`.
    :return: a matrix of `(#instances, #metrics)`.
    """
    long_form_scores: DataFrame = load_system_score()
    indices = []
    records = []
    for instance, value in long_form_scores.groupby(['model', 'dataset']):
        indices.append(instance)
        record = dict(value[['metric', 'system']].values)
        records.append(record)
    return DataFrame.from_records(records, indices)


if __name__ == '__main__':
    df = make_system_scores()
    print(df)
