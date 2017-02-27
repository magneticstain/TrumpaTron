#!/usr/bin/python3

"""
Trumpatron

- a bot that scrapes words and phrases from @realDonaldTrump to generate new tweets
"""

import os.path
import configparser
from tweepy import TweepError

import lib.bot

def main():
    """
    Main runtime module

    :return: void
    """

    # read in config
    configFile = 'conf/main.cfg'
    cfg = configparser.ConfigParser()
    if os.path.isfile(configFile):
        cfg.read(configFile)
    else:
        print('ERROR: config file not found :: [', configFile,']')

        exit(1)

    lgLineBreak = '#####################################################################'

    tweetSet = []
    tweetClauses = []

    # connect to twitter API and fetch tweets
    try:
        tApi = lib.bot.connectToTwitterAPI(cfg['AUTH']['consumerkey'], cfg['AUTH']['consumersecret'],
                                           cfg['AUTH']['accesstoken'], cfg['AUTH']['accesstokensecret'])

        # get public timeline tweets for user
        tweetSet = tApi.user_timeline('realdonaldtrump')
    except TweepError as err:
        print('ERROR: could not connect to Twitter API / fetch tweets ::', err)

        exit(1)

    # list and splice fetched tweets
    print('ORIGINAL TWEETS:')
    for tweet in tweetSet:
        print('TWEET:', tweet.text)

        # split tweet into list of clauses
        clauseSet = tweet.text.split('. ')

        # add clause set to master set
        tweetClauses += clauseSet

    # prune tweet clauses
    tweetClauses = lib.bot.pruneTweetClauses(tweetClauses)

    print(lgLineBreak)

    # generate new tweet from clauses
    newTweet = lib.bot.generateTweet(tweetClauses, int(cfg['GENERAL']['numclauses']))
    print('GENERATED TWEET:', newTweet)

if __name__ == '__main__':
    main()