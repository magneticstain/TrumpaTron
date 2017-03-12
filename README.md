# TrumpaTron
[![Documentation Status](https://readthedocs.org/projects/trumpatron/badge/?version=latest)](http://trumpatron.readthedocs.io/en/latest/?badge=latest) [![Requirements Status](https://requires.io/github/magneticstain/TrumpaTron/requirements.svg?branch=master)](https://requires.io/github/magneticstain/TrumpaTron/requirements/?branch=master) [![Build Status](https://travis-ci.org/magneticstain/TrumpaTron.svg?branch=master)](https://travis-ci.org/magneticstain/TrumpaTron) [![Coverage Status](https://coveralls.io/repos/github/magneticstain/TrumpaTron/badge.svg?branch=master)](https://coveralls.io/github/magneticstain/TrumpaTron?branch=master) [![Stories in Ready](https://badge.waffle.io/magneticstain/TrumpaTron.svg?label=ready&title=Ready)](http://waffle.io/magneticstain/TrumpaTron)

A Python bot designed to create original tweets from the most recent @realdonaldtrump tweets.

[@trumpatron1](https://twitter.com/trumpatron1)

## What is this?
The @trumpatron1 Twitter account is a mock account ran by this bot. At a regular interval, this bot runs, fetches 
the most recent @realdonaldtrump tweets, and mixes statements from those tweets together to create a new, original Tweet.

After being generated, it's tweeted to the @trumpatron1 account.

## Requirements
### OS
* Debian 6+
* Ubuntu 14.04+
* CentOS 6+

### Software
* python 3.3+
* pip3
* setuptools (if installing libraries)

## Installation
To install TrumpaTron locally, follow these steps:

1. Download and unzip the latest stable release from GitHub:
```bash
bot@trumpatron1:~$ wget https://github.com/magneticstain/TrumpaTron/archive/master.zip
bot@trumpatron1:~$ unzip master.zip 
```

2. Install application requirements:
```bash
bot@trumpatron1:~/TrumpaTron-master$ pip3 install -r requirements.txt
```

3. (Opt.) If you plan on utilizing the trumpatron library in your own applications (i.e. want to import the libraries in your own python scripts),
run the `setup.py` file now:
```bash
bot@trumpatron1:~/TrumpaTron-master$ sudo ./setup.py install
```

4. Move files to a static directory:
```bash
bot@trumpatron1:~/TrumpaTron-master$ sudo mkdir /opt/trumpatron && sudo cp -rf ./* /opt/trumpatron/
```

5. Create log directory:
```bash
sysadmin@nyc3ttrontesting01:/opt/trumpatron$ sudo mkdir /var/log/trumpatron/
```

TrumpaTron is now installed and ready to use.

## Usage
Nothing is easier than running this application.  It's the greatest syntax ever, believe me!
```bash
sysadmin@nyc3ttrontesting01:~/TrumpaTron-master$ /opt/trumpatron/trumpatron.py -h
usage: trumpatron.py [-h] [-f LOG_FILE] [-l LOG_LEVEL] [-c CONFIG_FILE]
                     [-n NUM_CLAUSES] [-y] [-k] [-t] [-d] [-s SLEEP_DELAY]
                     [-r]

A Python bot designed to create original tweets from the most recent
@realdonaldtrump tweets.

optional arguments:
  -h, --help            show this help message and exit
  -f LOG_FILE, --log-file LOG_FILE
                        File to write application logs to
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Minimum log severity level to log to file
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Configuration file to be used
  -n NUM_CLAUSES, --num-clauses NUM_CLAUSES
                        Number of clauses to use in Tweet
  -y, --assume-yes      Assume YES for all prompts
  -k, --config-check    Try running TrumpaTron up to after the configs are
                        read in
  -t, --test-run        Run TrumpaTron in test mode (generate tweet w/o
                        publishing)
  -d, --daemon-mode     Run TrumpaTron in daemon mode (run persistently)
  -s SLEEP_DELAY, --sleep-delay SLEEP_DELAY
                        Time to wait in between runs (used w/ -d|--daemon-
                        mode)
  -r, --random-sleep    Sleep for a random delay, with the value for
                        -s|--sleep-delay being the max sleep time

``` 

### Examples
Perform a configuration check on the primary config:
```bash
bot@trumpatron1:/opt/trumpatron$ ./trumpatron.py -c conf/primary.cfg -k
```

Perform a test run using the default config:
```bash
bot@trumpatron1:/opt/trumpatron$ ./trumpatron.py -t
```

Use tertiary config file:
```bash
bot@trumpatron1:/opt/trumpatron$ ./trumpatron.py -c conf/tertiary.cfg
```

Assume yes to all prompts using the default settings (automated tweeting):
```bash
bot@trumpatron1:/opt/trumpatron$ ./trumpatron.py -y
```

Use the settings in `conf/secondary.cfg`, generate a tweet with three clauses, and assume yes for all prompts:
```bash
bot@trumpatron1:/opt/trumpatron$ ./trumpatron.py -c conf/secondary.cfg -n 3 -y
```

Run trumpatron.py in test daemon mode using specific config and log file/level:
```bash
bot@trumpatron1:/opt/trumpatron$ ./trumpatron.py -c /opt/trumpatron/conf/specific.cfg -d -t -f /home/testing/ttron_test.log -l DEBUG
```

Run trumpatron.py in test daemon mode, ensuring any log messages WARN level and above are written, and overriding config values for number of clauses and sleep delay (30s):
```bash
bot@trumpatron1:/opt/trumpatron$ ./trumpatron.py -c /opt/trumpatron/conf/specific.cfg -n 3 -d -t -s 30 -l WARN
```

Run trumpatron.py in daemon mode using specific config file, with random sleep delay (max 120s):
```bash
bot@trumpatron1:/opt/trumpatron$ ./trumpatron.py -c /opt/trumpatron/conf/specific.cfg -d -s 120 -r
```

### Customizing Application
A configuration file is used by the application for various settings, mostly related to Twitter API authentication.
It's located at `conf/main.cfg`. Open the file to take a look at the various settings and customize them to your liking.