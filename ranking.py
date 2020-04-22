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

#Additional glabal variables to weigh results by favorites and retweets
_favs = 0.5
_RTs = 0.5

def averageLength(tweets):
    #to save time, the average length will be computed once per set of data
    #it will then be saved to a text document with the name "tweets_#ofTweets"
    #since it is unlikely we will have sets with the same number of tweets

    avgLen = -1
    if os.path.isfile('tweets_avgLen_' + str(len(tweets)) + '.txt'):
        f = open('tweets_avgLen_' + str(len(tweets)) + '.txt', 'r')
        avgLenS = f.read()
        avgLen = map(int, avgLenS)
    else:
        totLength = 0
        tweetCount = len(tweets)
        for tweet in tweets:
            words = tweet["text"].split()
            totLength += len(words)
        avgLen = totLength / tweetCount
        f = open('tweets_avgLen_' + str(len(tweets)) + '.txt', 'w')
        f.write(str(avgLen))

    return avgLen

def getIDF(tweets):
    idf = {}

    if os.path.isfile('tweets_idf_' + str(len(tweets)) + '.txt'):
        f = open('tweets_idf_' + str(len(tweets)) + '.txt', 'r')
        idf = json.load(f)
    else:
        for tweet in tweets:
            words = tweet["text"].split()
            for word in words:
                if word not in idf:
                    idf[word] = 0
                idf[word] += 1
        for word in idf:
            idf[word] = math.log(idf[word])
        f = open('tweets_idf_' + str(len(tweets)) + '.txt', 'w')
        json.dump(idf, f)
    
    return idf

def getNBestMatches(start,n, docScores):
    bestMatches = sorted(docScores.items(), key=operator.itemgetter(1))
    bestMatches.reverse()
    bestNMatches = bestMatches[start:start+n]
    #bestNMatches.reverse()
    return bestNMatches

def getMaxInteractions(tweets):
    maxFav = 0
    maxRT = 0
    for tweet in tweets:
        if tweet["favorite_count"] > maxFav:
            maxFav = tweet["favorite_count"]
        if tweet["retweet_count"] > maxRT:
            maxRT = tweet["retweet_count"]
    return (maxFav, maxRT)


def getRankings(query, tweets, bodyweight = _bodyweight, bbody = _bbody, k1 = _k1, PRLambda = _PRLambda, PRLambdaP = _PRLambdaP, favs = _favs, RTs = _RTs):
    #query is a list [], tweets is a dictionary defined in data.py, other arguments are used to tune performance
    #function returns a list of tuples, first item is the tweet dictionary, second is the score (ordered best->worst)

    #get term frequencies for each document and normalize with weights, combining equation 2 and 3 in the handout
    avgLenOfAll = averageLength(tweets)
    allIDF = getIDF(tweets)
    docScores = {}
    maxInteractions = getMaxInteractions(tweets)

    for tweet in tweets:
        weightedTF = {}
        words = tweet["text"].split()
        for word in words:
            if word not in weightedTF:
                weightedTF[word] = 0
            weightedTF[word] += 1
        for word in weightedTF:
            weightedTF[word] = weightedTF[word] / ((1 - bbody) + bbody * (len(words) / avgLenOfAll))
            weightedTF[word] += weightedTF[word] * bodyweight
        docScores[tweet["id_str"]] = 0
        for word in query:
            if word in weightedTF:
                docScores[tweet["id_str"]] += (weightedTF[word] / (k1 + weightedTF[word])) * math.log(allIDF[word])
                docScores[tweet["id_str"]] += PRLambda * math.log(docScores[tweet["id_str"]] + PRLambdaP)
                #additional variables to adjust score by favorite and retweet counts
                rtAndFavBonus = 1 + (.2 * favs * tweet["favorite_count"] / maxInteractions[0]) + (.5 * RTs * tweet["retweet_count"] / maxInteractions[1])
                if(rtAndFavBonus > 1.5):
                    print("Exceeded max")
                    rtAndFavBonus = 1.5
                docScores[tweet["id_str"]] *= rtAndFavBonus
                '''
    if search == True:
        searchMatchesID = getNBestMatches(start,5,docScores)
        searchMatches = []

        for doc in searchMatchesID:
            for tweet in tweets:
                if doc[0] == tweet["id_str"]:
                    searchMatches.append((tweet, doc[1]))

        return searchMatches

        
    else:
        '''
    
    fullMatchesID = getNBestMatches(0,len(docScores),docScores)
    fullMatches = []

    for doc in fullMatchesID:
        for tweet in tweets:
            if doc[0] == tweet["id_str"]:
                fullMatches.append((tweet, doc[1]))

    return fullMatches

    '''
        bestMatchesID = getNBestMatches(0,5, docScores)
        bestMatches = []

        for doc in bestMatchesID:
            for tweet in tweets:
                if doc[0] == tweet["id_str"]:
                    bestMatches.append((tweet, doc[1]))

        return bestMatches

   '''
