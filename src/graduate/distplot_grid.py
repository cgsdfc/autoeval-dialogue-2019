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
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame, Series
from seaborn import FacetGrid

from eval.consts import PLOT_FILENAME
from eval.data import UtterScoreDist, load_score_db_index
from eval.normalize import normalize_names_in_df

NAME = 'distplot_grid'

logger = logging.getLogger(__name__)

__version__ = '0.0.1'


def get_output(prefix: Path, metric):
    output = prefix / NAME / metric / PLOT_FILENAME
    if not output.parent.exists():
        output.parent.mkdir(parents=True)
    return output


def do_distplot(ax, data: UtterScoreDist):
    sns.distplot(data.utterance, ax=ax)
    ax.set_title('{} on {}'.format(data.model, data.dataset))


def distplot_wrapper(filename: Series, **kwargs):
    filename = filename.values[0]
    data = UtterScoreDist(filename, normalize_names=True, scale_values=True)
    sns.distplot(data.utterance, **kwargs)
    plt.title('{} on {}'.format(data.model, data.dataset))


def plot(data_index: DataFrame, prefix: Path):
    data_index = data_index.sort_values(by=['metric', 'model', 'dataset'])

    for metric, df2 in data_index.groupby('metric'):
        df2 = df2.reset_index()
        output = get_output(prefix, metric)
        df2 = normalize_names_in_df(df2)
        g = FacetGrid(df2, row='model', col='dataset')

        g.map(distplot_wrapper, 'filename')
        g.set_xlabels('')
        g.set_titles('{row_name} on {col_name}')
        logger.info('plotting to {}'.format(output))
        g.savefig(output)
        plt.close('all')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sns.set(color_codes=True, font='Times New Roman')

    dst_prefix = Path('/home/cgsdfc/Metrics/Eval/data/v2/plot')

    df = load_score_db_index(
        Path('/home/cgsdfc/Metrics/Eval/data/v2/score/db')
    )

    plot(df, dst_prefix)
