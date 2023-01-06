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
Clustermap of seaborn.

This currently does not work since `seaborn.clustermap()` does not support passing precomputed
corr matrix and thus we can't handle the NaN and neither can seaborn.
"""
import logging

from pandas import DataFrame
from seaborn import clustermap

from eval.consts import PLOT_FILENAME
from eval.data import seaborn_setup
from eval.utils import make_parent_dirs
from iconip.utterance import load_all_scores, SAVE_ROOT

# For large dataset, sample it with this value.
THRESHOLD = 1000
VERSION = 'v2'


def plot_clustermap():
    """
    Plot all clustermaps.

    :return:
    """
    seaborn_setup()
    for key, value in load_all_scores().items():
        output = make_parent_dirs(SAVE_ROOT / 'plot' / 'clustermap' / VERSION / key[0] / key[1] / PLOT_FILENAME)
        if len(value) > THRESHOLD:
            logging.info('value too large: {}'.format(len(value)))
            value = value.sample(n=THRESHOLD)
        logging.info('plotting to {}'.format(output))
        try:
            g = clustermap(value, metric='correlation', vmin=-1, vmax=1, z_score=1, row_cluster=False)
        except Exception as e:
            logging.warning('error: {}'.format(e))
        else:
            g.savefig(output)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    plot_clustermap()
