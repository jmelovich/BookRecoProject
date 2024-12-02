# The Book Recommendation System
_This repo is for Project 3, COP3530_

This tool is designed to help a user find a book (or books) they are most likely to enjoy reading.
The UI and all frontend interactions are programmed in Python, and all the backend is powered by a custom C++ class exposed to Python via Pybind11.
The tool is powered by a 100,000 entry dataset (found [here](https://www.kaggle.com/datasets/mdhamani/goodreads-books-100k/data)) where each entry contains the books title, author, genre, description, rating, and more.

## How It Works
The tool works by the user inputting their search parameters and hitting the 'Find Books!' button.

This has two primary stages: the filtering stage, and the sorting stage.

The Genre, Author, and Title user inputs act as a filter on the dataset.
Only books that contain all of the listed genres will pass the genre filter (AND filter).
All books with at least one of the listed authors will pass the author filter (OR filter).
And all books with a direct substring match from one of the listed titles will pass the title filer (OR filter.)

Then the remaining, filtered books will be sorted by the metric selected in the 'Sort By' user input dropdown, in the direction set by the 'Sorting Order' dropdown (descending by default).
The sorting algorithm employed to sort the remaining books can be selected from the 'Sorting Method' dropdown, with options for _Merge Sort_, _Shell Sort_, and _Quick Sort_. The amount of time it takes for the filtering & sorting operations to complete is output in the application log for comparison. Additionally, the 'Disable Cover Art?' checkbox can be flagged true to disable loading the book cover art in the grid- these must be loaded over the internet, so checking this box will show a substantial speed improvement in displaying the sorting results. Hovering your mouse over each book entry in the grid will also display information about that book, and clicking on it will open your web browser to the GoodReads page for said book.

There is also, with additional setup, a Vector Similarity Search feature implemented in this tool (not to address any project requirements, just as a learning exercise). Assuming its set up correctly, it can be used very simply and powerfully:

First apply any filters to the dataset you desire. Then, input a search query in the 'Vector Search Query' input box- since this does not employ direct substring matching, this query just needs to be related to the type of book you are looking for. (For books related to dungeons & dragons for example, one could just put 'dnd'). Then, in the 'SortBy' dropdown, select 'Vector Similarity'. Ensure 'Sorting Order' is set to 'Descending' (otherwise it will display the books LEAST related to your query) and then simply click 'Find Books!'. 


## Installing/Running The Project
Clone the repo and install the dependencies using:

```pip install -r requirements.txt```

Then the book_database.cpp c++ class needs to be compiled:
Open a terminal in the root of this project, then:

```cd src/BookDatabase```

```pip install .```

Then, if everything is set up correctly, run the ```main.py``` file.
Upon first run, the dataset should automatically be downloaded from Kagglehub. If this does not work, the dataset can be manually downloaded (from [here](https://www.kaggle.com/datasets/mdhamani/goodreads-books-100k/data)) and the ```GoodReads_100k_books.csv``` file placed in the data/ folder.


### Setting Up The Vector Search
These steps should be sufficient for all core components of this tool to function, but there are some additional steps that need to be taken for the Vector Search features to work correctly:

The Vector Search feature requires access to an OpenAI compatible endpoint, running a text-embedding model. In the project demonstration video, the Vector Search feature shown was using a locally-run inference server running the text-embedding model ```nomic embed text v1 5```. If you have an OpenAI account with API access, however, you can simply swap out the value for _API_KEY_ with your OpenAI API key in the _src/BookDatabase/book_utils.py_ file. Then try to perform a vector similarity search in the tool, and it should automatically start to generate the embeddings file (which only needs to be compelted once, and is saved for future use). After this completes the Vector Search features should be fully functional.
