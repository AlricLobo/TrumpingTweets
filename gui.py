from tkinter import*
from data import *
from ranking import *
import os
#TO-DO make the gui look nicer and more interactive
#query is the term you search for

start = 0
searchRanks = []

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

search = Entry(root,width = 50)
#search.grid(row = 0, column = 1, padx = 20)
search.pack()
search_label = Label(root, text = "Query")
search_label.pack()
#search_label.grid(row = 0, column = 0)
print_label = Label(root, text= "Answers Displayed Here")
print_label.pack(side = BOTTOM)
#print_label.grid(row=4, column = 0, columnspan = 4)
#photo1 = PhotoImage(file = r"C:\Users\alric\Desktop\pa1-spring20\TrumpingTweets\gui_logo.GIF")
#Label (e,image = photo1, bg = "white").grid(row=0,column = 0, sticky = W)

data = get_data()
def myClick():
    print("Cleaning up program from last execution")
    cleanTxtFiles()
    print("Beginning program")
    global searchRanks
    query = search.get()
    search.delete(0, END)
    query = get_query(query)
    ranks = getRankings(query,data)
    searchRanks = ranks
    ranks = ranks[0:5]
    
    print_records = ''
    for doc in ranks:
        print_records += str(doc[0]["text"]).replace('. ','.\n') + "\n" + "Doc score: " + str(doc[1]) + "\n\n"
    print("Program finished")
    print_label['text'] = print_records
    




    

def nextClick():
    global start
    
    start = start + 5
    if(start > len(searchRanks)):
    
    	start = len(searchRanks) - 5
    
    end = start + 5
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
        print_records += str(doc[0]["text"]).replace('. ','.\n') + "\n" + "Doc score: " + str(doc[1]) + "\n\n"
    print("Program finished")
    print_label['text'] = print_records
    



def prevClick():
    global start
    
    start = start - 5
    if(start < 0):
    
    	start = 0
    
    end = start + 5
    if(end < 0):
    
    	end = 5
    
    ranks = searchRanks[start:end]
    print(len(ranks))
    print(len(searchRanks))
    print_records = ''
    stringNewLine = ''
    #stringNewLine = str(doc[0]["text"])
    #stringNewLine.replace('.','.\n')
    for doc in ranks:
        print_records += str(doc[0]["text"]).replace('. ','.\n') + "\n" + "Doc score: " + str(doc[1]) + "\n\n"
    print("Program finished")
    print_label['text'] = print_records
searchButton = Button(root, text = "Search", command = myClick)
searchButton.pack()
#searchButton.grid(row = 3, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)
nextButton = Button(root, text = "Next", command = nextClick,pady = 10, padx = 10)
#nextButton.grid(row = 3, column = 3)
nextButton.pack(side = RIGHT)
prevButton = Button(root, text = "Prev", command = prevClick,pady = 10, padx = 10)
#prevButton.grid(row = 3, column = 2)
prevButton.pack(side = LEFT)
#prevButton.pack()

root.mainloop()