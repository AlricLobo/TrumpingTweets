import json   #used to load the tweets into a dictionary
import codecs #used to load the data file with the proper encoding
import string #used to remove punctuation from tweet

def isStartTweet(text):
    #how many . does the tweet start with? i.e. ...and then I said
    count = 0
    for i in text:
        if i == '.':
            count += 1
        else:
            return count
    return count

def isEndTweet(text):
    #how many . does the tweet end with? i.e. then he said...
    count = 0
    for i in reversed(text):
        if i == '.':
            count += 1
        else:
            return count
    return count

def cleanInput(text):
    #removes all non-letters from the input, helps to make sure words are properly accounted for
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return ''.join(filter(whitelist.__contains__, text))

def modifyData(data):
    stack = []

    #because tweets at the same time are in reverse order, we gotta fix it
    lastTweet = data[-1]
    reverseTimeQueue = []

    #lol, don't even ask how this works. I did it an hour ago and even I don't wanna comb through it

    for tweet in data[:]:
        if "is_retweet" not in tweet and tweet["text"][:4] == "RT @":
            data.remove(tweet)
        elif "is_retweet" in tweet and (tweet["text"][:4] == "RT @" or tweet["is_retweet"] == True):
            data.remove(tweet)
        else:
            tweet["text"] = tweet["text"].lower()
            #Everything below here serves one purpose, combine tweets that were meant to be together
            #The issue..? they reverse order if they were at the same time, and some groups of 3 tweets
            #would be ordered BAC or ACB or CBA or ABC, I had to account for all of those options
            #This was horrible to code and debug. I did it, but at what cost...
            if lastTweet["created_at"] == tweet["created_at"]:
                reverseTimeQueue.append(lastTweet)
            elif lastTweet["created_at"] != tweet["created_at"] and len(reverseTimeQueue) > 0:
                tempTweet = reverseTimeQueue[0]
                reverseTimeQueue.append(lastTweet)
                tempTweet["text"] = reverseTimeQueue[0]["text"][:(-1 * isEndTweet(reverseTimeQueue[0]["text"]))]
                for t in reverseTimeQueue[1:]:
                    tempTweet["text"] = tempTweet["text"] + " " + t["text"][isStartTweet(t["text"]):]
                if isStartTweet(tempTweet["text"]) >= 3:
                    stack.append(tempTweet)
                elif len(stack) > 0 and isEndTweet(tempTweet["text"]) >= 3:
                    while len(stack) > 0:
                        prevTweet = stack.pop()
                        if prevTweet in data:
                            data.remove(prevTweet)
                        tempTweet["text"] = tempTweet["text"][:(-1 * isEndTweet(tempTweet["text"]))] + " " + prevTweet["text"][isStartTweet(prevTweet["text"]):]
                    data.append(tempTweet)
                else:
                    data.append(tempTweet)
                while len(reverseTimeQueue) > 0:
                    temp = reverseTimeQueue.pop()
                    data.remove(temp)
            elif isStartTweet(tweet["text"]) >= 3:
                stack.append(tweet)
            elif len(stack) > 0 and isEndTweet(tweet["text"]) >= 3:
                while len(stack) > 0:
                    prevTweet = stack.pop()
                    if prevTweet in data:
                        data.remove(prevTweet)
                    tweet["text"] = tweet["text"][:(-1 * isEndTweet(tweet["text"]))] + " " + prevTweet["text"][isStartTweet(prevTweet["text"]):]
            elif len(stack) > 0:
                while len(stack) > 0:
                    stack.pop()
            lastTweet = tweet
    
    for tweet in data:
        tweet["text"] = tweet["text"].translate(tweet["text"].maketrans('', '', string.punctuation))

    #used to save data modifications to disk
    f_out = open('allTweets_ready2.json', 'w')
    json.dump(data, f_out)
    print("data done")
    exit()

def get_data():
    #call modifyData if the dataset needs to be adjusted to the program
    f = open('allTweets_ready3.json', 'r')
    data = json.load(f)
    return data

def get_query(q):
    #takes the query input from the user and returns a list, used in testing/debugging
    queryWords = q.lower()
    queryWords = queryWords.split()

    return queryWords

