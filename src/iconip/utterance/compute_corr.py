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
Compute inter-metric correlation on example-level and serialize the data.

The data is then analyzed and visualized in various ways. See `corr_heatmap.py` and other scripts.

Methods are:
    - Pearson's r
    - Spearman's r
    - Kendall's tau
"""
from iconip import CORR_METHODS
from iconip.utterance import load_all_scores, SAVE_ROOT
from eval.utils import make_parent_dirs
import logging

logger = logging.getLogger(__name__)


def compute_corr():
    """
    Compute and serialize correlation matrix for all (instance, method)s.

    :return:
    """
    for key, value in load_all_scores().items():
        for method in CORR_METHODS:
            logger.info('computing ({}, {}, {})'.format(method, *key))
            output = make_parent_dirs(
                SAVE_ROOT / 'corr' / method / key[0] / key[1] / 'corr.json'
            )
            corr = value.corr(method=method)
            # Note: NaN causes the linkage() to raise!
            # corr(X, Y) is NaN when one of X, Y is all-zero.
            corr.fillna(0, inplace=True)
            corr.to_json(output)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    compute_corr()
