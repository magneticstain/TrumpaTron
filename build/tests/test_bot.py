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

def testSendTweet_BLANK_TWEET():
    with pytest.raises(ValueError):
        lib.bot.sendTweet(None, '', True)