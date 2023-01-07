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

import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pandas import DataFrame

from eval.consts import PLOT_FILENAME, DATA_V2_ROOT
from eval.data import UtterScoreDist, load_score_db_index, seaborn_setup

NAME = 'distplot'

logger = logging.getLogger(__name__)

__version__ = '0.0.1'


def get_output(prefix: Path, triple):
    return prefix / NAME / triple.dataset / triple.model / triple.metric / PLOT_FILENAME


def do_distplot(data: UtterScoreDist, output):
    fig = Figure()
    FigureCanvas(fig)
    ax = fig.add_subplot(111)
    sns.distplot(data.utterance, ax=ax)
    ax.set_title('{} of {} on {}'.format(data.metric, data.model, data.dataset))
    logger.info('plotting to {}'.format(output))
    fig.savefig(str(output))


def plot(df: DataFrame, prefix: Path):
    for triple in df.itertuples(index=False):
        output = get_output(prefix, triple)
        if not output.parent.is_dir():
            output.parent.mkdir(parents=True)

        data = UtterScoreDist(triple.filename, scale_values=True, normalize_names=True)
        do_distplot(data, output)


if __name__ == '__main__':
    seaborn_setup()
    df = load_score_db_index()
    prefix = Path(DATA_V2_ROOT).joinpath('plot')

    plot(df, prefix)
