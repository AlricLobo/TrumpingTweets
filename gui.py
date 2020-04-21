from tkinter import*
from data import *
from ranking import *
import os
#TO-DO make the gui look nicer and more interactive
#query is the term you search for
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
search.grid(row = 0, column = 1, padx = 20)

search_label = Label(root, text = "Query")
search_label.grid(row = 0, column = 0)
#photo1 = PhotoImage(file = r"C:\Users\alric\Desktop\pa1-spring20\TrumpingTweets\gui_logo.GIF")
#Label (e,image = photo1, bg = "white").grid(row=0,column = 0, sticky = W)

data = get_data()
def myClick():
    print("Cleaning up program from last execution")
    cleanTxtFiles()
    print("Beginning program")
    query = search.get()
    search.delete(0, END)
    print(query)
    query = get_query(query)
    ranks = getRankings(query,data)
    print_records = ''
    for doc in ranks:
        print_records += str(doc[0]["text"]) + "\n" + "Doc score: " + str(doc[1]) + "\n\n"
    print("Program finished")
    print_label = Label(root, text=print_records)
    print_label.grid(row=4, column = 0, columnspan = 4)




    print(data[19])

def nextClick():
    print("next")

def prevClick():
    print("prev")
searchButton = Button(root, text = "Search", command = myClick)
searchButton.grid(row = 3, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 100)
nextButton = Button(root, text = "Next", command = nextClick)
nextButton.grid(row = 3, column = 3)
prevButton = Button(root, text = "Prev", command = prevClick)
prevButton.grid(row = 3, column = 2)

#prevButton.pack()

root.mainloop()