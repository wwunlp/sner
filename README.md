# Sumerian Named Entity Recognition
---
## Installation
```
pip3 install git+https://gitlab.cs.wwu.edu/canoym/sumerian.git@mike
```
If you are not in a [virtualenv] you may need to use `pip3` with `sudo` or
`--user`.

## Options and Arguments
* `-r` or `--run`: Run `analysis`, `formatting`, `unsupervised`, or `supervised`
routines.
* `-c` or `--corpus`: Location of corpus file.
* `-a` or `--attestations`: Location of attestations file.
* `-sr` or `--seed-rules`: Location of seed rules file.
* `-o` or `--output`: Location of output file.

* `-i` or `--iterations`: Number of iterations.
* `-mr` or `--max-rules`: Max number of rules per iterations.
* `-mf` or `--mod-freq`: Modifier of rule frequency.
* `-ms` or `--mod-str`: Modifier of rule strength.
* `-at` or `--accept-threshold`: Nam acceptance threshold.

* `-nt` or `--name-tag`: The formating for names, default is `$PN$`.
* `-nn` or `--norm-num`: Enable the normalization  of numbers.
* `-np` or `--norm-prof`: Enable the normalization of professions.
* `-lt` or `--left-tag`: Left tag of a sentence, default is `''`.
* `-rt` or `--right-tag`: Right tag of a sentence, default is `'\n'`.
* `-t` or `--tablet`: Add start of tablet line, default is `False`.
* `-m` or `--mode`: Switch between `csv` and `multiline` modes, default `csv`.

If an argument is not given, `sner` will check `sner.conf` before using the
default value. The `sner.conf` uses `JSON` syntax. i.e. `--name-tag $PN$` would
be `"name-tag": "$PN$"`.If you move `sner.conf` from the root of the
repository, you can set the enviroment variable `SNER_CONF` to the new
location of `sner.conf`.

[virtualenv]: https://virtualenv.pypa.io/en/stable/
