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

from setuptools import setup

from eval import __version__

setup(
    name='EvalHelper',
    version=__version__,
    description='Evaluation Helper',
    author='cgsdfc',
    author_email='cgsdfc@126.com',
    keywords=[
        'NL', 'CL', 'MT',
        'natural language processing',
        'computational linguistics',
        'machine translation',
    ],
    scripts=[
        'bin/eval_main.py',
    ],
    packages=[
        'eval',
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: ',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic'
    ],
    license='LICENCE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        # eval:
        'numpy',
        'nltk',
        'embeddingbased',
        'lsdscc',
        'rouge',
        'distinct_n',

        # corr:
        'seaborn',
        'matplotlib',
        'pandas',
        'scikit-learn',
        'scipy',
    ]
)
