import json

def get_data():
    #test file of 2020 tweets
    #TO-DO add and append the dictionary with every tweet since 2009
    with open(r'C:\Users\alric\Desktop\pa1-spring20\TrumpingTweets\data.json',encoding = "utf8") as f:

        data = json.load(f)
        for i in data:
            i['text'] = i['text'].encode('ascii', 'ignore').decode('ascii')

        return data

def get_query(q):
    queryWords = q.lower()
    queryWords = queryWords.split()

    return queryWords

