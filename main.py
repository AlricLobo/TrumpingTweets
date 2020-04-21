from data import *
from ranking import *

def main():
    print("Begining program")
    #queryS = raw_input("Enter query:\n")
    #query = get_query(queryS)
    query = ["china", "economy"]
    print("Gathering tweets")
    allTweets = get_data()
    print("Tweets gathered\nGetting rankings")
    ranks = getRankings(query, allTweets)
    print("Top results: ")
    for doc in ranks:
        print(str(doc[0]["text"]) + "\n" + str(doc[1]) + "\n")
    print("Program finished")



if __name__ == '__main__':
    main()
