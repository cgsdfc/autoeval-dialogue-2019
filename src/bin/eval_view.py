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

import argparse
import io
import pickle
import pprint
import subprocess
from pathlib import Path

from eval.repo import get_model, get_dataset

TEXTUAL_FORMATS = {
    '.txt', '.csv', '.tsv',
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser('View various info about models and datasets')
    parser.add_argument('-m', '--model', help='specify a model name')
    parser.add_argument('-d', '--dataset', help='specify a dataset name (needed with -m)')
    parser.add_argument('-w', '--what', help='the object to inspect')
    args = parser.parse_args()

    if args.model:
        if args.dataset is None:
            parser.error('dataset is needed with model')
        obj = get_model(args.model, trained_on=args.dataset)
    elif args.dataset:
        obj = get_dataset(args.dataset)
    else:
        parser.error('no model or dataset specified!')

    if args.what is None:
        pprint.pprint(obj.__dict__)
        parser.exit(0)

    attr = getattr(obj, args.what)
    path = Path(attr)
    if not path.exists():
        parser.error('{}={} is not a valid path'.format(args.what, path))

    if path.suffix in TEXTUAL_FORMATS:
        parser.exit(
            subprocess.call(['less', str(path)])
        )
    elif path.suffix == '.pkl':
        obj = pickle.loads(path.read_bytes())
        obj = pprint.pformat(obj)
        parser.exit(
            subprocess.call(
                ['less'],
                stdin=io.BytesIO(obj)
            )
        )
    else:
        parser.error('unknown format {} for {}'.format(path.suffix, path))
