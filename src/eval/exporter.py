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

import numbers
import logging
from pathlib import Path
import numpy as np
import pprint
import json

from eval.consts import CONFIG_JSON

logger = logging.getLogger(__name__)


class Exporter:

    def __init__(self, save_dir):
        self.save_dir = Path(save_dir)

    def process_result(self, result, under_test):
        metric = under_test.metric
        utterance, system = result

        def extract_fields(score, fields):
            if not fields:
                if isinstance(score, numbers.Number):
                    return score
                return score.__dict__
            if isinstance(fields, str):
                return getattr(score, fields)
            fields = tuple(fields)
            return {name: getattr(score, name) for name in fields}

        utterance = [extract_fields(score, metric.utterance_field) for score in utterance]
        if system is None:
            system = np.mean(utterance)
        else:
            system = extract_fields(system, metric.system_field)
        logging.info('utterance: %s', pprint.pformat(utterance))
        logger.info('system: %s', system)
        return dict(
            utterance=utterance,
            system=system,
            metric=under_test.metric_name,
            model=under_test.model_name,
            dataset=under_test.dataset_name,
        )

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool):
            return bool(obj)
        elif isinstance(obj, Path):
            return str(obj)
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            raise TypeError

    def export_json(self, result, under_test):
        result = self.process_result(result, under_test)
        output_path = self.get_output_path(under_test)

        logger.info('Saving scores to %s', output_path)
        with output_path.open('w') as f:
            json.dump(result, f, default=self.default)

    def get_output_path(self, under_test):
        prefix = under_test.prefix
        output_path = self.save_dir.joinpath(prefix).with_suffix('.json')
        return output_path

    def export_config(self, config):
        config_json = self.save_dir.joinpath(CONFIG_JSON)
        config_json.write_text(json.dumps(config, default=self.default))
