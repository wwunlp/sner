# Sumerian Named Entity Recognition
---
## Installation
```
pip3 install git+https://gitlab.cs.wwu.edu/canoym/sumerian.git@mike
```
If you are not in a [virtualenv] you may need to use `pip3` with `sudo` or
`--user`.

If you'd rather not use `pip3`, you can clone the repo.
```
git clone -b mike https://gitlab.cs.wwu.edu/canoym/sumerian.git
pip3 install editdistance
```

## Usage
If you used `pip3` to install `sner`, you can call `sner` from the command
line. If you cloned the repo, you can run `python3 sner.py` from within the 
repo.

## Options and Arguments
* `-r` or `--run`: Run `analysis`, `formatting`, `unsupervised-old`, or `ner`
routines.
* `-c` or `--corpus`: Location of corpus file.
* `-a` or `--attestations`: Location of attestations file.
* `-sr` or `--seed-rules`: Location of seed rules file.
* `-o` or `--output`: Location of output file.

* `-i` or `--iterations`: Number of iterations.
* `-mr` or `--max-rules`: Max number of rules per iterations.
* `-mf` or `--mod-freq`: Modifier of rule frequency.
* `-ms` or `--mod-str`: Modifier of rule strength.
* `-at` or `--accept-threshold`: Name acceptance threshold.
* `-al` or `--alpha`: Alpha value.
* `-k` or `--k`: K value.

* `-nn` or `--norm-num`: Enable the normalization  of numbers.
* `-np` or `--norm-prof`: Enable the normalization of professions.
* `-ng` or `--norm-geo`: Enable the normalization of geographic names.

If an argument is not given, `sner` will check `sner.conf` before using the
default value. The `sner.conf` uses `JSON` syntax. i.e. `--name-tag $PN$` would
be `"name-tag": "$PN$"`.If you move `sner.conf` from the root of the
repository, you can set the enviroment variable `SNER_CONF` to the new
location of `sner.conf`.

[virtualenv]: https://virtualenv.pypa.io/en/stable/
