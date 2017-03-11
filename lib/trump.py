#!/usr/bin/python3

"""
Trump.py

APP: TrumpaTron
DESC: A model class for performing tweet-based logic
CREATION_DATE: 2017-02-27

"""

# MODULES
# | Native
from random import choice, shuffle, randint
from curses.ascii import ispunct
import re
from os import fork
import time

# | Third-Party
import tweepy

# | Custom
import lib.bannon

# METADATA
__author__ = 'Joshua Carlson-Purcell'
__copyright__ = 'Copyright 2017, CarlsoNet'
__license__ = 'MIT'
__version__ = '1.0.1'
__maintainer__ = 'Joshua Carlson-Purcell'
__email__ = 'jcarlson@carlso.net'
__status__ = 'Production'


class Trump(lib.bannon.Bannon):
    """
    Trump.py

    The main tweet-controlling class
    """

    apiConn = None
    tweetSet = []
    tweetClauses = []
    generatedTweet = ''

    def __init__(self, cliParams, configParams):
        lib.bannon.Bannon.__init__(self, cliParams, configParams)

        # connect to Twitter API
        self.createTwitterAPIConn()

    def createTwitterAPIConn(self):
        """
        Authenticate to Twitter API using Tweepy library

        :return: void
        """

        # auth to twitter using oAuth
        auth = tweepy.OAuthHandler(self.config['consumerKey'], self.config['consumerSecret'])
        auth.set_access_token(self.config['accessToken'], self.config['accessTokenSecret'])

        # connect to twitter API
        self.apiConn = tweepy.API(auth)


    def getTweets(self, twitterUsername):
        """
        Get default tweet list for given twitter username

        :param twitterUsername: Twitter username or ID to fetch tweets from
        :return: void
        """

        # get public timeline tweets for user
        rawTweets = self.apiConn.user_timeline(twitterUsername)

        # strip tweet text from raw tweets
        for tweet in rawTweets:
            self.tweetSet.append(tweet.text)


    def spliceTweets(self):
        """
        Splice a set of tweets into a list of individual clauses

        :return: void
        """

        clauses = []

        # list and splice fetched tweets
        for tweet in self.tweetSet:
            # split tweet into list of clauses
            clauseSet = tweet.split('. ')

            # add clause set to master set
            clauses += clauseSet

        self.tweetClauses = clauses


    def formatTweet(self, tweetTxt):
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


    def pruneTweetClauses(self):
        """
        Prune and deduplicate sets of Tweet clauses

        :return: void
        """

        # dedupe clause set
        prunedTweetClauseSet = list(set(self.tweetClauses))
        prunedTweetClauseSet.sort(key=self.tweetClauses.index)

        # filter tweet text
        for i in range(0, len(prunedTweetClauseSet)):
            prunedTweetClauseSet[i] = self.formatTweet(prunedTweetClauseSet[i])

        # sort list of clauses by length
        prunedTweetClauseSet.sort(key=len)

        self.tweetClauses = prunedTweetClauseSet


    def divideClausesIntoSlices(self):
        """
        Split self.tweetClauses into N number of slices, where n = numClauses

        :return: a list containing all clause slices
        """

        slices = []

        # divide the set of tweet clauses into n slices, where n = numClausesToUse
        numClausesInSlice = int(len(self.tweetClauses) / self.config['numClauses'])

        # iterate through slices
        for i in range(0, self.config['numClauses']):
            slices.append([])

            # fill up slice with values
            startTweetClauseIdx = i * numClausesInSlice
            endTweetClauseIdx = startTweetClauseIdx + numClausesInSlice
            slices[i] = self.tweetClauses[startTweetClauseIdx:endTweetClauseIdx]

        return slices


    def getRandomTweetClause(self, clauses):
        """
        Choose a random clause from the set of tweet clauses

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


    def generateTweet(self):
        """
        Generates a unique tweet from a given set of sentence clauses

        :return: void
        """

        # check if tweet clauses are available
        if self.tweetClauses:
            slices = self.divideClausesIntoSlices()

            # generate tweet from clause slices
            # longest slice clause is always first, shortest is last, and the middle are chosen at random for
            # n - 2 clausesToUse
            longestClause = self.getRandomTweetClause(slices[-1])
            slices.pop(-1)

            shortestClause = self.getRandomTweetClause(slices[0])
            slices.pop(0)

            # generate middle clauses if any slices are still left
            middleClauses = ''
            if slices:
                # shuffle middle slices
                shuffle(slices)
                for clauseSlice in slices:
                    currentClause = self.getRandomTweetClause(clauseSlice)
                    middleClauses += currentClause

                # cap w/ period if not already punctuated
                if not ispunct(middleClauses[-1]):
                    middleClauses += '.'

            # concatonate tweet
            newTweet = longestClause + ' ' + middleClauses + ' ' + shortestClause

            self.generatedTweet = newTweet
        else:
            raise ValueError('no tweet clauses available')


    def sendTweet(self):
        """
        Send new generated Tweet to Twitter API

        :return: int based on success/fail : -1=discarded;0=no tweet provided;1=published
        """

        if self.generatedTweet:
            # send tweet to authenticated account using tweepy api connection
            if not self.config['assumeYes']:
                print('GENERATED TWEET:', self.generatedTweet)
                shouldPublish = input('=> Would you like to publish this tweet? [y/N]: ')
                shouldPublish = shouldPublish.strip().lower()
                if (shouldPublish != 'y' and shouldPublish != 'yes') or not shouldPublish:
                    return -1

            # attempt to publish tweet
            return self.apiConn.update_status(self.generatedTweet)
        else:
            raise ValueError('empty tweet text provided')


    def startBot(self, twitterUser):
        """
        Start button for TrumpaTron

        :param twitterUser: username (or ID) of user to fetch tweets from
        :return: void
        """

        # start while loop for daemon mode
        while True:
            # fetch tweets
            self.getTweets(twitterUser)
            # self.logger.debug('RAW TWEETS :: ' + str(self.tweetSet))

            # splice tweets into clauses and prune
            self.spliceTweets()
            self.pruneTweetClauses()
            # self.logger.debug('POST-SPLICED AND PRUNED TWEET CLAUSES :: ' + str(self.tweetClauses))

            # generate new tweet from clauses
            numTweetGenIterations = 0
            maxTweetGenIterations = 100
            while len(self.generatedTweet) == 0 or 140 < len(self.generatedTweet):
                # tweet msg is too long, try regenerating
                self.generateTweet()

                # increase generation count
                numTweetGenIterations += 1

                # check if iteration max has been hit
                if maxTweetGenIterations < numTweetGenIterations:
                    self.logger.critical('Maximum number of Tweet generation attempts ( ' + str(maxTweetGenIterations)
                                         + ' ) has been reached. Try reducing the number of clauses.')

                    exit(2)

            self.logger.debug('GENERATED TWEET: ' + self.generatedTweet)

            # publish tweet
            try:
                # check if this is a test run
                if not self.config['testRun']:
                    # not a test run, send tweet
                    tweetPubRslt = self.sendTweet()

                    # check result
                    if tweetPubRslt == -1:
                        self.logger.info('tweet not published, discarding...')
                    elif not tweetPubRslt:
                        self.logger.error('could not publish tweet for an unknown reason :(')
                    else:
                        self.logger.info('TWEET PUBLISHED SUCCESSFULLY! [ ID: ' + str(tweetPubRslt.id) + ' ]')
                else:
                    self.logger.info('application in test mode, exiting w/o sending tweet')
            except ValueError as valErr:
                self.logger.warning('invalid value provided for tweet :: ' + newTweet + ' :: ' + str(valErr))
            except tweepy.TweepError as err:
                self.logger.critical('could not publish tweet :: ' + self.generatedTweet + ' :: '
                                     + str(err.response) + ' :: ' + str(err.reason))

                exit(1)

            # check if we're in daemon mode and should restart loop or not
            if not self.config['daemonMode']:
                break
            else:
                # start by forking to a bg process
                if fork():
                    # fork successful, exit main process
                    exit()

                # in daemon mode, sleep for n second(s), where 1 <= n
                if self.config['sleepDelay']:
                    # check if random delay has been requested
                    if self.config['randomSleep']:
                        sleepDelay = randint(1, self.config['sleepDelay'])
                    else:
                        sleepDelay = self.config['sleepDelay']
                else:
                    # sleep delay not specified, use default
                    sleepDelay = 1

                # perform sleep
                self.logger.debug('sleeping for [ ' + str(sleepDelay) + ' ] seconds...')
                time.sleep(sleepDelay)

