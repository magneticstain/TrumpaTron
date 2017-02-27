#!/usr/bin/python3

"""
Bot.py

- the background logic that runs TrumpaTron
"""

from random import choice,shuffle
import tweepy

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

def pruneTweetClauses(tweetClauseSet):
    """
    Prune and deduplicate sets of Tweet clauses

    :param tweetClauseSet: list of clauses generated from tweets
    :return: pruned list of tweet clauses
    """

    # dedupe clause set
    prunedTweetClauseSet = list(set(tweetClauseSet))
    prunedTweetClauseSet.sort(key=tweetClauseSet.index)

    # sort list of clauses by length
    prunedTweetClauseSet.sort(key=len)

    return prunedTweetClauseSet

def divideClausesIntoSlices(clauses, numSlices):
    """

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

    :param clauses: list of clauses to select from
    :return: clause from given list
    """

    return choice(clauses)

def generateTweet(tweetClauses, numClausesToUse=3):
    """
    Generates a unique tweet from a given set of sentence clauses

    :param tweetClauses: list of clauses previously generated from tweets
    :param numClausesToUse: the number of clauses the new tweet should contain (default: 3)
    :return: new tweet in string format
    """

    newTweet = ''
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

    # concatonate tweet
    newTweet = longestClause + '. ' + middleClauses + '. ' + shortestClause

    return newTweet