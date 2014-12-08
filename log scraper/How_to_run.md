

This log scrapper is written in python and tested on:
  python 2.6
  python 2.7


Start by creating a [virtualenv][1] in a clone of the repository


    virtualenv -p $(which python2.6) .venv
    source .venv/bin/activate

The easiest way to run the tests is with `nosetests`. You need to install it
into the virtual environment, even if it is installed system-wide.

    pip install -r test/requirements.txt
    nosetests


How to run the scrapper. This scrapper was created with the usage assumption
of running on a system that had [cat][2] installed.


If you file is named: 'puppet_access_ssl.log' the command will be:

    cat 'puppet_access_ssl.log' | python logscrapper/logscrapper.py

The output will look something similar to:

    Total production
    total prod access: 6
    total prod failure: 0
    ============
    Total failures:  6
    ============
    Total dev
    Total request for dev: 9
    Dev access breakdown by IP:
        10.101.3.205: 1
        10.34.89.138: 1
        10.80.174.42: 1
        10.80.58.67: 1
        10.39.111.203: 1
        10.80.146.96: 1
        10.204.150.156: 1
        10.204.211.99: 1
        10.114.199.41: 1

[1]: http://www.virtualenv.org/en/latest/
[2]: http://linux.die.net/man/1/cat
