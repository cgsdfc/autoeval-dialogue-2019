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
import pickle

from eval.config_parser import parse_dataset
from eval.repo import all_datasets

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    datasets = parse_dataset(all_datasets)
    for ds in datasets:
        logging.info('checking {}'.format(ds))
        len_contexts = len(open(ds.contexts).readlines())
        len_references = len(open(ds.references).readlines())
        len_test_dialog = len(pickle.load(open(ds.test_dialogues, 'rb')))

        if len_contexts != len_references:
            logging.warning('{}: contexts != reference'.format(ds))
        if len_references != len_test_dialog:
            logging.warning('{}: references != test_dialog'.format(ds))
