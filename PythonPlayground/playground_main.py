# at the moment this script is just giving an example usage of tkinter for creating a window and simple UI
# i also demonstrate how to import a function from another file, which is useful for organizational purposes
# for example, we can create seperate py files for each type of approach or complicated operation and then run them from here

# in this case, I import the add_numbers function from the functions.py file, which defines that method from a C function 
# defined in functions/add_numbers.cpp

import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteEntry
from playground_functions import add_numbers

def button_click():
    label_greybox = tk.Label(root,  background="#909090", width=50, height=50)
    label_results = tk.Label(root, background="#909090", font="Poppins")
    label_greybox.place(x=700, y=500)
    if genre_entry.get() == "":
        genre_results = "N/A"
    else:
        genre_results = genre_entry.get()
    if entry_minprice.get() == "":
        minprice_results = "N/A"
    else:
        minprice_results = entry_minprice.get()
    if entry_maxprice.get() == "":
        maxprice_results = "N/A"
    else:
        maxprice_results = entry_maxprice.get()
    label_results.config(text=f"Genre: {genre_results}\n"
                              f"Min Price: {minprice_results}\n"
                              f"Max Price: {maxprice_results}")
    label_results.place(x=700, y=500)


# Create the main window
root = tk.Tk()
root.title("Amazon Popular Books Filter Program")
root.geometry("1300x800")
root['background'] = '#909090'

label = tk.Label(root, width= 100, height=5, bg="#3C5291")
label.place(x=0, y=0)

label = tk.Label(root, width= 200, height=100, bg="#172038")
label.place(x=490, y=0)

label = tk.Label(root, width= 200, height=100, bg="#4B68B8")
label.place(x=500, y=0)


# Create Genre Search Bar
genre_entry = tk.Entry(root, width=20)
genre_entry.place(x=100, y=135)
label = tk.Label(root, text="Genre: ", font="Poppins", background='#909090')
label.place(x=10, y=130)

#Create min price entry field
entry_minprice = tk.Entry(root, width=20)
entry_minprice.place(x=200, y=185)
label = tk.Label(root, text="Min Price Point: ", font="Poppins", background='#909090')
label.place(x=10, y=180)

#Create max price entry field
entry_maxprice = tk.Entry(root, width=20)
entry_maxprice.place(x=200, y=225)
label = tk.Label(root, text="Max Price Point: ", font="Poppins", background='#909090')
label.place(x=10, y=220)

# Create a button
button = tk.Button(root, text="Print Results", font="Poppins", command=button_click, width=10, height=3)
button.place(x=250, y=600)

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