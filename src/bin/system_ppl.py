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

from pathlib import Path
import argparse
from eval.data import UtterScoreDist
import logging
import pprint as pp

METRIC_NAME = 'serban_ppl'

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Report system PPL from score files')
    parser.add_argument('-p', '--prefix', help='the location of the PPL score files')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    files = Path(args.prefix).glob(f'*{METRIC_NAME}.json')
    files = list(files)
    logging.info('Found PPL score files:\n{}'.format(pp.pformat(files)))

    for file in files:
        score_dist = UtterScoreDist(file)
        print(f"""
        Model: {score_dist.model}
        Dataset: {score_dist.dataset}
        PPL: {score_dist.system:.4f}
        """)
