# at the moment this script is just giving an example usage of tkinter for creating a window and simple UI
# i also demonstrate how to import a function from another file, which is useful for organizational purposes
# for example, we can create seperate py files for each type of approach or complicated operation and then run them from here

# in this case, I import the add_numbers function from the functions.py file, which defines that method from a C function 
# defined in functions/add_numbers.cpp

import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteEntry
from playground_functions import add_numbers

def button_click():
    label_greybox1 = tk.Label(root,  background="#8c92ac", width=14, height=7)
    label_greybox2 = tk.Label(root, background="#8c92ac", width=14, height=7)
    label_greybox3 = tk.Label(root, background="#8c92ac", width=14, height=7)
    label_greybox4 = tk.Label(root, background="#8c92ac", width=14, height=7)
    label_greybox5 = tk.Label(root, background="#8c92ac", width=14, height=7)
    label_greybox1.place(x=550, y=10)
    label_greybox2.place(x=550, y=150)
    label_greybox3.place(x=550, y=290)
    label_greybox4.place(x=550, y=430)
    label_greybox5.place(x=550, y=570)

# Create the main window
root = tk.Tk()
root.title("Amazon Popular Books Filter Program")
root.geometry("1300x800")
root['background'] = '#8c92ac'

label = tk.Label(root, width= 100, height=5, bg="#3C5291")
label.place(x=0, y=0)

label = tk.Label(root, width= 200, height=100, bg="#172038")
label.place(x=490, y=0)

label = tk.Label(root, width= 200, height=100, bg="#4B68B8")
label.place(x=500, y=0)


# Create Genre Search Bar
genre_entry = tk.Entry(root, width=20)
genre_entry.place(x=100, y=135)
label = tk.Label(root, text="Genre: ", font="Poppins", background='#8c92ac')
label.place(x=10, y=130)

#Create min price entry field
entry_minprice = tk.Entry(root, width=20)
entry_minprice.place(x=200, y=185)
label = tk.Label(root, text="Min Price Point: ", font="Poppins", background='#8c92ac')
label.place(x=10, y=180)

#Create max price entry field
entry_maxprice = tk.Entry(root, width=20)
entry_maxprice.place(x=200, y=225)
label = tk.Label(root, text="Max Price Point: ", font="Poppins", background='#8c92ac')
label.place(x=10, y=220)

# Create a button
button = tk.Button(root, text="Print Results", font="Poppins", command=button_click, width=10, height=3)
button.place(x=180, y=600)

# Option menu for choosing the algorithm
algorithms = ["Merge Sort", "Sleep Sort", "Shell Sort"] # Not set in stone
var = tk.StringVar(root)
var.set(algorithms[0])

data_structures = tk.OptionMenu(root, var, *algorithms)
data_structures.place(x=200, y = 40)

label = tk.Label(root, text="Sorting Method:", font="Poppins", background='#3C5291')
label.place(x=200, y=10)

#Option menu for sorting variable
Sorting_var = ["Rating", "Review Count", "Page number", "Date", "Alphabetical"]

var = tk.StringVar(root)
var.set(Sorting_var[0])

Sorting_bar = tk.OptionMenu(root, var, *Sorting_var)
Sorting_bar.place(x=20, y = 40)

label = tk.Label(root, text="Sort By: ", font="Poppins", background='#3C5291')
label.place(x=20, y=10)

# # Create input fields
# entry1 = tk.Entry(root)
# entry1.place(x=100, y=200)
#
# entry2 = tk.Entry(root)
# entry2.pack(pady=5)
#
# # Create a button
# button = tk.Button(root, text="Add Numbers", command=button_click)
# button.pack(pady=10)
#


# Start the GUI event loop
root.mainloop()