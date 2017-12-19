# S&P500 ML & Regression Models
Project created with the goal of using SVM Convex Optimization to classify attributes of S&P 500 securities.

## Requirements
The project is written in Python 3.  It uses the following packages:

- [requests](http://docs.python-requests.org/en/master/)
- [bs4](https://www.crummy.com/software/BeautifulSoup/)
- [yahoo_finance](https://pypi.python.org/pypi/yahoo-finance/)
- [numpy](http://www.numpy.org/)

## Options
`python fetch.py -h` prints:
```
usage: fetch.py [-h] [-d] [-l] [-s SYM] [-S SYM]

optional arguments:
  -h, --help         show this help message and exit
  -d, --data         save current S&P data to {TODAY}.csv
  -l, --list         list S&P Companies with sectors
  -s SYM, --sym SYM  print all data for symbol "SYM"
  -S SYM, --SYM SYM  print filtered data for symbol "SYM"

```

