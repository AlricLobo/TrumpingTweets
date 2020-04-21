import os.path #used to check if a file exists in averageLength

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


def getRankings(query, tweets, bodyweight = _bodyweight, bbody = _bbody, k1 = _k1, PRLambda = _PRLambda, PRLambdaP = _PRLambdaP):
    #get term frequencies for each document and normalize with weights, combining equation 2 and 3 in the handout
    avgLenOfAll = averageLength(tweets)
    w_dt = {}


    for tweet in tweets:
        weightedTF = {}
        words = tweet["text"].split()
        for word in words:
            if word not in weightedTF:
                weightedTF[word] = 0
            weightedTF[word] += 1
        w_dt[tweet] = 0
        for word in weightedTF:
            weightedTF[word] = weightedTF[word] / ((1 - bbody) + bbody * (words.length / avgLenOfAll))
            w_dt[tweet] += weightedTF[word] * bodyweight

    return "test"