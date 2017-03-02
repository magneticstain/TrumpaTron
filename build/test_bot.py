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

# | Custom
import lib.bot

def testConnectToTwitterAPI_FAIL_ALL_BLANKS():
    assert lib.bot.connectToTwitterAPI('', '', '', '') == None