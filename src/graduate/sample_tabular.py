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

import json
import logging
from pathlib import Path

from pylatex import Table, Label, Marker, Command, LongTabularx
from pylatex.utils import bold, NoEscape

from eval.normalize import normalize_name
from eval.utils import make_parent_dirs

column2text = {
    'context': '消息：',
    'reference': '参考：',
    'response': '响应：',
}

TABULAR_TEX = 'tabular.tex'
TABLE_TEX = 'table.tex'


def fill_data_in_tabular(data: list, truncate=None):
    if truncate:
        data = data[:truncate]

    tabular = LongTabularx(
        table_spec='rX',
        width_argument=NoEscape(r'0.8\textwidth'),
        booktabs=True
    )
    # tabular.append(Command('small'))
    tabular.add_hline()
    for item in data:
        for key, value in column2text.items():
            cells = [bold(value), item[key]]
            tabular.add_row(cells)
        tabular.add_hline()
    return tabular


def wrap_in_table(tabular_path, dataset, model):
    table = Table(position='H')
    model = normalize_name('model', model)
    dataset = normalize_name('dataset', dataset)
    table.append(Command('small'))
    table.append(Command('centering'))
    table.add_caption(f'{model} 在 {dataset} 上的取样')
    table.append(Label(Marker(prefix='tab', del_invalid_char=False, name=f'{model}_{dataset}_sample')))
    table.append(Command('input', arguments=str(tabular_path)))
    return table


def make_tabular(src_prefix: Path = None, dst_prefix: Path = None):
    if src_prefix is None:
        src_prefix = Path('/home/cgsdfc/Metrics/Eval/data/v2/example/sample')
    if dst_prefix is None:
        dst_prefix = Path('/home/cgsdfc/GraduateDesign/data/sample')

    def parse_url(path: Path):
        k, dataset, model, file = path.parts[-4:]
        return dataset, model

    for src in src_prefix.rglob('*.json'):
        data = json.load(src.open())
        tabular = fill_data_in_tabular(data, 5)
        dataset, model = parse_url(src)
        subdir = make_parent_dirs(dst_prefix / dataset / model)

        output = subdir.joinpath(TABULAR_TEX)
        table = wrap_in_table(output, dataset, model)
        logging.info('writing tabular to {}'.format(output))
        output.write_text(tabular.dumps())

        output = subdir.joinpath(TABLE_TEX)
        logging.info('writing table to {}'.format(output))
        output.write_text(table.dumps())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    make_tabular()
