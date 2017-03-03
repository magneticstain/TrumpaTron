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
