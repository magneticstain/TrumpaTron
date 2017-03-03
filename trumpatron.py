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
import os.path

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
    # cliParser.add_argument('-s', '--num-clauses', help='Number of clauses to use in Tweet', default=0)
    cliParser.add_argument('-y', '--assume-yes', action='store_true', help='Assume YES for all prompts', default=False)
    cliParser.add_argument('-k', '--config-check', action='store_true', help='Try running TrumpaTron up to after the configs are read in', default=False)
    cliParser.add_argument('-t', '--test-run', action='store_true', help='Run TrumpaTron in test mode (generate tweet w/o publishing)', default=False)

    # read in args
    return cliParser.parse_args()

def main():
    """
    Main runtime module

    :return: void
    """

    lgLineBreak = '#####################################################################'

    # parse CLI arguments
    cliParams = parseCliArgs()

    # read in config file
    configFile = cliParams.config
    cfg = None
    try:
        cfg = configparser.ConfigParser()
        if os.path.isfile(configFile):
            cfg.read(configFile)
        else:
            print('ERROR: config file not found :: [', configFile,']')

            exit(1)
    except configparser.Error as err:
        print('ERROR: could not parse config file :: [ ', configFile,' ]\nDETAILS:\n',err, sep='')

        exit(1)

    # stop here if running in test mode
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

    # check if the number of clauses to be used in tweet was provided via CLI param; it overrides the config file val
    if cliParams.num_clauses:
        numClauses = cliParams.num_clauses
    else:
        # use config value
        numClauses = cfg['GENERAL']['numclauses']

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

if __name__ == '__main__':
    main()
