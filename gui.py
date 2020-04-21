from tkinter import*
from data import get_data
#TO-DO make the gui look nicer and more interactive
#query is the term you search for

root = Tk()

e = Entry(root,width = 50)
e.pack()

def myClick():
    query = e.get()
    print(query)
    data = get_data()
    print(data[1])
myButton = Button(root, text = "Search", command = myClick)
myButton.pack()


root.mainloop()