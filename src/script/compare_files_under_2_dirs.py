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
from eval.data import find_all_data_files
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_1')
    parser.add_argument('dir_2')
    args = parser.parse_args()

    data_files = find_all_data_files(args.dir_1)
    missing = 0
    inconsistent = 0

    for file in data_files:
        file_2 = Path(args.dir_2).with_name(file.name)
        if not file_2.is_file():
            missing += 1
            logging.info('dir_2: {} not a file'.format(file_2))
        elif file_2.read_bytes() != file.read_bytes():
            inconsistent += 1
            logging.info('file content not the same:')
            logging.info('file_1: {}'.format(file))
            logging.info('file_2: {}'.format(file_2))

    logging.info('missing {}'.format(missing))
    logging.info('inconsistent {}'.format(inconsistent))
