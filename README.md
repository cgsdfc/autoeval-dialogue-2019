[![CircleCI](https://circleci.com/gh/cgsdfc/ICONIP2019.svg?style=svg&circle-token=c7abc42f7d5476d0a13d2c1c927d9078f2f8df99)](https://circleci.com/gh/cgsdfc/ICONIP2019)
[![Build status](https://ci.appveyor.com/api/projects/status/5592iiitlxd5rtp3?svg=true)](https://ci.appveyor.com/project/cgsdfc/iconip2019)

# My Paper for ICONIP2019
This repository hosts the latex source code for my submission to the [ICONIP2019](ICONIP2019) (International Conference of Neural Information Processing). The title is *Automatic Evaluation of Generative Dialogue Systems: An Empirical Study*. This is my very first attempt to write a formal academic paper in full English. We conducted an empirical study on various metrics of the generative dialogue systems.

# Contributions
We first trained three models (LSTM, HRED, and VHRED) on three datasets (LSDSCC, OpenSubtitles, and Ubuntu) and then measured the system-level scores and example-level scores with vairous metrics. The metrics we used included word-overlap ones such BLEU and METEOR and word-embedding ones such as Vector Average and Greedy Matching.

On the example level, we observed an inter-metrics clustering based on correlations. In other words, similar metrics tend to have better correlations with one another. The results imply tuning with one set of metrics may yield a gotcha when testing on a dissimilar set of metrics.

# Links
Here are some useful links related to this project:

- The main codebase for generating and analyzing data is at [Eval](https://github.com/neural-dialogue-metrics/Eval.git).
- My graduate design done at Beihang University is at [GraduateDesign](https://github.com/cgsdfc/GraduateDesign.git), which is the origin of this work.
- This work is mainly inspired by the work of Liu et al., namely *How NOT to Evaluate Your Dialogue Systems: An Empirical Study of Unsupervised Evaluation Metrics for Dialogue Response Generation*.
- My fork of the wonderful generative models created by Serban et al. is at [HRED-VHRED](https://github.com/cgsdfc/HRED-VHRED.git). The original project can be found [here](https://github.com/julianser/hed-dlg-truncated.git).
- My fork of the wonderful but messy codebase of Li et al. is at [Neural-Dialogue-Generation](https://github.com/cgsdfc/Neural-Dialogue-Generation.git). he original project can be found [here](he original project can be found [here])

# Acknowledgement
This work is supported by Engineering Research Center of Ministry of Education for Advanced Computer Application Technology (ACAREC) of Beihang University.
