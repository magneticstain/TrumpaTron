#!/usr/bin/python3

"""

APP: TrumpaTron
DESC: A Python bot designed to create original tweets from the most recent @realdonaldtrump tweets.
AUTHOR: @magneticstain
CREATION_DATE: 2017-02-27

"""

# MODULES
# | Native
import os.path
import configparser

# | Third-Party
from tweepy import TweepError

# | Custom
import lib.bot

# METADATA
__author__ = 'Joshua Carlson-Purcell'
__copyright__ = 'Copyright 2017, CarlsoNet'
__license__ = 'MIT'
__version__ = '1.0.0-alpha'
__maintainer__ = 'Joshua Carlson-Purcell'
__email__ = 'jcarlson@carlso.net'
__status__ = 'Development'

def main():
    """
    Main runtime module

    :return: void
    """

    lgLineBreak = '#####################################################################'

    # read in config
    try:
        configFile = 'conf/main.cfg'
        cfg = configparser.ConfigParser()
        if os.path.isfile(configFile):
            cfg.read(configFile)
        else:
            print('ERROR: config file not found :: [', configFile,']')

            exit(1)
    except configparser.Error as err:
        print('ERROR: could not parse config file :: [ ', configFile,' ]\nDETAILS:\n',err, sep='')

        exit(1)

    # connect to twitter API and fetch tweets
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
    while len(newTweet) == 0 or 140 < len(newTweet):
        # tweet msg is too long, try regenerating
        newTweet = lib.bot.generateTweet(tweetClauses, int(cfg['GENERAL']['numclauses']))
    print('GENERATED TWEET:', newTweet)

    # publish tweet
    try:
        if lib.bot.sendTweet(tApi, newTweet):
            print('TWEET PUBLISHED SUCCESSFULLY!')
        else:
            print('ERROR: empty tweet sent')

            exit(1)
    except TweepError as err:
        print('ERROR: could not publish tweet ::', newTweet,'::', err)

        exit(1)

if __name__ == '__main__':
    main()