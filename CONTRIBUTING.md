# Contributing to Sumerian Named Entity Recongnition
---
To start contributing, you can install the project by
```
git clone https://github.com/wwunlp/sner.git
cd sner/
pip3 install .'[develop]'
```
Please follow the [Google Python Style Guide].

The project is organized into `classes`, `docs`, `models`, `scripts`, and
`tests`.

* Class files should probably go into `classes`.
* The main file fora model should go into `models`.
* General scripts should go into `scripts`, and scripts for models should
into a sub-directory of the model in `scripts`.
* Test files should go into `tests`.
* Compile docs with `sphinx`, and post the html files to `docs/`.

If you're parsing `.atf` files, please look at the [ATF reference].

[Google Python Style Guide]: https://google.github.io/styleguide/pyguide.html
[ATF reference]: https://github.com/wwunlp/sner/blob/master/atf_reference.md