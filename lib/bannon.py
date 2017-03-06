#!/usr/bin/python3

"""
Bannon.py

APP: Trumpatron
DESC: The base class that acts as a controller for the bot
CREATION_DATE: 2017-03-05

"""

# MODULES
# | Native
import logging

# | Third-Party

# | Custom

# METADATA
__author__ = 'Joshua Carlson-Purcell'
__copyright__ = 'Copyright 2017, CarlsoNet'
__license__ = 'MIT'
__version__ = '1.0.1'
__maintainer__ = 'Joshua Carlson-Purcell'
__email__ = 'jcarlson@carlso.net'
__status__ = 'Production'


class Bannon():
    """
    Bannon.py

    The base model/controller class for TrumpaTron
    """

    config = []
    logger = None

    def __init__(self, cliParams, configParams):
        # set app configs
        self.setConfig(cliParams, configParams)

        # start logging
        self.initializeLogger(__name__)

    def setConfig(self, cliParameters, configFileParameters):
        """
        Deduplicate conflicting app settings using override rules, and set the master app configuration

        :param cliParameters: cliParser arguments
        :param configFileParameters: configParser cfgs
        :return: dictionary of app config settings
        """

        if not cliParameters or not configFileParameters:
            raise ValueError('data is missing in order to set master config :: CLI : [', cliParameters,
                             '] :: CFG_FILE : [', configFileParameters, ']')
        else:
            # set cli-only and config-file-only params
            masterCfg = {
                'configChk': cliParameters.config_check,
                'testRun': cliParameters.test_run,
                'assumeYes': cliParameters.assume_yes,
                'daemonMode': cliParameters.daemon_mode,
                'randomSleep': cliParameters.random_sleep,
                'consumerKey': configFileParameters['AUTH']['consumerkey'],
                'consumerSecret': configFileParameters['AUTH']['consumersecret'],
                'accessToken': configFileParameters['AUTH']['accesstoken'],
                'accessTokenSecret': configFileParameters['AUTH']['accesstokensecret']
            }

            # apply config override rules
            ## log filename
            if cliParameters.log_file:
                masterCfg['logFile'] = cliParameters.log_file
            elif configFileParameters['LOGGING']['logfile']:
                # filename for logs set in config, let's use it
                masterCfg['logFile'] = configFileParameters['LOGGING']['logfile']
            else:
                # log filename not provided, we'll use the default
                masterCfg['logFile'] = '/var/log/trumpatron/app.log'

            ## level of logging
            if cliParameters.log_level:
                masterCfg['loggingLvl'] = cliParameters.log_level
            elif configFileParameters['LOGGING']['debuglevel']:
                masterCfg['loggingLvl'] = configFileParameters['LOGGING']['debuglevel']
            else:
                masterCfg['loggingLvl'] = 'WARNING'

            ## number of clauses to be used in tweet
            if cliParameters.num_clauses:
                masterCfg['numClauses'] = cliParameters.num_clauses
            elif configFileParameters['GENERAL']['numclauses']:
                # use config value
                masterCfg['numClauses'] = int(configFileParameters['GENERAL']['numclauses'])
            else:
                masterCfg['numClauses'] = 2

            ## sleep delay
            if cliParameters.sleep_delay != 1:
                masterCfg['sleepDelay'] = cliParameters.sleep_delay
            elif configFileParameters['GENERAL']['sleepdelay']:
                masterCfg['sleepDelay'] = int(configFileParameters['GENERAL']['sleepdelay'])
            else:
                masterCfg['sleepDelay'] = 1

        self.config = masterCfg

    def initializeLogger(self, loggerName, logFormatDef='%(asctime)s [ %(levelname)s ] [ %(name)s ] %(message)s'):
        """
        Initialize logging stream

        :param loggerName: title of logger stream to use
        :param logFormatDef: string declaring the format to write logs in
        :return: void
        """

        # get logging level
        logLvl = getattr(logging, self.config['loggingLvl'].upper())

        # initialize logger
        lgr = logging.getLogger(loggerName)
        lgr.setLevel(logLvl)

        # create file handler for log file
        fileHandler = logging.FileHandler(self.config['logFile'])
        fileHandler.setLevel(logLvl)

        # set output formatter
        frmtr = logging.Formatter(logFormatDef)
        fileHandler.setFormatter(frmtr)

        # associate file handler w/ logger
        lgr.addHandler(fileHandler)

        self.logger = lgr