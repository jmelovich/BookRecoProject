# at the moment this script is just giving an example usage of tkinter for creating a window and simple UI
# i also demonstrate how to import a function from another file, which is useful for organizational purposes
# for example, we can create seperate py files for each type of approach or complicated operation and then run them from here

# in this case, I import the add_numbers function from the functions.py file, which defines that method from a C function 
# defined in functions/add_numbers.cpp

import tkinter as tk
from playground_functions import add_numbers

def button_click():
    num1 = entry1.get()
    num2 = entry2.get()
    result = add_numbers(num1, num2)
    label.config(text=f"Result: {result}")

# Create the main window
root = tk.Tk()
root.title("Number Adder (C++ Backend)")
root.geometry("300x200")

# Create input fields
entry1 = tk.Entry(root)
entry1.pack(pady=5)

entry2 = tk.Entry(root)
entry2.pack(pady=5)

# Create a button
button = tk.Button(root, text="Add Numbers", command=button_click)
button.pack(pady=10)

# Create a label
label = tk.Label(root, text="Result: ")
label.pack(pady=10)

# Start the GUI event loop
root.mainloop()