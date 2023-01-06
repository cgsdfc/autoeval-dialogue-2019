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

from eval.config_parser import product_models_datasets, parse_dataset
from eval.repo import all_datasets, get_dataset
from models import find_serban_models
from eval.utils import load_template, get_random_gpu
from eval.models import SerbanModel

logger = logging.getLogger(__name__)
train_template = load_template('serban_train')
sample_template = load_template('serban_sample')


def get_train(model: SerbanModel, name):
    save_dir = model.weights.parent
    model_prefix = model.weights.name.replace('_model.npz', '')
    prototype = model.prototype
    return train_template.format(
        name=name,
        save_dir=save_dir,
        prototype=prototype,
        model_prefix=model_prefix,
        gpu=get_random_gpu(),
    )


def get_sample(model: SerbanModel, name):
    model_prefix = model.weights.with_name(model.weights.name.replace('_model.npz', ''))
    context = get_dataset(model.trained_on).contexts
    output = model.responses
    return sample_template.format(
        name=name,
        model_prefix=model_prefix,
        context=context,
        output=output,
        gpu=get_random_gpu(),
    )


def train_and_sample_scripts(output_dir: Path):
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    scripts_map = {
        'train': get_train,
        'sample': get_sample,
    }

    for model in find_serban_models():
        for name, gen_fn in scripts_map.items():
            script = output_dir.joinpath('_'.join((model.name, model.trained_on, name))).with_suffix('.sh')
            logger.info('new script: {}'.format(script))
            script.write_text(gen_fn(model, script.stem))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prefix')
    args = parser.parse_args()
    train_and_sample_scripts(Path(args.prefix))
