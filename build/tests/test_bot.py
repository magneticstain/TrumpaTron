#!/usr/bin/python3

"""

APP: Trumpatron
DESC: Bot.py Unit Test
CREATION_DATE: 2017-03-01

"""

# MODULES
# | Native

# | Third-Party
import pytest
import tweepy

# | Custom
import lib.bot

def testConnectToTwitterAPI_ALL_BLANKS():
    api = lib.bot.connectToTwitterAPI('', '', '', '')

    assert isinstance(api, tweepy.API)

def testSpliceTweets():
    # create test set of Status objs
    status1 = tweepy.Status()
    status1.text = 'This is a test. Testing.'

    status2 = tweepy.Status()
    status2.text = 'Test #2. Unit. Test.'

    testTweetSet = [status1, status2]

    assert lib.bot.spliceTweets(testTweetSet) == ['This is a test', 'Testing.', 'Test #2', 'Unit', 'Test.']

def testFormatTweet_BLANK_TWEET():
    with pytest.raises(ValueError):
        lib.bot.formatTweet('')

def testFormatTweet_PLAIN_TWEET():
    tweet = 'Test of normal tweet!'

    assert tweet == lib.bot.formatTweet(tweet)

def testFormatTweet_FORMATTED_TWEET():
    origTweet = 'Test of tweet that needs formatting! https://t.co/RDO6Jt2pip     '
    postFormattingTweet = 'Test of tweet that needs formatting!'

    assert postFormattingTweet == lib.bot.formatTweet(origTweet)

def testPruneTweetClauses():
    # pruning should: dedupe clauses, strip URLs, and sort the clauses by length
    testTweetClauses = ['This is a test', 'Testing.', 'This is a test, too', 'Test #2', 'Unit', 'Testing.', 'w/ URL https://t.co/qCDljfF3wN']

    prunedTweetClauses = lib.bot.pruneTweetClauses(testTweetClauses)

    assert prunedTweetClauses == ['Unit', 'w/ URL', 'Test #2', 'Testing.', 'This is a test', 'This is a test, too']

def testDivideClausesIntoSlices():
    testClauseSet = ['Unit', 'w/ URL', 'Test #2', 'Testing.', 'This is a test', 'This is a test, too']

    # test 2 and 3 clause slices
    assert lib.bot.divideClausesIntoSlices(testClauseSet, 2) == [['Unit', 'w/ URL', 'Test #2'],['Testing.', 'This is a test', 'This is a test, too']]
    assert lib.bot.divideClausesIntoSlices(testClauseSet, 3) == [['Unit', 'w/ URL'], ['Test #2', 'Testing.'], ['This is a test', 'This is a test, too']]

def testGenerateTweet():
    twoSliceClauseSet = [['Unit', 'w/ URL', 'Test #2'],['Testing.', 'This is a test', 'This is a test, too']]
    threeSliceClauseSet = [['Unit', 'w/ URL'], ['Test #2', 'Testing.'], ['This is a test', 'This is a test, too']]

    assert lib.bot.generateTweet(twoSliceClauseSet, 3).strip() != ''
    assert lib.bot.generateTweet(threeSliceClauseSet, 2).strip() != ''

def testSendTweet_BLANK_TWEET():
    with pytest.raises(ValueError):
        lib.bot.sendTweet(None, '', True)