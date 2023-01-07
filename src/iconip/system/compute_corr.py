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
Compute inter-instance system-level correlatoin
"""
import logging
from eval.utils import make_parent_dirs
from iconip.system import make_system_scores, SAVE_ROOT
from iconip import CORR_METHODS


def compute():
    scores = make_system_scores()
    scores = scores.rename(index=lambda x: '({}, {})'.format(*x))  # Make tuple columns to str.
    print(scores.index)
    scores = scores.transpose()
    for method in CORR_METHODS:
        logging.info('computing method {}'.format(method))
        corr = scores.corr(method)
        output = make_parent_dirs(SAVE_ROOT / 'corr' / method / 'corr.json')
        corr.to_json(output)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    compute()
