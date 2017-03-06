#!/usr/bin/python3

"""

APP: TrumpaTron
DESC: A Python bot designed to create original tweets from the most recent @realdonaldtrump tweets.
AUTHOR: @magneticstain
CREATION_DATE: 2017-02-27

"""

# MODULES
# | Native
import argparse
import configparser
from os import path

# | Third-Party
from tweepy import TweepError

# | Custom
import lib.trump

# METADATA
__author__ = 'Joshua Carlson-Purcell'
__copyright__ = 'Copyright 2017, CarlsoNet'
__license__ = 'MIT'
__version__ = '1.0.1'
__maintainer__ = 'Joshua Carlson-Purcell'
__email__ = 'jcarlson@carlso.net'
__status__ = 'Production'


def parseCliArgs():
    """
    Parse CLI arguments

    :return: dictionary of arg key-val's
    """

    # set CLI arguments
    cliParser = argparse.ArgumentParser(description='A Python bot designed to create original tweets from the most recent @realdonaldtrump tweets.')
    cliParser.add_argument('-f', '--log-file', help='File to write application logs to')
    cliParser.add_argument('-l', '--log-level', help='Minimum log severity level to log to file', default='INFO')
    cliParser.add_argument('-c', '--config-file', help='Configuration file to be used',default='conf/main.cfg')
    cliParser.add_argument('-n', '--num-clauses', help='Number of clauses to use in Tweet', default=0, type=int)
    cliParser.add_argument('-y', '--assume-yes', action='store_true', help='Assume YES for all prompts', default=False)
    cliParser.add_argument('-k', '--config-check', action='store_true', help='Try running TrumpaTron up to after the configs are read in', default=False)
    cliParser.add_argument('-t', '--test-run', action='store_true', help='Run TrumpaTron in test mode (generate tweet w/o publishing)', default=False)
    cliParser.add_argument('-d', '--daemon-mode', action='store_true', help='Run TrumpaTron in daemon mode (run persistently)', default=False)
    cliParser.add_argument('-s', '--sleep-delay', help='Time to wait in between runs (used w/ -d|--daemon-mode)', default=1, type=int)
    cliParser.add_argument('-r', '--random-sleep', action='store_true', help='Sleep for a random delay, with the value for -s|--sleep-delay being the max sleep time', default=False)

    # read in args
    return cliParser.parse_args()


def parseConfigFile(configFile):
    """
    Parse App Configuration from File

    :param configFile: filename of configuration file to read in
    :return: ConfigParser() obj
    """

    # create CP object
    cfg = configparser.ConfigParser()

    # check if config file is readable
    if path.isfile(configFile):
        # ingest ad return configuration
        cfg.read(configFile)

        return(cfg)
    else:
        print('[CRIT] config file not found :: [', configFile, ']')

        exit(1)


def main():
    """
    Main runtime module

    :return: void
    """

    # parse CLI arguments
    cliParams = parseCliArgs()

    # read in config file
    cfg = None
    try:
        cfg = parseConfigFile(cliParams.config_file)
    except configparser.Error as err:
        print('[CRIT] could not parse config file :: [ ', cliParams.config_file, ' ]\nDETAILS:\n', err.message, sep="")

        exit(1)

    # create base object(s)
    trump = None
    try:
        trump = lib.trump.Trump(cliParams, cfg)
    except TweepError as err:
        print('[CRIT] could not connect to Twitter API ::', str(err.response), '::', str(err.reason))

        exit(1)

    # stop here if running in config-test mode
    if trump.config['configChk']:
        trump.logger.info('configuration check SUCCESSFUL, exiting...')

        exit()

    # start trump bot
    trump.startBot('realdonaldtrump')


if __name__ == '__main__':
    main()
