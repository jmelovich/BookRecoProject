# this is a very simple script I was using to test using a CPP class in Python

import os
import book_database_cpp
from src.BookDatabase.book_utils import get_text_embedding
import pandas as pd

# Create an instance of the concrete implementation

csv_path = "DatasetManagement/GoodReads_100k_books.csv"

# convert csv_path to absolute path
csv_path = os.path.abspath(csv_path)

db = book_database_cpp.BookDatabase_Type1(csv_path)

# Test the methods

# declare map of strings to strings
filters = {
    "genre": "Cultural, Poetry"
}



# result = db.printBooks(50)

# print(result)

test_result = db.filterBooks(filters, True)
pdf = pd.DataFrame(test_result)
print(pdf.head(50))