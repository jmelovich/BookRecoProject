# this is a very simple script I was using to test using a CPP class in Python

import book_database_cpp
import numpy as np

# Create an instance of the concrete implementation
db = book_database_cpp.SimpleBookDatabase("test.csv")

# Test the methods
query = np.array([[1.0, 2.0], [3.0, 4.0]])
result = db.findBooks(query)
test_result = db.testFunc("hello")

print(result)
print(test_result)