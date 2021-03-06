from tkinter import*
from data import *
from ranking import *
import os
#TO-DO make the gui look nicer and more interactive
#query is the term you search for

start = 0
searchRanks = []
isFav = False
isRel = True
isRetweet = False
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
answerFrame = Frame(root, padx = 5, pady = 5,  bg = "gray25",width = 10000, height = 700)
answerFrame.pack()
answerFrame.pack_propagate(False)
searchFrame.pack_propagate(False)
search = Entry(searchFrame,width = 50)
search.grid(row = 0, column = 1, pady = 10, padx = 10, ipadx = 100)
search_label = Label(searchFrame, text = "Query")
search_label.grid(row = 0, column = 0)

print_label = Label(answerFrame, text= "Answers Displayed Here", font = ("Lucida Grande",10,"bold"), bg = "gray25" , fg = "white")
print_label.pack()
options = ["Relevance", "favorites", "retweets"]

clicked = StringVar()
clicked.set(options[0])
drop = OptionMenu(searchFrame,clicked,*options)
drop.grid(row = 1, column = 4)

data = get_data()

def printAns(rankArray, start, end):
	print_records = ''
	snippet = rankArray[start:end]
	for doc in snippet:
		print_records += str(doc["text"]).replace('. ','.\n') + "\n" + "Doc score: " + str(doc["doc_score"]) + "\n" + "retweets: " + str(doc["retweet_count"]) + "\n"+ "favorites: " + str(doc["favorite_count"]) + "\n" + str(doc["created_at"]).replace("+0000","") + "\n\n"
	print("Program finished")
	print_label['text'] = print_records
def myClick():
    #print("Cleaning up program from last execution")
    #cleanTxtFiles()
    print("Beginning program")
    global searchRanks
    global start
    ranks = []
    query = search.get()
    search.delete(0, END)
    query = get_query(query)
    if not query:
    	print_label['text'] = "Please enter a Query"
    else:    	

    	unRefRanks = getRankings(query,data)
    
    	for doc in unRefRanks:
        	if doc["doc_score"] > 0:
        		ranks.append(doc)                
    	
    	print(len(ranks))
    	if(clicked.get() == "Relevance"):
    		searchRanks = ranks
    		isRel = True
    		isFav = False
    		isRetweet = False
    	elif(clicked.get() == "favorites"):
    		searchRanks = ranks
    		ranks = sorted(ranks,key= lambda i: i['favorite_count'],reverse = True)
    		
    		favRanks = ranks
    		isRel = False
    		isFav = True
    		isRetweet = False
    	elif(clicked.get() == "retweets"):
    		print("reached")
    		searchRanks = ranks
    		ranks = sorted(ranks,key= lambda i: i['retweet_count'],reverse = True)
    		#searchRanks = ranks
    		retweetRanks = ranks
    		isRel = False
    		isFav = False
    		isRetweet = True
    	start = 0
    	printAns(ranks,0,3)
    



    

def nextClick():
    global start
    global isFav
    global isRel
    global isRetweet
    global favRanks
    global retweetRanks
    start = start + 3
    if(start > len(searchRanks)):
    
    	start = len(searchRanks) - 3
    end = start + 3
    if(end > len(searchRanks)):
    	start = len(searchRanks) - 3
    	end = len(searchRanks)
    if(isRel == True):
    	printAns(searchRanks,start,end)
    elif isFav == True:
    	printAns(favRanks,start,end)
    elif isRetweet == True:
    	printAns(retweetRanks,start,end)

    
    



def prevClick():
    global start
    
    start = start - 3
    if(start < 0):
    
    	start = 0
    
    end = start + 3
    if(end < 0):
    	start = 0
    	end = 3
    
    ranks = searchRanks[start:end]
    print(len(ranks))
    print(len(searchRanks))
    if(end > len(searchRanks)):
    
    	end = len(searchRanks)
    if(isRel == True):
    	printAns(searchRanks,start,end)
    elif isFav == True:
    	printAns(favRanks,start,end)
    elif isRetweet == True:
    	printAns(retweetRanks,start,end)

    
    
def updateClick():
	ranks =[]
	global start
	global isFav
	global isRel
	global isRetweet
	global favRanks
	global retweetRanks
	if(clicked.get() == "Relevance"):
		isRel = True
		isFav = False
		isRetweet = False
		if(len(searchRanks) != 0):
			printAns(searchRanks,0,3)
	elif(clicked.get() == "favorites"):
		isRel = False
		isFav = True
		isRetweet = False
		if(len(favRanks)!= 0):
			printAns(favRanks,0,3)
		elif(len(favRanks) == 0 and len(searchRanks) != 0):
			ranks = searchRanks 
			ranks = sorted(ranks,key= lambda i: i['favorite_count'],reverse = True)
			favRanks = ranks
			printAns(ranks,0,3)
	elif(clicked.get() == "retweets"):
		isRel = False
		isFav = False
		isRetweet = True
		print("reached")
		if(len(retweetRanks)!= 0):
			printAns(retweetRanks,0,3)
		elif(len(retweetRanks) == 0 and len(searchRanks) != 0):
			print("reached here")
			ranks = searchRanks 
			ranks = sorted(ranks,key= lambda i: i['retweet_count'],reverse = True)
			retweetRanks = ranks
			printAns(ranks,0,3)
	start = 0

	
searchButton = Button(searchFrame, text = "Search", command = myClick)
#searchButton.pack(side = BOTTOM)
searchButton.grid(row = 2, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)
nextButton = Button(searchFrame, text = "Next", command = nextClick,pady = 10, padx = 10)
nextButton.grid(row = 3, column = 3)
#nextButton.pack(side = RIGHT)
prevButton = Button(searchFrame, text = "Prev", command = prevClick,pady = 10, padx = 10)
prevButton.grid(row = 3, column = 0)

updateButton = Button(searchFrame, text = "Update", command = updateClick,pady = 10, padx = 10)
updateButton.grid(row = 3, column = 4)
root.mainloop()