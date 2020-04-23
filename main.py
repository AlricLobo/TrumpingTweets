from data import *
from ranking import *

import random
import math

import os #used in cleanTxtFiles

def cleanTxtFiles():
    #removes the test files generated while debugging
    #remove call to this function when testing
    filesInDir = os.listdir(os.curdir)
    for file in filesInDir:
        if file.endswith(".txt"):
            print("Removing " + str(file))
            os.remove(os.path.join(os.curdir, file))

def DCGScore(relScores):
    #Returns the DCG scores from a list of relevancy scores
    #This scores will be normalized later
    dcgScore = 0
    count = 2
    for i in relScores:
        dcgScore += ((2 ** i) - 1) / (math.log(count, 2))
        count += 1
    return dcgScore

def main():
    #This program is used for rapid testing and output adjustment
    #The proper GUI is to be used by the users, not this
    numResults = 10
    print("Begining program")
    print("Gathering tweets")
    allTweets = get_data()
    queryS = input("Enter query:\n")
    query = get_query(queryS)
    print("Tweets gathered\nGetting rankings")
    ranks = getRankings(query, allTweets)
    print("Top results: ")
    topDocs = ranks[:numResults]
    randTopDocs = topDocs
    random.shuffle(randTopDocs)

    userRanking = []    #to be used to calc NDCG

    for doc in topDocs:
        if doc["doc_score"] == 0:
            continue
        print(doc["text"])
        print(doc["doc_score"])
        print(doc["retweet_count"])
        print(doc["favorite_count"])
        print(doc["created_at"])
        print("\n\n")
    exit()

    #Get user ranking [0-3] for the randomized top numResults
    for doc in randTopDocs:
        print(doc["text"])
        uInput = ''
        while not (uInput == '0' or uInput == '1' or uInput == '2' or uInput == '3'):
            uInput = input()
        userRanking.append(int(uInput))
        for d in topDocs:
            if d["id_str"] == doc["id_str"]:
                d["user_rank"] = int(uInput)
                break

    #Calculate MAP
    mapScore = 0
    numRel = 0
    for i in range(numResults):
        if topDocs[i]["user_rank"] > 0:
            numRel += 1
        mapScore += (numRel / (i + 1))
    mapScore = mapScore / numResults
    print("Map score is: " + str(mapScore))

    #Calculate NDCG
    userRanking.sort(reverse = True)
    perfectNDCG = DCGScore(userRanking) / numResults
    algoResults = []
    for doc in topDocs:
        algoResults.append(doc["user_rank"])
    ndcgScore = DCGScore(algoResults) / numResults
    ndcgScore = ndcgScore / perfectNDCG
    print("NDCG score is: " + str(ndcgScore))

if __name__ == '__main__':
    main()
