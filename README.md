# Sumerian Named Entity Recognition

## Installation
```bash
$ pip3 install git+https://github.com/wwunlp/sner.git@master
```
If you are not in a [virtualenv] you may need to use `pip3` with `sudo` or
`--user`.

If you'd rather clone the repository.
```bash
$ git clone https://github.com/wwunlp/sner.git
$ cd sner/
$ pip3 install .
```

## Usage
If you used `pip3` to install `sner`, you can call `sner` from the command
line.
If you cloned the repo, you can run `python3 sner.py` from within the repo.

## Options and Arguments
* `-r` or `--run`: Run one of the following models: `dec`, `nbc`, `ner`, `rdf`,
`sgd`, or `svc`. Or one of the following routines: `analysis`, `export`, 
`export-atf`, `formatting`, `over-fit`, or `testing`.
* `-cf` or `--config`: Configuration file to use.
* `-p` or `--path`: Path to data directory.
* `-c` or `--corpus`: File name of the corpus.
* `-a` or `--attestations`: File name of the attestations.
* `-sr` or `--seed-rules`: File name of the seed rules.

* `-i` or `--iterations`: Number of iterations.
* `-mr` or `--max-rules`: Max number of rules per iterations.
* `-al` or `--alpha`: Alpha value.
* `-k` or `--k`: K value.

* `-nd` or `--norm-date`: Enable date normalization.
* `-ng` or `--norm-geo`: Enable geographical name normalization.
* `-nn` or `--norm-num`: Enable number normalization.
* `-np` or `--norm-prof`: Enable profession normalization.

`sner` will check `sner.conf` before using default value.
The `sner.conf` uses `JSON` syntax.
i.e. `--corpus corpus.csv` would be `"corpus": "corpus.csv"`.
If you want to change the hyperparameters used,
you can define them in `sner.conf`.
If your `sner.conf` is not in the root of the repository,
you can set the enviroment variable `SNER_CONF` to the path of `sner.conf`.

<p align="center">
    <img src="https://i.imgur.com/CpI851D.jpg" alt="sner">
</p>

[virtualenv]: https://virtualenv.pypa.io/en/stable/
