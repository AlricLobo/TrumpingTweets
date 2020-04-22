from tkinter import*
from data import *
from ranking import *
import os
#TO-DO make the gui look nicer and more interactive
#query is the term you search for

start = 0
searchRanks = []
favRanks = []
retweetRanks = []
def cleanTxtFiles():
    #removes the test files generated while debugging
    #remove call to this function when testing
    filesInDir = os.listdir(os.curdir)
    for file in filesInDir:
        if file.endswith(".txt"):
            print("Removing " + str(file))
            os.remove(os.path.join(os.curdir, file))

root = Tk()
root.title('Trump Tweet Search')
searchFrame = Frame(root)
searchFrame.pack()
#leftFrame = Frame(root, padx = 5, pady = 5)
#leftFrame.pack(padx = 10, pady = 10)
#rightFrame = Frame(root, padx = 5, pady = 5)
#rightFrame.pack(padx = 10, pady = 10)
answerFrame = Frame(root, padx = 5, pady = 5, relief = SUNKEN, bg = "grey",width = 10000, height = 700)
answerFrame.pack()
answerFrame.pack_propagate(False)
search = Entry(searchFrame,width = 50)
#search.pack()
search.grid(row = 0, column = 1, pady = 10, padx = 10, ipadx = 100)
search_label = Label(searchFrame, text = "Query")
#search_label.pack(side = LEFT)
search_label.grid(row = 0, column = 0)

print_label = Label(answerFrame, text= "Answers Displayed Here", font = ("Lucida Grande",10))
print_label.pack()
#print_label.grid(row=4, column = 0, columnspan = 4)
#photo1 = PhotoImage(file = r"C:\Users\alric\Desktop\pa1-spring20\TrumpingTweets\gui_logo.GIF")
#Label (e,image = photo1, bg = "white").grid(row=0,column = 0, sticky = W)
options = ["Relevance", "favorites", "retweets"]

clicked = StringVar()
clicked.set(options[0])
drop = OptionMenu(searchFrame,clicked,*options)
drop.grid(row = 1, column = 4)

data = get_data()
def myClick():
    #print("Cleaning up program from last execution")
    #cleanTxtFiles()
    print("Beginning program")
    global searchRanks
    query = search.get()
    search.delete(0, END)
    query = get_query(query)
    ranks = getRankings(query,data)
    if(clicked.get() == "Relevance"):
    	searchRanks = ranks
    elif(clicked.get() == "favorites"):
    	for doc in ranks:
    		if doc[1] > 0:
    			favRanks.append(doc) 
    	ranks = sorted(favRanks,key= lambda i: i[0]['favorite_count'],reverse = True)
    	searchRanks = ranks
    elif(clicked.get() == "retweets"):
    	print("reached")
    	for doc in ranks:
    		if doc[1] > 0:
    			retweetRanks.append(doc)
    	ranks = sorted(retweetRanks,key= lambda i: i[0]['retweet_count'],reverse = True)
    	searchRanks = ranks

    ranks = ranks[0:3]
    print(ranks[0])
    print_records = ''
    for doc in ranks:
        print_records += str(doc[0]["text"]).replace('. ','.\n') + "\n" + "Doc score: " + str(doc[1]) + "\n" + "retweets: " + str(doc[0]["retweet_count"]) + "\n"+ "favorites: " + str(doc[0]["favorite_count"]) + "\n\n"
    print("Program finished")
    print_label['text'] = print_records
    



    

def nextClick():
    global start
    
    start = start + 3
    if(start > len(searchRanks)):
    
    	start = len(searchRanks) - 3
    
    end = start + 3
    if(end > len(searchRanks)):
    
    	end = len(searchRanks)
    
    ranks = searchRanks[start:end]
    print(len(ranks))
    print(len(searchRanks))
    print_records = ''
    stringNewLine = ''
    #stringNewLine = str(doc[0]["text"])
    #stringNewLine.replace('.','.\n')
    for doc in ranks:
        print_records += str(doc[0]["text"]).replace('. ','.\n') + "\n" + "Doc score: " + str(doc[1]) + "\n" + "retweets: " + str(doc[0]["retweet_count"]) + "\n"+ "favorites: " + str(doc[0]["favorite_count"]) + "\n\n"
    print("Program finished")
    print_label['text'] = print_records
    



def prevClick():
    global start
    
    start = start - 3
    if(start < 0):
    
    	start = 0
    
    end = start + 3
    if(end < 0):
    
    	end = 3
    
    ranks = searchRanks[start:end]
    print(len(ranks))
    print(len(searchRanks))
    print_records = ''
    stringNewLine = ''
    #stringNewLine = str(doc[0]["text"])
    #stringNewLine.replace('.','.\n')
    for doc in ranks:
        print_records += str(doc[0]["text"]).replace('. ','.\n') + "\n" + "Doc score: " + str(doc[1]) + "\n" + "retweets: " + str(doc[0]["retweet_count"]) + "\n"+ "favorites: " + str(doc[0]["favorite_count"]) + "\n\n"
    print("Program finished")
    print_label['text'] = print_records
    '''
def updateClick():
	ranks =[]
	if(clicked.get() == "Relevance"):
		if(len(searchRanks) != 0):
			ranks =searchRanks
	elif(clicked.get() == "favorites"):
		if(len(favRanks)!= 0):
			ranks = favRanks
		elif(len(favRanks) == 0 and len(searchRanks) != 0):
			ranks = searchRanks 
			ranks = sorted(ranks,key= lambda i: i[0]['favorite_count'],reverse = True)
	elif(clicked.get() == "retweets"):
		if(len(retweetRanks)!= 0):
			ranks = retweetRanks
		elif(len(retweetRanks) == 0 and len(searchRanks) != 0):
			ranks = searchRanks 
			ranks = sorted(ranks,key= lambda i: i[0]['favorite_count'],reverse = True)
	print_records = ''
	for doc in ranks:
		print_records += str(doc[0]["text"]).replace('. ','.\n') + "\n" + "Doc score: " + str(doc[1]) + "\n" + "retweets: " + str(doc[0]["retweet_count"]) + "\n"+ "favorites: " + str(doc[0]["favorite_count"]) + "\n\n"
	print("Program finished")
	print_label['text'] = print_records
		'''

	
searchButton = Button(searchFrame, text = "Search", command = myClick)
#searchButton.pack(side = BOTTOM)
searchButton.grid(row = 2, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)
nextButton = Button(searchFrame, text = "Next", command = nextClick,pady = 10, padx = 10)
nextButton.grid(row = 3, column = 3)
#nextButton.pack(side = RIGHT)
prevButton = Button(searchFrame, text = "Prev", command = prevClick,pady = 10, padx = 10)
prevButton.grid(row = 3, column = 0)

#updateButton = Button(searchFrame, text = "Update", command = updateClick,pady = 10, padx = 10)
#updateButton.grid(row = 3, column = 4)
root.mainloop()