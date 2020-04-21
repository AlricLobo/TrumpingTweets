import os.path  #used to check if a file exists in averageLength() and getIDF()
import json     #used to write idf to file in getIDF()
import math     #used in getRankings to take the log of IDF and the lambda function
import operator #used in getNBestMatches to sort the docScores and pick the best

#Global variables for the BM25 input
_bodyweight = 0.5
_bbody = 0.5
_k1 = 0.5
_PRLambda = 0.5
_PRLambdaP = 0.5

def averageLength(tweets):
    #to save time, the average length will be computed once per set of data
    #it will then be saved to a text document with the name "tweets_#ofTweets"
    #since it is unlikely we will have sets with the same number of tweets

    avgLen = -1
    if os.path.isfile('tweets_' + str(tweets.length) + '.txt'):
        f = open('tweets_' + str(tweets.length) + '.txt')
        avgLen = f.read()
    else:
        totLength = 0
        tweetCount = tweets.length
        for tweet in tweets:
            words = tweet["text"].split()
            totLength += words.length
        avgLen = totLength / tweetCount
        f = open('tweets_' + str(tweets.length) + '.txt', 'x')
        f.write(avgLen)

    return avgLen

def getIDF(tweets):
    idf = {}

    return idf

def getNBestMatches(n, docScores):
    bestMatches = sorted(docScores.items(), key=operator.itemgetter(1))
    bestNMatches = bestMatches[-n:]
    bestNMatches.reverse()
    return bestNMatches


def getRankings(query, tweets, bodyweight = _bodyweight, bbody = _bbody, k1 = _k1, PRLambda = _PRLambda, PRLambdaP = _PRLambdaP):
    #query is a list [], tweets is a dictionary defined in data.py, other arguments are used to tune performance
    #function returns a list of tuples, first item is the tweet dictionary, second is the score (ordered best->worst)

    #get term frequencies for each document and normalize with weights, combining equation 2 and 3 in the handout
    avgLenOfAll = averageLength(tweets)
    allIDF = getIDF(tweets)
    docScores = {}

    for tweet in tweets:
        weightedTF = {}
        words = tweet["text"].split()
        for word in words:
            if word not in weightedTF:
                weightedTF[word] = 0
            weightedTF[word] += 1
        for word in weightedTF:
            weightedTF[word] = weightedTF[word] / ((1 - bbody) + bbody * (words.length / avgLenOfAll))
            weightedTF[word] += weightedTF[word] * bodyweight
        docScores[tweet] = 0
        for word in query:
            if word in weightedTF[word]:
                docScores[tweet] += (weightedTF[word] / (k1 + weightedTF)) * math.log(allIDF[word])
                docScores[tweet] += PRLambda * math.log(docScores[tweet] + PRLambdaP)

    bestMatches = getNBestMatches(10, docScores)

    #DEBUG
    for item in bestMatches:
        print(item[1])

    return bestMatches