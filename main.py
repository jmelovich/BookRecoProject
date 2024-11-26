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
    create_option_menu, BookGridUI, load_genre_list, load_author_list, load_bookformat_list, load_title_list,
    genres_autocomplete_list, authors_autocomplete_list, bookformats_autocomplete_list, titles_autocomplete_list,
    CustomAutocompleteEntry
)


import book_database_cpp


class BookRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.selected_genres = []
        self.selected_authors = []
        self.selected_titles = []
        self.selected_bookformats = []
        self.sorted_books_df = None
        
        # Load the genre list for autocomplete
        load_genre_list()
        load_author_list()
        load_title_list()
        load_bookformat_list()
        
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

        # Author input with autocomplete
        create_label(self.input_frame, "Author:", "Poppins", '#8c92ac', 2, 0)
        self.author_entry = CustomAutocompleteEntry(
            self.input_frame,
            completevalues=authors_autocomplete_list,
            add_callback=self.add_author,  # Pass the callback for Enter key
            width=20,
            font=('Poppins', 10),
            bg='white',
            fg='black'
        )
        self.author_entry.grid(row=2, column=1, padx=10, pady=5)

        self.author_list_frame = tk.Frame(self.input_frame, bg='#3C5291')
        self.author_list_frame.grid(row=3, column=0, columnspan=2, sticky='w', padx=10, pady=5)

        create_button(self.input_frame, "+", self.add_author, "Poppins", 3, 1, 2, 2)

        # Title input with autocomplete
        create_label(self.input_frame, "Title:", "Poppins", '#8c92ac', 4, 0)
        self.title_entry = CustomAutocompleteEntry(
            self.input_frame,
            completevalues=titles_autocomplete_list,
            add_callback=self.add_title,  # Pass the callback for Enter key
            width=20,
            font=('Poppins', 10),
            bg='white',
            fg='black'
        )
        self.title_entry.grid(row=4, column=1, padx=10, pady=5)

        self.title_list_frame = tk.Frame(self.input_frame, bg='#3C5291')
        self.title_list_frame.grid(row=5, column=0, columnspan=2, sticky='w', padx=10, pady=5)

        create_button(self.input_frame, "+", self.add_title, "Poppins", 3, 1, 4, 2)

        # Book Format input with autocomplete
        create_label(self.input_frame, "Book Format:", "Poppins", '#8c92ac', 6, 0)
        self.bookformat_entry = CustomAutocompleteEntry(
            self.input_frame,
            completevalues=bookformats_autocomplete_list,
            add_callback=self.add_bookformat,  # Pass the callback for Enter key
            width=20,
            font=('Poppins', 10),
            bg='white',
            fg='black'
        )
        self.bookformat_entry.grid(row=6, column=1, padx=10, pady=5)

        self.bookformat_list_frame = tk.Frame(self.input_frame, bg='#3C5291')
        self.bookformat_list_frame.grid(row=7, column=0, columnspan=2, sticky='w', padx=10, pady=5)

        create_button(self.input_frame, "+", self.add_bookformat, "Poppins", 3, 1, 6, 2)

        # Search terms
        create_label(self.input_frame, "Search Terms:", "Poppins", '#8c92ac', 8, 0)
        self.search_terms_entry = create_entry(self.input_frame, 20, 8, 1)

        # Find books button
        create_button(self.input_frame, "Find Books!", self.find_books, "Poppins", 10, 3, 9, 1)

        # Sorting options
        algorithms = ["Merge Sort", "Shell Sort", "Quick Sort"]
        create_label(self.input_frame, "Sorting Method:", "Poppins", '#3C5291', 10, 0)
        self.sort_algorithm = create_option_menu(self.input_frame, algorithms, algorithms[0], 10, 1)

        sorting_var = ["Rating", "Review Count", "Page number", "Alphabetical"]
        create_label(self.input_frame, "Sort By:", "Poppins", '#3C5291', 11, 0)
        self.sort_by = create_option_menu(self.input_frame, sorting_var, sorting_var[0], 11, 1)

        sorting_order = ["Descending", "Ascending"]
        create_label(self.input_frame, "Sorting Order:", "Poppins", '#3C5291', 12, 0)
        self.order_by = create_option_menu(self.input_frame, sorting_order, sorting_order[0], 12, 1)

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

    def add_author(self):
        author = self.author_entry.get().strip()
        if author:
            author_frame = tk.Frame(self.author_list_frame, bg='#8c92ac', relief='solid', padx=5, pady=2)
            author_frame.pack(side='top', fill='x', pady=2)

            author_label = tk.Label(author_frame, text=author, bg='#8c92ac')
            author_label.pack(side='left')

            self.selected_authors.append(author)

            def remove_author():
                self.selected_authors.remove(author_label.cget('text'))
                author_frame.destroy()

            remove_button = tk.Button(author_frame, text='x', command=remove_author,
                                      bg='red', fg='white', padx=5)
            remove_button.pack(side='right')

            self.author_entry.delete(0, 'end')

    def add_title(self):
        title = self.title_entry.get().strip()
        if title:
            title_frame = tk.Frame(self.title_list_frame, bg='#8c92ac', relief='solid', padx=5, pady=2)
            title_frame.pack(side='top', fill='x', pady=2)

            title_label = tk.Label(title_frame, text=title, bg='#8c92ac')
            title_label.pack(side='left')

            self.selected_titles.append(title)

            def remove_title():
                self.selected_titles.remove(title_label.cget('text'))
                title_frame.destroy()

            remove_button = tk.Button(title_frame, text='x', command=remove_title,
                                      bg='red', fg='white', padx=5)
            remove_button.pack(side='right')

            self.title_entry.delete(0, 'end')

    def add_bookformat(self):
        bookformat = self.bookformat_entry.get().strip()
        if bookformat:
            bookformat_frame = tk.Frame(self.bookformat_list_frame, bg='#8c92ac', relief='solid', padx=5, pady=2)
            bookformat_frame.pack(side='top', fill='x', pady=2)

            bookformat_label = tk.Label(bookformat_frame, text=bookformat, bg='#8c92ac')
            bookformat_label.pack(side='left')

            self.selected_bookformats.append(bookformat)

            def remove_bookformat():
                self.selected_bookformats.remove(bookformat_label.cget('text'))
                bookformat_frame.destroy()

            remove_button = tk.Button(bookformat_frame, text='x', command=remove_bookformat,
                                      bg='red', fg='white', padx=5)
            remove_button.pack(side='right')

            self.bookformat_entry.delete(0, 'end')

    def on_book_click(self, event, index):
        print(f"Clicked on row index: {index}")
        print(self.sorted_books_df.iloc[index])
        webbrowser.open(self.sorted_books_df.iloc[index]['link'])
        
    def collect_parameters(self):
        parameters = {}
        # get the filters
        if self.selected_genres:
            parameters["genre"] = ",".join(self.selected_genres)
        # get the author(s), title, and bookformat
        # author is a list, so needs to be revised first
        parameters['titleFilter'] = self.entry_title.get()
        parameters['bookFormat'] = self.entry_bookformat.get()
        
        # get the sorting algorithm
        if self.sort_algorithm.get() == 'Shell Sort':
            parameters["sortMethod"] = 'shell'
        elif self.sort_algorithm.get() == 'Quick Sort':
            parameters["sortMethod"] = 'quick'
        elif self.sort_algorithm.get() == 'Merge Sort':
            parameters["sortMethod"] = 'merge'
        # get the sorting order
        if self.order_by.get() == 'Ascending':
            parameters["sortOrder"] = 'asc'
        elif self.order_by.get() == 'Descending':
            parameters["sortOrder"] = 'desc'
        # get the sorting criteria
        if self.sort_by.get() == 'Rating':
            parameters["sortBy"] = 'rating'
        elif self.sort_by.get() == 'Review Count':
            parameters["sortBy"] = 'review_count'
        elif self.sort_by.get() == 'Page number':
            parameters["sortBy"] = 'num_pages'
        elif self.sort_by.get() == 'Alphabetical':
            parameters["sortBy"] = 'title'
        
        return parameters

    def find_books(self):
        parameters = self.collect_parameters()
        print(parameters)
        start_time = time.time()       
        search_result = self.book_db.findBooks(parameters)   
        self.sorted_books_df = pd.DataFrame(search_result)
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
    return book_database_cpp.BookDatabase_Type0(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookRecommendationApp(root)
    root.mainloop()