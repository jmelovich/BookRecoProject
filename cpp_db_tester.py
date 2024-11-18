# this is a very simple script I was using to test using a CPP class in Python

import os
import book_database_cpp
from src.BookDatabase.book_utils import get_text_embedding

# Create an instance of the concrete implementation

csv_path = "DatasetManagement/GoodReads_100k_books.csv"

# convert csv_path to absolute path
csv_path = os.path.abspath(csv_path)

db = book_database_cpp.SimpleBookDatabase(csv_path, 50)

# Test the methods

test_result = db.testFunc("hello")
print(test_result)

result = db.printBooks(50)

print(result)
