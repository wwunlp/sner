# Contributing to Sumerian Named Entity Recongnition
---
To start contributing, you can install the project by
```
git clone https://gitlab.cs.wwu.edu/canoym/sumerian.git
cd sumerian/
pip3 install .'[develop]'
```
Please follow the [Google Python Style Guide].

The project is organized into `classes`, `models`, `scripts`, and `tests`.
Class files should probably go into `classes`. The main file for a model
should go into `models`. General scripts should go into `scripts`, and
scripts for models should into a subdirectory of the model in `scripts`.
Test files should go into `tests`.

[Google Python Style Guide]: https://google.github.io/styleguide/pyguide.html
