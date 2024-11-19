import os
import webbrowser
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import kagglehub

import book_database_cpp
import time

selected_genres = []

def create_label(parent, text, font, background, row, column):
    label = tk.Label(parent, text=text, font=font, background=background)
    label.grid(row=row, column=column, sticky='w', padx=10, pady=5)
    return label

def create_entry(parent, width, row, column):
    entry = tk.Entry(parent, width=width)
    entry.grid(row=row, column=column, padx=10, pady=5)
    return entry

def create_button(parent, text, command, font, width, height, row, column):
    button = tk.Button(parent, text=text, command=command, font=font, width=width, height=height)
    button.grid(row=row, column=column, padx=10, pady=5)
    return button

def create_option_menu(parent, options, default, row, column):
    var = tk.StringVar(parent)
    var.set(default)
    option_menu = tk.OptionMenu(parent, var, *options)
    option_menu.grid(row=row, column=column, padx=10, pady=5)
    return var

def adjust_grid(event):
    global grid_columns
    grid_canvas.update_idletasks()
    width = grid_canvas.winfo_width()
    new_columns = max(1, width // 150)
    if new_columns != grid_columns:
        grid_columns = new_columns
        rearrange_grid()

def rearrange_grid():
    children = grid_frame.winfo_children()
    for index, widget in enumerate(children):
        widget.grid_forget()
        widget.grid(row=index // grid_columns, column=index % grid_columns, padx=5, pady=5, sticky="nsew")

def setup_ui(root):
    root.title("Book Recommendation System")
    root.geometry("920x800")
    root['background'] = '#3C5291'
    root.bind("<Configure>", adjust_grid)

    input_frame = tk.Frame(root, bg='#3C5291')
    input_frame.pack(side='left', fill='y')

    global grid_canvas, grid_frame
    grid_canvas = tk.Canvas(root, bg='#172038')
    grid_canvas.pack(side='right', fill='both', expand=True)

    grid_frame = tk.Frame(grid_canvas, bg='#172038')
    grid_window = grid_canvas.create_window((0, 0), window=grid_frame, anchor='nw')

    scrollbar = tk.Scrollbar(root, orient="vertical", command=grid_canvas.yview)
    grid_canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    def on_frame_configure(event):
        grid_canvas.configure(scrollregion=grid_canvas.bbox("all"))

    grid_frame.bind("<Configure>", on_frame_configure)
    grid_canvas.bind_all("<MouseWheel>", lambda event: grid_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    create_label(input_frame, "Genre:", "Poppins", '#8c92ac', 0, 0)
    genre_entry = create_entry(input_frame, 20, 0, 1)
    
    genre_list_frame = tk.Frame(input_frame, bg='#3C5291')
    genre_list_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=5)

    def add_genre():
        genre = genre_entry.get().strip()
        if genre:
            genre_frame = tk.Frame(genre_list_frame, bg='#8c92ac', relief='solid', padx=5, pady=2)
            genre_frame.pack(side='top', fill='x', pady=2)

            genre_label = tk.Label(genre_frame, text=genre, bg='#8c92ac')
            genre_label.pack(side='left')
            
            selected_genres.append(genre)

            def remove_genre():
                selected_genres.remove(genre_label.cget('text'))
                genre_frame.destroy()

            remove_button = tk.Button(genre_frame, text='x', command=remove_genre, bg='red', fg='white', padx=5)
            remove_button.pack(side='right')

            genre_entry.delete(0, 'end')

    create_button(input_frame, "+", add_genre, "Poppins", 3, 1, 0, 2)

    create_label(input_frame, "Min Price Point:", "Poppins", '#8c92ac', 2, 0)
    entry_minprice = create_entry(input_frame, 20, 2, 1)

    create_label(input_frame, "Max Price Point:", "Poppins", '#8c92ac', 3, 0)
    entry_maxprice = create_entry(input_frame, 20, 3, 1)

    create_label(input_frame, "Search Terms:", "Poppins", '#8c92ac', 4, 0)
    search_terms_entry = create_entry(input_frame, 20, 4, 1)

    create_button(input_frame, "Find Books!", findBooks, "Poppins", 10, 3, 5, 1)

    algorithms = ["Merge Sort", "Sleep Sort", "Shell Sort"]
    create_label(input_frame, "Sorting Method:", "Poppins", '#3C5291', 6, 0)
    create_option_menu(input_frame, algorithms, algorithms[0], 6, 1)

    sorting_var = ["Rating", "Review Count", "Page number", "Date", "Alphabetical"]
    create_label(input_frame, "Sort By:", "Poppins", '#3C5291', 7, 0)
    create_option_menu(input_frame, sorting_var, sorting_var[0], 7, 1)  


def loadData(file_path):
    if not isinstance(file_path, str):
        return None
    if not os.path.exists(file_path):
        downloaded_path = kagglehub.dataset_download("mdhamani/goodreads-books-100k")
        os.rename(downloaded_path + "/GoodReads_100k_books.csv", file_path)
    return pd.read_csv(file_path).head(50)

def loadImageFromURL(url):
    if not isinstance(url, str):
        return None
    if not url.startswith("http"):
        return None
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return ImageTk.PhotoImage(image)

img_width = 130
img_height = img_width * (20/15)
def populateGrid(dataframe):
    for widget in grid_frame.winfo_children():
        widget.destroy()
    for index, row in dataframe.iterrows():
        image = loadImageFromURL(row['img'])
        if image is not None:
            image = image._PhotoImage__photo.subsample(max(1, int(image.height() // img_height)))
            label = tk.Label(
                grid_frame,
                image=image,
                background="#3C5291",
                width=img_width,
                height=img_height
            )
        else:
            image = ImageTk.PhotoImage(Image.new('RGB', (int(img_width), int(img_height)), color='#172038'))
            label = tk.Label(
                grid_frame,
                image=image,
                text=row['title'],
                compound='center',
                background="#3C5291",
                fg="white",
                wraplength=img_width,
                justify="center",
                width=img_width,
                height=img_height
            )

        label.image = image
        label.grid(row=index // grid_columns, column=index % grid_columns, padx=5, pady=5, sticky="nsew")
        label.bind("<Enter>", lambda event, title=row['title'], author=row['author'], rating=row['rating']: on_hover(event, title, author, rating))
        label.bind("<Leave>", on_leave)
        label.bind("<Button-1>", lambda event, idx=index: on_click(event, idx))
        label.row_index = index

def on_hover(event, title, author, rating):
    event.widget.config(relief="raised", bd=0)
    tooltip = tk.Toplevel(event.widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{event.widget.winfo_rootx()}+{event.widget.winfo_rooty()}")
    label = tk.Label(tooltip, text=f"{title}\n{author}\nRating: {rating}", background="yellow", relief="solid", borderwidth=1)
    label.pack()
    event.widget.tooltip = tooltip

def on_leave(event):
    event.widget.config(relief="flat", bd=0)
    if hasattr(event.widget, 'tooltip'):
        event.widget.tooltip.destroy()
        del event.widget.tooltip

def on_click(event, index):
    print(f"Clicked on row index: {index}")
    print(sorted_books_df.iloc[index])
    webbrowser.open(sorted_books_df.iloc[index]['link'])
    
    
def findBooks():
    print(selected_genres)
    filters = {
        "genre": ",".join(selected_genres)
    }
    
    start_time = time.time()
    
    filter_result = book_db.filterBooks(filters, True)
    sorted_books_df = pd.DataFrame(filter_result)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"FilterBooks completed in {elapsed_time:.2f} seconds")

    populateGrid(sorted_books_df) # this takes the longest (5ish seconds), while everything else is instant

    pass
    
    
sorted_books_df = None
global book_db
csv_path = "DatasetManagement/GoodReads_100k_books.csv"
csv_path = os.path.abspath(csv_path)

if __name__ == "__main__":
    grid_columns = 3
    root = tk.Tk()
    setup_ui(root)    
    

    book_db = book_database_cpp.BookDatabase_Type1(csv_path)
    
    root.mainloop()
