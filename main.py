import os
import webbrowser
import pandas as pd
import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteEntry
import kagglehub
import time
import SortingAlgorithms as sr

from src.ui_utils import (
    create_label, create_entry, create_button, 
    create_option_menu, BookGridUI, load_genre_list,
    genres_autocomplete_list, CustomAutocompleteEntry
)


import book_database_cpp



class BookRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.selected_genres = []
        self.sorted_books_df = None
        
        # Load the genre list for autocomplete
        load_genre_list()
        
        self.setup_ui()
        
        csv_path = os.path.abspath("DatasetManagement/GoodReads_100k_books.csv")
        self.book_db = load_data_cpp(csv_path)

    def setup_ui(self):
        self.root.title("Book Recommendation System")
        self.root.geometry("920x800")
        self.root['background'] = '#3C5291'

        # Create main frames
        self.input_frame = tk.Frame(self.root, bg='#3C5291')
        self.input_frame.pack(side='left', fill='y')

        # Initialize book grid
        self.book_grid = BookGridUI(self.root)
        self.root.bind("<Configure>", self.book_grid.adjust_grid)

        # Setup input controls
        self.setup_input_controls()

    def setup_input_controls(self):
        # Genre input with autocomplete
        create_label(self.input_frame, "Genre:", "Poppins", '#8c92ac', 0, 0)
        self.genre_entry = CustomAutocompleteEntry(
            self.input_frame,
            completevalues=genres_autocomplete_list,
            add_callback=self.add_genre,  # Pass the callback for Enter key
            width=20,
            font=('Poppins', 10),
            bg='white',
            fg='black'
        )
        self.genre_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.genre_list_frame = tk.Frame(self.input_frame, bg='#3C5291')
        self.genre_list_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=5)
        
        create_button(self.input_frame, "+", self.add_genre, "Poppins", 3, 1, 0, 2)

        # Price inputs
        # create_label(self.input_frame, "Min Price Point:", "Poppins", '#8c92ac', 2, 0)
        # self.entry_minprice = create_entry(self.input_frame, 20, 2, 1)

        # create_label(self.input_frame, "Max Price Point:", "Poppins", '#8c92ac', 3, 0)
        # self.entry_maxprice = create_entry(self.input_frame, 20, 3, 1)

        # Search terms
        create_label(self.input_frame, "Search Terms:", "Poppins", '#8c92ac', 5, 0)
        self.search_terms_entry = create_entry(self.input_frame, 20, 5, 1)

        # Find books button
        create_button(self.input_frame, "Find Books!", self.find_books, "Poppins", 10, 3, 6, 1)

        # Sorting options
        algorithms = ["Merge Sort", "Shell Sort", "Quick Sort"]
        create_label(self.input_frame, "Sorting Method:", "Poppins", '#3C5291', 7, 0)
        self.sort_algorithm = create_option_menu(self.input_frame, algorithms, algorithms[0], 7, 1)

        sorting_var = ["Rating", "Review Count", "Page number", "Date", "Alphabetical"]
        create_label(self.input_frame, "Sort By:", "Poppins", '#3C5291', 8, 0)
        self.sort_by = create_option_menu(self.input_frame, sorting_var, sorting_var[0], 8, 1)

        sorting_order = ["Ascending", "Descending"]
        create_label(self.input_frame, "Sorting Order:", "Poppins", '#3C5291', 9, 0)
        self.order_by = create_option_menu(self.input_frame, sorting_order, sorting_order[0], 9, 1)

        # Author
        # TODO: Add Autocomplete for authors; allow user to select one or multiple authors
        create_label(self.input_frame, "Author(s):", "Poppins", '#8c92ac', 2, 0)
        self.entry_author = create_entry(self.input_frame, 20, 2, 1)

        # Title
        # TODO: Add Autocomplete for Title; allow user to select title
        create_label(self.input_frame, "Title:", "Poppins", '#8c92ac', 3, 0)
        self.entry_title = create_entry(self.input_frame, 20, 3, 1)

        # Bookformat
        # TODO: Add Autocomplete for Bookformat; allow user to select bookformat
        create_label(self.input_frame, "Bookformat:", "Poppins", '#8c92ac', 4, 0)
        self.entry_bookformat = create_entry(self.input_frame, 20, 4, 1)

        # Page Count
        # TODO: Add page count option for people to select

        # Total Ratings
        # TODO: ADD total ratings option for people to select

    def add_genre(self):
        genre = self.genre_entry.get().strip()
        if genre:
            genre_frame = tk.Frame(self.genre_list_frame, bg='#8c92ac', relief='solid', padx=5, pady=2)
            genre_frame.pack(side='top', fill='x', pady=2)

            genre_label = tk.Label(genre_frame, text=genre, bg='#8c92ac')
            genre_label.pack(side='left')
            
            self.selected_genres.append(genre)

            def remove_genre():
                self.selected_genres.remove(genre_label.cget('text'))
                genre_frame.destroy()

            remove_button = tk.Button(genre_frame, text='x', command=remove_genre, 
                                    bg='red', fg='white', padx=5)
            remove_button.pack(side='right')

            self.genre_entry.delete(0, 'end')

    def on_book_click(self, event, index):
        print(f"Clicked on row index: {index}")
        print(self.sorted_books_df.iloc[index])
        webbrowser.open(self.sorted_books_df.iloc[index]['link'])

    def find_books(self):
        print(self.selected_genres)
        filters = {
            "genre": ",".join(self.selected_genres)
        }
        
        start_time = time.time()
        filter_result = self.book_db.filterBooks(filters, True)
        if self.sort_algorithm.get() == 'Shell Sort':
            if self.sort_by.get() == "Rating":
                if self.order_by.get() == 'Ascending':
                    sr.Shell_Sort(filter_result, 'Ascending')
                elif self.order_by.get() == 'Descending':
                    sr.Shell_Sort(filter_result, 'Descending')
        if self.sort_algorithm.get() == 'Quick Sort':
            if self.sort_by.get() == "Rating":
                if self.order_by.get() == 'Ascending':
                    filter_result = sr.Quick_Sort(filter_result, 'Ascending')
                elif self.order_by.get() == 'Descending':
                    filter_result = sr.Quick_Sort(filter_result, 'Descending')
        if self.sort_algorithm.get() == 'Merge Sort':
            if self.sort_by.get() == "Rating":
                if self.order_by.get() == 'Ascending':
                    sr.mergeSort(filter_result, 'Ascending')
                elif self.order_by.get() == 'Descending':
                    sr.mergeSort(filter_result, 'Descending')
        self.sorted_books_df = pd.DataFrame(filter_result)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"FilterBooks completed in {elapsed_time:.2f} seconds")
        self.book_grid.populate_grid(self.sorted_books_df, self.on_book_click)

def load_data(file_path):
    if not isinstance(file_path, str):
        return None
    if not os.path.exists(file_path):
        downloaded_path = kagglehub.dataset_download("mdhamani/goodreads-books-100k")
        os.rename(downloaded_path + "/GoodReads_100k_books.csv", file_path)
    return pd.read_csv(file_path).head(50)

def load_data_cpp(file_path):
    if not isinstance(file_path, str):
        return None
    if not os.path.exists(file_path):
        downloaded_path = kagglehub.dataset_download("mdhamani/goodreads-books-100k")
        os.rename(downloaded_path + "/GoodReads_100k_books.csv", file_path)
    return book_database_cpp.BookDatabase_Type1(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookRecommendationApp(root)
    root.mainloop()