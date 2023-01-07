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
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from eval.consts import DATA_V2_ROOT
from eval.utils import make_parent_dirs
from graduate.annotated import load_annotated_index, FILENAME

__version__ = '0.0.1'

NAMESPACE = 'sample'

CRR = ['context', 'reference', 'response']


def get_output(prefix: Path, k, dataset, model):
    return make_parent_dirs(prefix / 'example' / NAMESPACE / str(k) / dataset / model / FILENAME)


def get_metrics(df: DataFrame):
    for col, dtype in df.dtypes.items():
        if col not in CRR:
            yield col


def make_sample(df: DataFrame, k=None, prefix: Path = None):
    if k is None:
        k = 10
    if prefix is None:
        prefix = Path(DATA_V2_ROOT)

    for row in df.itertuples(index=False):
        df2: DataFrame = pd.read_json(row.path)
        df2 = df2.sample(n=k)
        crr = df2[CRR]
        output = get_output(
            prefix=prefix,
            k=k,
            dataset=row.dataset,
            model=row.model,
        )
        logging.info('writing to {}'.format(output))
        crr.to_json(output, orient='records')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    df = load_annotated_index()
    make_sample(df)
