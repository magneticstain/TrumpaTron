#!/usr/bin/python3

"""
Bot.py

- the background logic that runs TrumpaTron
"""

from random import choice,shuffle
import re
from curses.ascii import ispunct
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
        tweetTxt = re.sub(r'[:\s]*http\S+(|\s)', ' ', tweetTxt).strip()

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

    # make sure it's punctuated
    if not ispunct(clause[-1]):
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

    # print message length for debugging
    # print('MSG LENGTH:', str(len(newTweet)))

    return newTweet

def sendTweet(api, tweet, promptBeforePublish=True):
    """
    Send new generated Tweet to Twitter API

    :param api: tweepy API connection obj
    :param tweet: tweet text to send
    :param promptBeforePublish: specifies if the user should be prompted before publishing [default: True]
    :return: int based on success/fail : -1=discarded;0=no tweet provided;1=published
    """

    if tweet:
        # send tweet to authenticated account using tweepy api connection
        if promptBeforePublish:
            shouldPublish = input('Would you like to publish this tweet? [default: Y]: ')
            shouldPublish = shouldPublish.strip().lower()
            if shouldPublish != 'y' and shouldPublish != '':
                return -1

        # attempt to publish tweet
        return api.update_status(tweet)
    else:
        raise ValueError('empty tweet text provided')
