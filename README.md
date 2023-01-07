# Automatic Evaluation of Generative Dialogue Systems

## Introduction

This repository contains the LaTeX and Python sources of my bachelor's graduation project done at Beihang University in 2019. This work is mainly concerned with the automatic evaluation of the generative dialogue systems based on the Seq2Seq framework with a special focus on content diversity. This work was initially carried out as a graduation project and later it was extended with more in-depth analyses to form a submission to ICONIP-2019. Thanks to this process, it now contains both a Chinese version and an English version as follows:

- [Chinese version](docs/paper-zh.pdf) is the original version written as a bachelor's graduation project, namely, *A Diversity-oriented Analysis on Evaluating the Generative Dialogue Models*.
- [English version](docs/paper-en.pdf) is an extension of the Chinese version and a submission to ICONIP-2019, namely, *Automatic Evaluation of Generative Dialogue Systems: An Empirical Study*.

The code locations are listed as follows:

- [paper-zh](paper-zh/README.md) contains the LaTeX source of the Chinese version.
- [paper-en](paper-zh/README.md) contains the LaTeX source of the Chinese version.
- [src](src/README.md) contains the Python source of the benchmark framework called `Eval`.
- [neural-dialogue-metrics](https://github.com/neural-dialogue-metrics) contain our implementations of several classical dialogue evaluation metrics, i.e., BLEU, ROUGE, METEOR, Distinct-N, EmbeddingBased, etc. 

## Briefing

This work is primarily an empirical study of the behaviors of dialogue metrics. Specifically, we categorized metrics into three groups, namely, n-gram-based, embedding-based, and model-based. Three representative Seq2Seq-based generative dialogue models were selected, namely, the LSTM language model, HRED, and VHRED. Three popular datasets were selected, namely, OpenSubtitles, Ubuntu, and LSDSCC. A grid of experiments composed of these metrics, models, and datasets was then carried out and results were collected and analyzed. We first looked at the system-level scores (which measured how well a model behaved on a dataset) in a big table and found that no system could beat all the other ones along the datasets axis or metrics axis. This is likely due to the *No Free Lunch Theorem, NFL*. Then, we looked at the utterance-level scores (which measured how good a generated response is) and plotted various diagrams for each (dataset, metric, model) triple. We found that 

## Limitations

- This work basically reproduced known facts about dialogue metrics and systems. No new metrics, models, nor datasets were proposed.
- This work has been outdated since it was written in the age of the Seq2Seq framework. Now that the Transformer-based models have advanced the field of dialogue systems significantly, it is time for this work to retire.

## Links

Here are some useful links related to this project:

- The main codebase for generating and analyzing data is at [Eval](https://github.com/neural-dialogue-metrics/Eval.git).
- My graduate design done at Beihang University is at [GraduateDesign](https://github.com/cgsdfc/GraduateDesign.git), which is the origin of this work.
- This work is mainly inspired by the work of Liu et al., namely *How NOT to Evaluate Your Dialogue Systems: An Empirical Study of Unsupervised Evaluation Metrics for Dialogue Response Generation*.
- My fork of the wonderful generative models created by Serban et al. is at [HRED-VHRED](https://github.com/cgsdfc/HRED-VHRED.git). The original project can be found [here](https://github.com/julianser/hed-dlg-truncated.git).
- My fork of the wonderful but messy codebase of Li et al. is at [Neural-Dialogue-Generation](https://github.com/cgsdfc/Neural-Dialogue-Generation.git). The original project can be found [here](https://github.com/jiweil/Neural-Dialogue-Generation.git).

## Acknowledgement

- This work was supervised by Prof. Wenge Rong, School of Computer Science and Engineering, Beihang University. Sincerely thanks to my supervisor.
- This work was inspired by *Liu, C.W., R., Serban, How NOT to evaluate your dialogue system: An empirical study of unsupervised evaluation metrics for dialogue response generation. EMNLP-2016*. Many thanks for your insights and efforts in making dialogue systems better.


