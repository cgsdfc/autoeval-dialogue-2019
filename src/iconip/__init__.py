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

"""
Visualization scripts for my submission to ICONIP2019.
"""

import functools
from pathlib import Path
import pickle
from eval.utils import make_parent_dirs
import logging

import seaborn as sns
from pandas import DataFrame
from pathlib import Path
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
SAVE_ROOT = Path('/home/cgsdfc/Metrics/Eval/data/v2/iconip/system')


def cache_this(cache_path, load=pickle.load, dump=pickle.dump):
    """
    A decorator that implements a function with optional cache on the filesystem.

    :param fn: fn does the real computation.
    :param cache_path: used to store the serialized results of fn.
    :param load: `load(path)` -> deserialized object.
    :param dump: `dump(obj, path)` -> serialize object to path.
    :return:
    """
    cache_path = Path(cache_path)

    def decorate(fn):
        @functools.wraps(fn)
        def impl(*args, use_cache=True, **kwargs):
            if cache_path.is_file() and use_cache:
                logger.debug('cache hit, load from {}'.format(cache_path))
                return load(cache_path.open('rb'))
            logger.debug('calling {}'.format(fn.__name__))
            data = fn(*args, **kwargs)
            make_parent_dirs(cache_path)
            dump(data, cache_path.open('wb'))
            return data

        return impl

    return decorate


CORR_METHODS = ['pearson', 'spearman', 'kendall']


class CorrHeatmapPlotter:
    cmap = sns.diverging_palette(240, 10, as_cmap=True)

    def plot(self, corr: DataFrame, output: Path, annot=False):
        # Plotting logic.
        plt.gcf().subplots_adjust(bottom=0.18, right=1.0)  # Fit all labels in.
        # Mask is not used.
        # mask = np.zeros_like(corr, dtype=np.bool)
        # mask[np.triu_indices_from(mask)] = True
        logger.info('plotting to {}'.format(output))
        ax = sns.heatmap(
            corr, center=0, cmap=self.cmap, vmax=1, vmin=-1,
            square=True, linewidth=0.5, annot=annot,
            cbar_kws={
                'shrink': 0.5
            })
        ax.set_aspect('equal')
        plt.savefig(output, bbox_inches='tight')
        plt.close('all')
