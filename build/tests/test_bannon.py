#!/usr/bin/python3

"""

APP: Trumpatron
DESC: Bot.py Unit Test
CREATION_DATE: 2017-03-01

"""

# MODULES
# | Native

# | Third-Party
import argparse
import pytest

# | Custom
import lib.bannon


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


def testInit_BLANK():
    with pytest.raises(ValueError):
        bBot = lib.bannon.Bannon(argparse.ArgumentParser(), [])


def testSetConfig_VALID(validCliParser, validCfgParams):
    # should initialize without throwing an exception
    bBot = lib.bannon.Bannon(validCliParser, validCfgParams)


def testSetConfig_INVALID(validCliParser, validCfgParams):
    # should initialize without throwing an exception using the invalid data provided

    # set invalid values
    validCliParser.assume_yes = 3
    validCliParser.config_file = True
    validCliParser.test_run = '222222222222'

    bBot = lib.bannon.Bannon(validCliParser, validCfgParams)


def testSetConfig_MISSING_PARAMS(invalidCliParser, validCfgParams):
    # should throw an attribute error
    with pytest.raises(AttributeError):
        bBot = lib.bannon.Bannon(invalidCliParser, validCfgParams)


def testInitializeLogger_VALID(validCliParser, validCfgParams):
    # create Bannon instance
    bBot = lib.bannon.Bannon(validCliParser, validCfgParams)

    # set relevant config values
    bBot.config['loggingLvl'] = 'INFO'
    bBot.config['logFile'] = '/var/log/trumpatron/app_test.log'

    # initialize logger
    bBot.initializeLogger(__name__)


def testInitializeLogger_INVALID_LOG_LVL(validCliParser, validCfgParams):
    # create Bannon instance
    bBot = lib.bannon.Bannon(validCliParser, validCfgParams)

    # set relevant config values
    bBot.config['loggingLvl'] = 'INFORM_LVL5!'
    bBot.config['logFile'] = '/var/log/trumpatron/app_test.log'

    # initialize logger
    # should throw an exception due to invalid logging lvl
    with pytest.raises(AttributeError):
        bBot.initializeLogger(__name__)


def testInitializeLogger_INVALID_LOG_FILE(validCliParser, validCfgParams):
    # create Bannon instance
    bBot = lib.bannon.Bannon(validCliParser, validCfgParams)

    # set relevant config values
    bBot.config['loggingLvl'] = 'INFO'
    bBot.config['logFile'] = '/invalid/log/file/test.log'

    # initialize logger
    # should throw an exception due to invalid log file
    with pytest.raises(FileNotFoundError):
        bBot.initializeLogger(__name__)


def testInitializeLogger_INVALID_LOG_FORMAT(validCliParser, validCfgParams):
    # create Bannon instance
    bBot = lib.bannon.Bannon(validCliParser, validCfgParams)

    # set relevant config values
    bBot.config['loggingLvl'] = 'INFO'
    bBot.config['logFile'] = '/var/log/trumpatron/app_test.log'

    # initialize logger
    # with an invalid log format, any format is accepted and the backend library is asked to handle it
    # right now, no exception should be thrown
    bBot.initializeLogger(__name__, '!!! INVALID LOG FORMAT !!!')

