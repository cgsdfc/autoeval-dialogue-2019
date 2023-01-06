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
A random model -- shuffle the ground truth as output
"""
import argparse
import logging
from pathlib import Path

import numpy as np

from eval.config_parser import load_config, parse_dataset
from eval.consts import RANDOM_MODEL_ROOT
from eval.repo import get_model

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Run the random model (response by randomly shuffling the references')
    parser.add_argument('-c', '--config')
    parser.add_argument('-p', '--prefix')
    args = parser.parse_args()
    prefix = Path(args.prefix or RANDOM_MODEL_ROOT)
    logging.basicConfig(level=logging.INFO)

    if args.config is None:
        from eval.repo import all_datasets as datasets
    else:
        datasets = load_config(args.config)['datasets']

    datasets = parse_dataset(datasets)
    # note the last line does not end with \n.
    for ds in datasets:
        logging.info('dataset: {}'.format(ds.references))
        references = Path(ds.references).read_text().splitlines()
        np.random.shuffle(references)

        output = get_model('random', ds.name).responses
        if not output.parent.exists():
            output.parent.mkdir(parents=True)
        output.write_text('\n'.join(references))
