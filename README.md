ACM Keyword Collector
===========

Python script to automatically collect keywords from research papers, from ACM digital library. This tool is built on top of [acmdownload](https://github.com/niklasekstrom/acmdownload)

## WARNING:
This tool issues many post request to ACM Digital Library; at some point the dl.acm.org site will notice this and temporarily block your IP.

# Package dependence:
* BibtexParser
* pandas

# Installing and running:

* Download and install the latest release of [Python 3](https://www.python.org/downloads/).
* Download bibtex from [dblp](https://dblp.org/) with the corresponding year and conference name and save it in ```conferences/{CONFERENCE}/{CONFERENCE}{YEAR}.bib```, e.g. ```conferences/cvpr/cvpr2021.bib```
* Install all dependent packages.

Run using the command line: 
```python3 bibparser.py -p [list of conferences] -y [list of years]```


# Searching keyword of a paper


The query engine will read doi(s) from the bib file given in ```conferences/{CONFERENCE}/{CONFERENCE}{YEAR}.bib``` file and query its full bibtex from [dl.acm.org](dl.acm.org).
Then it count the number of papers that have the target word(s) in either keyword or abstract section, and print it in pandas string format.
