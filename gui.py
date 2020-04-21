from tkinter import*
from data import *
from ranking import *
#TO-DO make the gui look nicer and more interactive
#query is the term you search for

root = Tk()
root.title('Trump Tweet Search')

search = Entry(root,width = 50)
search.grid(row = 0, column = 1, padx = 20)

search_label = Label(root, text = "Query")
search_label.grid(row = 0, column = 0)
#photo1 = PhotoImage(file = r"C:\Users\alric\Desktop\pa1-spring20\TrumpingTweets\gui_logo.GIF")
#Label (e,image = photo1, bg = "white").grid(row=0,column = 0, sticky = W)

data = get_data()
Len = len(data)
def myClick():

    query = search.get()
    search.delete(0,END)
    print(query)



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