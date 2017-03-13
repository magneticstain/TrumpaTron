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
import lib.trump


class DummyArgParse:
    """
    A dummy object that mimics the object returned from ArgParse
    """

    log_file = ''
    log_level = ''
    config_file = ''
    num_clauses = 2
    assume_yes = False
    config_check = False
    test_run = False
    daemon_mode = False
    sleep_delay = 5
    random_sleep = False


class DummyArgParse_MISSING_PARAMS:
    """
    A dummy object that mimics the object returned from ArgParse. Purposely doesn't include random variables for testing
    """

    log_file = ''
    config_file = ''
    assume_yes = False
    config_check = False
    test_run = False
    daemon_mode = False
    random_sleep = False


# FIXTURES
@pytest.fixture()
def validCliParser():
    # create dummy argparse obj
    return DummyArgParse()


@pytest.fixture()
def invalidCliParser():
    # create a purposefully invalid dummy argparse obj
    DAP = DummyArgParse_MISSING_PARAMS()

    return DAP


@pytest.fixture()
def validCfgParams():
    # generate dummy config file data
    cfg = {
        'AUTH': {
            'consumerkey': '',
            'consumersecret': '',
            'accesstoken': '',
            'accesstokensecret': ''
        },
        'GENERAL': {
            'numclauses': 2,
            'sleepdelay': 5
        },
        'LOGGING': {
            'logfile': '/var/log/trumpatron/app_test.log',
            'debuglevel': 'INFO'
        }
    }

    return cfg


@pytest.fixture()
def roCfgParams(validCfgParams):
    # generate dummy config file data w/ RO twitter API creds
    cfg = {
        'AUTH': {
            'consumerkey': '965vXNOAJBIQQK71ggCTGTyfU',
            'consumersecret': 'kPjkIqEm6MvB4xljH8Vlp0RfNlx1WzwpOZF9hPQFlQLEIY4SGA',
            'accesstoken': '836257267485921284-p0M6jYJ7P3j4KniNnrbOfLZJWTd3bTy',
            'accesstokensecret': 'waKbSHeMps0Y8pCLLAVvduwC0cMbjQuqLohaGERJvyVQT'
        },
        'GENERAL': {
            'numclauses': 2,
            'sleepdelay': 5
        },
        'LOGGING': {
            'logfile': '/var/log/trumpatron/app_test.log',
            'debuglevel': 'INFO'
        }
    }

    return cfg


def testCreateTwitterAPIConn(validCliParser, validCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, validCfgParams)

    tBot.createTwitterAPIConn()

    assert tBot.apiConn != None


def testGetTweets_INVALID_TWITTER_API_CREDS(validCliParser, validCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, validCfgParams)

    # get tweets from specified username
    # should cause a Tweepy exception
    with pytest.raises(tweepy.TweepError):
        tBot.getTweets('realdonaldtrump')


def testGetTweets_VALID_TWITTER_USERNAME(validCliParser, roCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, roCfgParams)

    # get tweets from specified username
    tBot.getTweets('realdonaldtrump')

    assert tBot.tweetSet != []


def testGetTweets_INVALID_TWITTER_USERNAME(validCliParser, roCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, roCfgParams)

    # get tweets from specified username
    # should cause a Tweepy exception
    with pytest.raises(tweepy.TweepError):
        tBot.getTweets('aiojwrrwtnnnnnaisdjfoiajsdif88892lnl132323')


def testFlushTweetData_SUCCESSFUL(validCliParser, validCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, validCfgParams)

    # set tweets, tweet clauses, and generated tweet
    # create test set of Status objs
    status1 = 'This is a test. Testing.'
    status2 = 'Test #2. Unit. Test.'
    testTweetSet = [status1, status2]
    tBot.tweetSet = testTweetSet
    tBot.tweetClauses = ['This is a test', 'Testing.', 'Test #2', 'Unit', 'Test.']
    tBot.generatedTweet = 'Test tweet!'

    # flush tweet data
    tBot.flushTweetData()

    assert tBot.tweetSet == []
    assert tBot.tweetClauses == []
    assert tBot.generatedTweet == ''


def testSpliceTweets(validCliParser, validCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, validCfgParams)

    # create test set of Status objs
    status1 = 'This is a test. Testing.'
    status2 = 'Test #2. Unit. Test.'
    testTweetSet = [status1, status2]
    tBot.tweetSet = testTweetSet

    # splice tweets
    tBot.spliceTweets()

    assert tBot.tweetClauses == ['This is a test', 'Testing.', 'Test #2', 'Unit', 'Test.']


def testFormatTweet_BLANK_TWEET(validCliParser, validCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, validCfgParams)

    with pytest.raises(ValueError):
        tBot.formatTweet('')


def testFormatTweet_PLAIN_TWEET(validCliParser, validCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, validCfgParams)

    # set tweet
    tweet = 'Test of normal tweet!'

    assert tweet == tBot.formatTweet(tweet)


def testFormatTweet_FORMATTED_TWEET(validCliParser, validCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, validCfgParams)

    # set tweet(s)
    origTweet = 'Test of tweet that needs formatting! https://t.co/RDO6Jt2pip     '
    postFormattingTweet = 'Test of tweet that needs formatting!'

    assert postFormattingTweet == tBot.formatTweet(origTweet)


def testPruneTweetClauses(validCliParser, validCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, validCfgParams)

    # pruning should: dedupe clauses, strip URLs, and sort the clauses by length
    # set clauses
    origTestTweetClauses = ['This is a test', 'Testing.', 'This is a test, too', 'Test #2', 'Unit', 'Testing.', 'w/ URL https://t.co/qCDljfF3wN']
    tBot.tweetClauses = origTestTweetClauses

    # prune clauses
    tBot.pruneTweetClauses()

    # check thaat tweetClauses post-pruning are correct
    assert tBot.tweetClauses == ['Unit', 'w/ URL', 'Test #2', 'Testing.', 'This is a test', 'This is a test, too']


def testDivideClausesIntoSlices(validCliParser, validCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, validCfgParams)

    # set clauses
    tBot.tweetClauses = ['Unit', 'w/ URL', 'Test #2', 'Testing.', 'This is a test', 'This is a test, too']

    # test 2 and 3 clause slices
    # 2 clauses
    tBot.config['numClauses'] = 2
    assert tBot.divideClausesIntoSlices() == [['Unit', 'w/ URL', 'Test #2'], ['Testing.', 'This is a test', 'This is a test, too']]

    # 3 clauses
    tBot.config['numClauses'] = 3
    assert tBot.divideClausesIntoSlices() == [['Unit', 'w/ URL'], ['Test #2', 'Testing.'], ['This is a test', 'This is a test, too']]


def testGenerateTweet_NO_TWEET_CLAUSES(validCliParser, roCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, roCfgParams)

    with pytest.raises(ValueError):
        # generate tweet
        tBot.generateTweet()


def testGenerateTweet_VALID(validCliParser, roCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, roCfgParams)

    # set clauses
    tBot.tweetClauses = ['Unit', 'w/ URL', 'Test #2', 'Testing.', 'This is a test', 'This is a test, too']

    # generate tweet
    tBot.generateTweet()

    assert tBot.generatedTweet != ''


def testSendTweet_BLANK_TWEET(validCliParser, roCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, roCfgParams)

    with pytest.raises(ValueError):
        tBot.sendTweet()


def testStartBot_TEST_RUN(validCliParser, roCfgParams):
    # create Trump instance
    tBot = lib.trump.Trump(validCliParser, roCfgParams)

    # set config to enable test run mode
    tBot.config['testRun'] = True

    # start test run
    tBot.startBot('realdonaldtrump')

