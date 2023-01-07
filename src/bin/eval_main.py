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

from eval.config_parser import load_config
from eval.engine import Engine

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Run the automatic evaluation engine')
    parser.add_argument('-c', '--config', help='path to config file (default to builtin config)')
    parser.add_argument('-p', '--prefix', help='path to output directory')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force to overwrite existing files (default is to skip)')
    args = parser.parse_args()

    if args.config:
        config = load_config(args.config)
    else:
        from eval.repo import default_config as config

    engine = Engine(config, args.prefix, args.force)
    engine.run()