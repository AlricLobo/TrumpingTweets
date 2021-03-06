import os.path  #used to check if a file exists in averageLength() and getIDF()
import json     #used to write idf to file in getIDF()
import math     #used in getRankings to take the log of IDF and the lambda function
import operator #used in getNBestMatches to sort the docScores and pick the best
import time     #used for debugging slow program
import string   #used to remove punctuation in getIDF and getRankings

#Global variables for the BM25 input
_bodyweight = 0.62
_bbody = 0.45
_k1 = 0.4
_PRLambda = 0.86
_PRLambdaP = 0.35

#Additional glabal variables to weigh results by favorites and retweets
_favs = 0.1
_RTs = 0.24


#Most functions here have a time argument, that was used to measure performance time with varying optimizations


def getMetadata(tweets, seconds):
    #to save time, the average length will be computed once per set of data
    #it will then be saved to a text document with the name "tweets_#ofTweets"
    #since it is unlikely we will have sets with the same number of tweets

    print("Getting tweet metadata: " + str(time.time() - seconds))

    avgLen = -1
    if os.path.isfile('tweets_metadata_' + str(len(tweets)) + '.txt'):
        f = open('tweets_metadata_' + str(len(tweets)) + '.txt', 'r')
        mdS = json.load(f)
        md = {0: float(mdS["0"]), 1: float(mdS["1"]), 2: float(mdS["2"]), }
    else:
        totLength = 0
        maxFav = 0
        maxRT = 0
        tweetCount = len(tweets)
        for tweet in tweets:
            words = tweet["text"].split()
            totLength += len(words)
            if tweet["favorite_count"] > maxFav:
                maxFav = tweet["favorite_count"]
            if tweet["retweet_count"] > maxRT:
                maxRT = tweet["retweet_count"]
        avgLen = totLength / tweetCount
        md = { 0: avgLen, 1: maxFav, 2: maxRT }
        
        f = open('tweets_metadata_' + str(len(tweets)) + '.txt', 'w')
        json.dump(md, f)

    print("Returning tweet metadata: " + str(time.time() - seconds))

    return md

def getIDF(tweets, seconds):
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    #Similar goal as above, will automatically save/load IDF for an archive
    #if it exists. Will generate it if the file doesn't exist
    seconds = time.time()
    print("Getting tweet IDF: " + str(time.time() - seconds))
    idf = {}

    if os.path.isfile('tweets_idf_' + str(len(tweets)) + '.txt'):
        f = open('tweets_idf_' + str(len(tweets)) + '.txt', 'r')
        idf = json.load(f)
    else:
        for tweet in tweets:
            words = tweet["text"].split()
            for word in words:
                tempWord = ''.join(filter(whitelist.__contains__, word))
                if tempWord not in idf:
                    idf[tempWord] = 0
                idf[tempWord] += 1
        f = open('tweets_idf_' + str(len(tweets)) + '.txt', 'w')
        json.dump(idf, f)

    print("Returning tweet IDF: " + str(time.time() - seconds))
    
    return idf

def getBestMatches(tweets, seconds):
    #Sorts the list of tweets by highest score
    print("Starting best matches: " + str(time.time() - seconds))
    bestMatches = sorted(tweets, key = lambda i: i["doc_score"])
    bestMatches.reverse()
    print("Finishing best matches: " + str(time.time() - seconds))
    return bestMatches

def getRankings(query, tweets, bodyweight = _bodyweight, bbody = _bbody, k1 = _k1, PRLambda = _PRLambda, PRLambdaP = _PRLambdaP, favs = _favs, RTs = _RTs):
    #query is a list [], tweets is a dictionary defined in data.py, other arguments are used to tune performance
    #function returns a list of tuples, first item is the tweet dictionary, second is the score (ordered best->worst)

    seconds = time.time()

    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    #get term frequencies for each document and normalize with weights, combining equation 2 and 3 in the handout
    md = getMetadata(tweets, seconds)
    allIDF = getIDF(tweets, seconds)

    print("Starting rankings algorithm: " + str(time.time() - seconds))

    for tweet in tweets:
        weightedTF = {}
        words = tweet["text"].split()
        for word in words:
            tempWord = ''.join(filter(whitelist.__contains__, word))
            if tempWord not in weightedTF:
                weightedTF[tempWord] = 0
            weightedTF[tempWord] += 1
        for word in weightedTF:
            weightedTF[word] = weightedTF[word] / ((1 - bbody) + bbody * (len(words) / md[0]))
            weightedTF[word] += weightedTF[word] * bodyweight
        tweet["doc_score"] = 0
        for word in query:
            tempWord = ''.join(filter(whitelist.__contains__, word))
            if tempWord in weightedTF:
                tweet["doc_score"] += (weightedTF[tempWord] / (k1 + weightedTF[tempWord])) * math.log(allIDF[tempWord] + 1)
                tweet["doc_score"] += PRLambda * math.log(tweet["doc_score"] + PRLambdaP)
                #additional variables to adjust score by favorite and retweet counts
                rtAndFavBonus = 1 + (.2 * favs * tweet["favorite_count"] / md[1]) + (.5 * RTs * tweet["retweet_count"] / md[2])
                if(rtAndFavBonus > 1.5):
                    print("Exceeded max")
                    rtAndFavBonus = 1.5
                tweet["doc_score"] *= rtAndFavBonus
    print("Finishing rankings algorithm: " + str(time.time() - seconds))
    
    fullMatches = getBestMatches(tweets, seconds)

    return fullMatches