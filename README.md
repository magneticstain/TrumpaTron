# TrumpaTron
[![Stories in Ready](https://badge.waffle.io/magneticstain/TrumpaTron.svg?label=ready&title=Ready)](http://waffle.io/magneticstain/TrumpaTron) [![Build Status](https://travis-ci.org/magneticstain/TrumpaTron.svg?branch=master)](https://travis-ci.org/magneticstain/TrumpaTron) [![Coverage Status](https://coveralls.io/repos/github/magneticstain/TrumpaTron/badge.svg?branch=master)](https://coveralls.io/github/magneticstain/TrumpaTron?branch=master) [![Documentation Status](https://readthedocs.org/projects/trumpatron/badge/?version=latest)](http://trumpatron.readthedocs.io/en/latest/?badge=latest)

A Python bot designed to create original tweets from the most recent @realdonaldtrump tweets.

[@trumpatron1](https://twitter.com/trumpatron1)

## What is this?
The @trumpatron1 Twitter account is a mock account ran by this bot. At a regular interval, this bot runs, fetches 
the most recent @realdonaldtrump tweets, and mixes statements from those tweets together to create a new, original Tweet.

After being generated, it's tweeted to the @trumpatron1 account.

## Usage
Nothing is easier than running this application.  It's the greatest syntax ever, believe me!
```bash
bot@trumpatron1 ~ $ ./trumpatron.py -h
usage: trumpatron.py [-h] [-c CONFIG] [-n NUM_CLAUSES] [-y]

A Python bot designed to create original tweets from the most recent @realdonaldtrump tweets.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration file to be used
  -n NUM_CLAUSES, --num-clauses NUM_CLAUSES
                        Number of clauses to use in Tweet
  -y, --assume-yes      Assume YES for all prompts
  
``` 

### Examples
Use tertiary config file:
```bash
bot@trumpatron1 ~ $ ./trumpatron.py -c conf/tertiary.cfg
```

Assume yes to all prompts using the default settings (automated tweeting):
```bash
bot@trumpatron1 ~ $ ./trumpatron.py -y
```

Use the settings in `conf/secondary.cfg`, generate a tweet with three clauses, and assume yes for all prompts:
```bash
bot@trumpatron1 ~ $ ./trumpatron.py -c conf/secondary.cfg -n 3 -y
```

### Customizing Application
A configuration file is used by the application for various settings, mostly related to Twitter API authentication.
It's located at `conf/main.cfg`. Open the file to take a look at the various settings and customize them to your liking.