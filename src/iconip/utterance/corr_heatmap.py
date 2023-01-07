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
Correlation heatmap of various metrics for each instance.

This a direct visualization of the correlation matrix. Each number of the matrix is replaced by a colored
cell, reflecting the magnitude of the value. Specifically, possitive correlation uses warm color while
negative correlation uses cold color. Zero correlation uses white.
"""

import logging

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from seaborn import heatmap

from eval.consts import PLOT_FILENAME
from eval.utils import make_parent_dirs
from iconip.utterance import PLOT_ROOT, load_all_corr
from iconip import CorrHeatmapPlotter

# Generate a red-blue-white palette.
# See http://seaborn.pydata.org/generated/seaborn.diverging_palette.html
cmap = sns.diverging_palette(240, 10, as_cmap=True)
VERSION = 'v4'


def plot_heatmap():
    """
    Plots all the heatmaps.

    :return:
    """
    sns.set(font_scale=0.9, style='white', font='Times New Roman')
    p = CorrHeatmapPlotter()
    for (method, model, dataset), corr in load_all_corr().items():
        output = PLOT_ROOT / 'plot' / 'heatmap' / VERSION / method / model / dataset / PLOT_FILENAME
        logging.info('plotting to {}'.format(output))
        output = make_parent_dirs(output)
        p.plot(corr, output)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    plot_heatmap()
