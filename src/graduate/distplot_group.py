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
import re
from pathlib import Path

import matplotlib.pyplot as plt
from pandas import DataFrame
from seaborn import FacetGrid

from eval.consts import PLOT_FILENAME, DATA_V2_ROOT
from eval.data import load_score_db_index, seaborn_setup, get_schema_name
from eval.group import get_col_wrap, MetricGroup, contains, re_match
from eval.normalize import normalize_names_in_df
from eval.utils import make_parent_dirs
from graduate.distplot_grid import distplot_wrapper

NAME = get_schema_name(__file__)

logger = logging.getLogger(__name__)

__version__ = '0.0.2'

MODEL = 'hred'
DATASET = 'opensub'


class MyGroup(MetricGroup):
    group_matchers = {
        'BLEU': contains('bleu'),
        'Embedding/ADEM': lambda s: 'embedding_based' in s or s == 'adem',
        'ROUGE-N': re_match(r'rouge_\d'),
        'Distinct/ROUGE-L,-W': lambda s: re.match(r'(distinct_\d|rouge_[lw])', s),
        'Others': lambda s: True,
    }


def get_output(prefix: Path, group):
    return make_parent_dirs(prefix / NAME / DATASET / MODEL / group / PLOT_FILENAME)


def plot(df: DataFrame, prefix: Path):
    for group, df2 in df.groupby('group'):
        num_metrics = len(df2.metric.unique())
        logger.info('#metrics {} in group {}'.format(num_metrics, group))
        g = FacetGrid(df2, col='metric', col_wrap=get_col_wrap(num_metrics))
        g.map(distplot_wrapper, 'filename')
        g.set_xlabels('')
        # g.set_titles(col_template='{metric}')
        output = get_output(prefix, group)
        logger.info('plotting to {}'.format(output))
        g.savefig(output)
        plt.close('all')


def preprocess() -> DataFrame:
    df = load_score_db_index()
    df = df[(df.model == MODEL) & (df.dataset == DATASET) & (df.metric != 'serban_ppl')]
    df = MyGroup().add_group_column_to_df(df)
    df = df.sort_values('metric')
    df = normalize_names_in_df(df)
    return df


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    seaborn_setup()
    prefix = Path(DATA_V2_ROOT).joinpath('plot')
    df = preprocess()
    plot(df, prefix)
