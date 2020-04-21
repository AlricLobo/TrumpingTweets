from data import *
from ranking import *

import os #used in cleanTxtFiles

def cleanTxtFiles():
    #removes the test files generated while debugging
    #remove call to this function when testing
    filesInDir = os.listdir(os.curdir)
    for file in filesInDir:
        if file.endswith(".txt"):
            print("Removing " + str(file))
            os.remove(os.path.join(os.curdir, file))

def main():
    print("Cleaning up program from last execution")
    cleanTxtFiles()
    print("Begining program")
    queryS = input("Enter query:\n")
    query = get_query(queryS)
    print("Gathering tweets")
    allTweets = get_data()
    print("Tweets gathered\nGetting rankings")
    ranks = getRankings(query, allTweets)
    print("Top results: ")
    for doc in ranks:
        print(str(doc[0]["text"]) + "\n" + "Doc score: " + str(doc[1]) + "\n\n")
    print("Program finished")



if __name__ == '__main__':
    main()
