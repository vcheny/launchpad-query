# launchpad-query
This is a small script to query Launchpad for Contrail bugs and print out related info into csv format. One of its uses is to collect some statistics for bugs contains certain tags.

# Usage
```
[cheny-mbp:~/Work/github/launchpad-query]$ ./lpq.py -h
usage: lpq [-h] [-a AFTER] [-b BEFORE] [--open_only] [--closed_only] tag

Script to query Contrail related bugs in launchpad

positional arguments:
  tag                   List launchpad matching given tags

optional arguments:
  -h, --help            show this help message and exit
  -a AFTER, --after AFTER
                        List launchpad created since given time e.g.
                        2018-03-19
  -b BEFORE, --before BEFORE
                        List launchpad created before given time e.g.
                        2018-03-19
  --open_only           Only list LPs in open state
  --closed_only         Only list LPs not in open state
```
