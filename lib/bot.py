#!/usr/bin/python3

"""
Bot.py

APP: TrumpaTron
DESC: A Python bot designed to create original tweets from the most recent @realdonaldtrump tweets.
AUTHOR: @magneticstain
CREATION_DATE: 2017-02-27

"""

# MODULES
# | Native
from random import choice,shuffle
from curses.ascii import ispunct,isdigit
import re

# | Third-Party
import tweepy

# | Custom

# METADATA
__author__ = 'Joshua Carlson-Purcell'
__copyright__ = 'Copyright 2017, CarlsoNet'
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Joshua Carlson-Purcell'
__email__ = 'jcarlson@carlso.net'
__status__ = 'Production'


def connectToTwitterAPI(consumerKey, consumerSecret, accessToken, accessTokenSecret):
    """
    Authenticate to Twitter API using Tweepy library

    :param consumerKey: application consumer Key (via Twitter, dev-side)
    :param consumerSecret: application consumer secret (via Twitter, dev-side) [CONFIDENTIAL]
    :param accessToken: user access token (via Twitter, user-side)
    :param accessTokenSecret: user access token secret (via Twitter, user-side) [CONFIDENTIAL]
    :return: tweepy API object (connection to twitter API)
    """

    # auth to twitter using oAuth
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    # connect to twitter API
    api = tweepy.API(auth)

    return api


def spliceTweets(tweetSet):
    """
    Splice a set of tweets into a list of individual clauses

    :param tweetSet: list of Tweepy tweet objects
    :return: list of post-spliced tweet clauses
    """

    tweetClauses = []

    # list and splice fetched tweets
    print('ORIGINAL TWEETS:')
    for tweet in tweetSet:
        print('TWEET:', tweet.text)

        # split tweet into list of clauses
        clauseSet = tweet.text.split('. ')

        # add clause set to master set
        tweetClauses += clauseSet

    return tweetClauses


def formatTweet(tweetTxt):
    """
    Format tweet text, e.g. remove urls, strip excess whitespace, add ending punctuation, etc

    :param tweetTxt: raw text of tweet
    :return: string - filtered tweet text
    """

    if not tweetTxt:
        raise ValueError('ERROR: blank tweet text provided')
    else:
        # filter out URLs and strip surrounding whitespace
        tweetTxt = re.sub(r'[:\s]*http\S+(|\s)', '', tweetTxt).strip()

        # check if ll text has been stripped
        if not tweetTxt:
            # set to default tweet clause
            tweetTxt = '<3'

    return tweetTxt


def pruneTweetClauses(tweetClauseSet):
    """
    Prune and deduplicate sets of Tweet clauses

    :param tweetClauseSet: list of clauses generated from tweets
    :return: pruned list of tweet clauses
    """

    # dedupe clause set
    prunedTweetClauseSet = list(set(tweetClauseSet))
    prunedTweetClauseSet.sort(key=tweetClauseSet.index)

    # filter tweet text
    for i in range(0, len(prunedTweetClauseSet)):
        prunedTweetClauseSet[i] = formatTweet(prunedTweetClauseSet[i])

    # sort list of clauses by length
    prunedTweetClauseSet.sort(key=len)

    return prunedTweetClauseSet


def divideClausesIntoSlices(clauses, numSlices):
    """
    Split a given set of clauses into N number of slices, where n = numSlices

    :param clauses: tweet clauses to divide
    :param numSlices: number of slices to divide clauses into
    :return: a list containing all clause slices
    """

    slices = []

    # divide the set of tweet clauses into n slices, where n = numClausesToUse
    numClausesInSlice = int(len(clauses) / numSlices)
    # iterate through slices
    for i in range(0, numSlices):
        slices.append([])

        # fill up slice with values
        startTweetClauseIdx = i * numClausesInSlice
        endTweetClauseIdx = startTweetClauseIdx + numClausesInSlice
        slices[i] = clauses[startTweetClauseIdx:endTweetClauseIdx]

    return slices


def getRandomTweetClause(clauses):
    """
    Choose a random clause from a set of tweet clauses

    :param clauses: list of clauses to select from
    :return: clause from given list
    """

    # make selection
    clause = choice(clauses)

    # capitalize the first letter in the clause
    clause = clause[0].capitalize() + clause[1:]

    # make sure it's punctuated or the default clause
    if not ispunct(clause[-1]) and clause != '<3':
        clause += '!'

    return clause


def generateTweet(tweetClauses, numClausesToUse=3):
    """
    Generates a unique tweet from a given set of sentence clauses

    :param tweetClauses: list of clauses previously generated from tweets
    :param numClausesToUse: the number of clauses the new tweet should contain (default: 3)
    :return: new tweet in string format
    """

    slices = divideClausesIntoSlices(tweetClauses, numClausesToUse)

    # generate tweet from clause slices
    # longest slice clause is always first, shortest is last, and the middle are chosen at random for n - 2 clausesToUse
    longestClause = getRandomTweetClause(slices[-1])
    slices.pop(-1)

    shortestClause = getRandomTweetClause(slices[0])
    slices.pop(0)

    # generate middle clauses if any slices are still left
    middleClauses = ''
    if slices:
        # shuffle middle slices
        shuffle(slices)
        for clauseSlice in slices:
            currentClause = getRandomTweetClause(clauseSlice)
            middleClauses += currentClause

        # cap w/ period
        middleClauses += '. '

    # concatonate tweet
    newTweet = longestClause + ' ' + middleClauses + shortestClause

    return newTweet


def sendTweet(api, tweet, skipPromptBeforePublish=False):
    """
    Send new generated Tweet to Twitter API

    :param api: tweepy API connection obj
    :param tweet: tweet text to send
    :param skipPromptBeforePublish: specifies if we should prompt the user to publish (FALSE) or assume yes (TRUE)
    :return: int based on success/fail : -1=discarded;0=no tweet provided;1=published
    """

    if tweet:
        # send tweet to authenticated account using tweepy api connection
        if not skipPromptBeforePublish:
            shouldPublish = input('=> Would you like to publish this tweet? [y/N]: ')
            shouldPublish = shouldPublish.strip().lower()
            if (shouldPublish != 'y' and shouldPublish != 'yes') or not shouldPublish:
                return -1

        # attempt to publish tweet
        return api.update_status(tweet)
    else:
        raise ValueError('empty tweet text provided')

