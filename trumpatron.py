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
from os import path, fork
import time
from random import randint

# | Third-Party
from tweepy import TweepError

# | Custom
import lib.bot

# METADATA
__author__ = 'Joshua Carlson-Purcell'
__copyright__ = 'Copyright 2017, CarlsoNet'
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Joshua Carlson-Purcell'
__email__ = 'jcarlson@carlso.net'
__status__ = 'Production'

def parseCliArgs():
    """
    Parse CLI arguments

    :return: dictionary of arg key-val's
    """

    # set arguments
    cliParser = argparse.ArgumentParser(description='A Python bot designed to create original tweets from the most recent @realdonaldtrump tweets.')
    cliParser.add_argument('-c', '--config', help='Configuration file to be used',default='conf/main.cfg')
    cliParser.add_argument('-n', '--num-clauses', help='Number of clauses to use in Tweet', default=0)
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
        print('ERROR: config file not found :: [', configFile, ']')

        exit(1)


def main():
    """
    Main runtime module

    :return: void
    """

    lgLineBreak = '#####################################################################'

    # parse CLI arguments
    cliParams = parseCliArgs()

    # start while loop for daemon mode
    while True:
        # read in config file
        configFile = cliParams.config
        cfg = None
        try:
            cfg = parseConfigFile(configFile)
        except configparser.Error as err:
            print('ERROR: could not parse config file :: [ ', configFile,' ]\nDETAILS:\n',err, sep='')

            exit(1)

        # check for cli params that would overwrite the config file values
        # number of clauses to be used in tweet
        if cliParams.num_clauses:
            numClauses = cliParams.num_clauses
        else:
            # use config value
            numClauses = cfg['GENERAL']['numclauses']
        # sleep delay
        if cliParams.sleep_delay != 1:
            sleepDelay = cliParams.sleep_delay
        else:
            # use config value if available, or the default if it isn't
            if cfg['GENERAL']['sleepdelay']:
                sleepDelay = int(cfg['GENERAL']['sleepdelay'])
            else:
                sleepDelay = 1

        # stop here if running in config-test mode
        if cliParams.config_check:
            print('[INFO] configuration check SUCCESSFUL, exiting...')

            exit()

        # connect to twitter API and fetch tweets
        tApi = None
        tweetSet = []
        try:
            tApi = lib.bot.connectToTwitterAPI(cfg['AUTH']['consumerkey'], cfg['AUTH']['consumersecret'],
                                               cfg['AUTH']['accesstoken'], cfg['AUTH']['accesstokensecret'])

            # get public timeline tweets for user
            tweetSet = tApi.user_timeline('realdonaldtrump')
        except TweepError as err:
            print('ERROR: could not connect to Twitter API / fetch tweets ::', err)

            exit(1)

        # splice tweet into clauses
        tweetClauses = lib.bot.spliceTweets(tweetSet)

        # prune tweet clauses
        tweetClauses = lib.bot.pruneTweetClauses(tweetClauses)

        print(lgLineBreak)

        # generate new tweet from clauses
        newTweet = ''
        numTweetGenIterations = 0
        maxTweetGenIterations = 100
        while len(newTweet) == 0 or 140 < len(newTweet):
            # tweet msg is too long, try regenerating
            newTweet = lib.bot.generateTweet(tweetClauses, int(numClauses))

            # increase generation count
            numTweetGenIterations += 1

            # check if iteration max has been hit
            if maxTweetGenIterations < numTweetGenIterations:
                print('[ERROR] Maximum number of Tweet generation attempts (', maxTweetGenIterations, ') has been reached. '
                        'Try reducing the number of clauses.')

                exit(2)

        print('GENERATED TWEET:', newTweet)

        # publish tweet
        try:
            # check if this is a test run
            if not cliParams.test_run:
                tweetPubRslt = lib.bot.sendTweet(tApi, newTweet, cliParams.assume_yes)
                print('')
                if tweetPubRslt == -1:
                    print('[INFO] Tweet not published, discarding...')
                elif not tweetPubRslt:
                    print('[ERROR] could not publish tweet for an unknown reason :(')
                else:
                    print('TWEET PUBLISHED SUCCESSFULLY! [ ID:',tweetPubRslt.id,']')
            else:
                print('[INFO] application in test mode, exiting w/o sending tweet')
        except ValueError as valErr:
            print('ERROR: invalid value provided for tweet ::', newTweet, '::', valErr)
        except TweepError as err:
            print('ERROR: could not publish tweet ::', newTweet,'::', err)

            exit(1)

        # check if we're in daemon mode and should restart loop or not
        if not cliParams.daemon_mode:
            break
        else:
            # start by forking to a bg process
            # if fork():
                # fork successful, exit main process
                # exit()

            # in daemon mode, sleep for n second(s), where 1 <= n
            # check if random delay has been requested
            if cliParams.random_sleep:
                sleepDelay = randint(1, sleepDelay)

            # perform sleep
            time.sleep(sleepDelay)


if __name__ == '__main__':
    main()
