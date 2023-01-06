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

from pathlib import Path
from eval.normalize import normalize_name

from pylatex import Figure, Label, Marker, NoEscape


def make_figures(plot_prefix: Path, dst_prefix: Path, fig_width: float):
    files = list(plot_prefix.rglob('*.pdf'))
    width_arg = r'{}\textwidth'.format(fig_width)
    width_arg = NoEscape(width_arg)

    for file in files:
        metric = file.parent.name
        norm_metric = normalize_name('metric', metric)
        output = dst_prefix.joinpath(metric).with_suffix('.tex')
        figure = Figure(position='H')
        figure.add_image(filename=str(file), width=width_arg)
        figure.add_caption('{} 的概率分布图'.format(norm_metric))
        figure.append(Label(Marker(
            prefix='fig',
            name=NoEscape('{}dist'.format(norm_metric)),
        )))
        output.write_text(figure.dumps())


FIGURE_WIDTH = 0.6

if __name__ == '__main__':
    plot_prefix = Path('/home/cgsdfc/Metrics/Eval/data/v2/plot/distplot_grid')
    dst_prefix = Path('/home/cgsdfc/GraduateDesign/data').joinpath('distplot_grid')
    if not dst_prefix.exists():
        dst_prefix.mkdir(parents=True)

    make_figures(
        plot_prefix=plot_prefix,
        dst_prefix=dst_prefix,
        fig_width=FIGURE_WIDTH,
    )
