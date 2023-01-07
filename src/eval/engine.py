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

import itertools
import logging
import pprint
from pathlib import Path

from eval.config_parser import parse_models_and_datasets, parse_metrics
from eval.exporter import Exporter
from eval.loader import ResourceLoader
from eval.utils import UnderTest

logger = logging.getLogger(__name__)


def parse_config(config):
    metrics = parse_metrics(config['metrics'])
    models_and_datasets = parse_models_and_datasets(config)
    return [
        UnderTest(metric=metric, model=model, dataset=dataset)
        for metric, (model, dataset) in itertools.product(metrics, models_and_datasets)
    ]


class Engine:
    def __init__(self, config, save_dir, force=False):
        self.exporter = Exporter(save_dir)
        self.loader = ResourceLoader()
        self.config = config
        self.force = force
        self.under_tests = parse_config(config)

    def is_outdated(self, output: Path, under_test):
        if not output.exists():
            return True
        filenames = self.loader.get_filenames(under_test).values()
        for file in filenames:
            if not file.exists():
                return True
            if file.stat().st_mtime > output.stat().st_mtime:
                logger.info('file {} is newer than {}'.format(file, output))
                return True
        return False

    def run(self):
        logger.info('save_dir: %s', self.exporter.save_dir)
        logger.info('config: %s', pprint.pformat(self.config))

        self.exporter.export_config(self.config)
        for under_test in self.under_tests:
            output_path = self.exporter.get_output_path(under_test)
            if not self.is_outdated(output_path, under_test) and not self.force:
                logger.info('skipping up-to-date file %s', output_path)
                continue

            logger.info('Running under_test: %r', under_test)
            payload = self.loader.load_resources(under_test)
            if payload is None:
                continue

            logger.info('Calculating scores...')
            try:
                result = under_test.metric(**payload)
            except KeyboardInterrupt:
                logging.warning('interrupted, skipping...')
            else:
                self.exporter.export_json(result, under_test)
        logger.info('run {} under_tests'.format(len(self.under_tests)))
        logger.info('all done')
