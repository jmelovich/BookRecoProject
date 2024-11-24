# Helper function for shell sort to help with rearranging the position of elements after the first swap

def Swap(books, index1, index2):
    labels = ["title", "author", "genre", "description", "isbn", "img", "year", "rating_count", "page_count",
              "price", "link", "rating"]
    for i in range(len(labels)):
        category = labels[i]
        temp = books[category][index1]
        books[category][index1] = books[category][index2]
        books[category][index2] = temp

def Shell_Helper(books, iteration, current):
    if (current - iteration) >= 0 and type(current) == 'int':
        if books['rating'][current] > (books['rating'][current - iteration]):
            Swap(books, current, current - iteration)
            Shell_Helper(books['rating'], iteration, current - iteration)


# Main function for completing Shell sort on a list
def Shell_Sort(books, form):  # Function to rearrange elements within the list in ascending order
    size = len(books['rating'])
    iteration = size // 2
    while iteration > 0:
        for i in range(size):
            if i + iteration < size:
                if books['rating'][i + iteration] > books['rating'][i]:  # Swaps two elements if they are out of order
                    Swap(books, i, i + iteration)
                    Shell_Helper(books, iteration, i)  # Helper to continue swapping the current element
        iteration = iteration // 2
    if form == 'Ascending':
        for i in range(len(books['rating']) // 2):
            Swap(books, i, len(books['rating']) - 1 - i)


def Change_book(Updated_list, books, index):
    labels = ["title", "author", "genre", "description", "isbn", "img", "year", "rating_count", "page_count",
              "price", "link", "rating"]
    for i in range(len(labels)):
        Updated_list[labels[i]][index] = books[labels[i]][index]


def Quick_Helper(Updated_list, Original, books, index, iteration):
    size = len(books)
    leftlist = []
    leftlist_index = []
    rightlist = []
    rightlist_index = []
    pivot = books[size - 1]
    pivot_index = index[len(index) - 1]
    if size <= 1:
        Change_book(Updated_list, Original, pivot_index)
        return
    for i in range(size - 1):
        if books[i] >= pivot:
            leftlist.append(books[i])
            if iteration == 0:
                leftlist_index.append(i)
            else:
                leftlist_index.append(index[i])
        elif books[i] < pivot:
            rightlist.append(books[i])
            if iteration == 0:
                rightlist_index.append(i)
            else:
                rightlist_index.append(index[i])
    if len(leftlist) > 0:
        Quick_Helper(Updated_list, Original, leftlist, leftlist_index, 1)
    if len(rightlist) > 0:
        Quick_Helper(Updated_list, Original, rightlist, rightlist_index, 1)


def Quick_Sort(books, form):
    Updated_list = books
    Quick_Helper(Updated_list, books, books['rating'], [0], 0)
    if form == "Ascending":
        for i in range(len(Updated_list['rating']) // 2):
            Swap(Updated_list, i, len(Updated_list['rating']) - 1 - i)
    return Updated_list


def mergeSort(books, form):
    updated_list = books
    left = 0
    right = len(books['rating']) - 1
    mergeSortHelper(books, left, right)


def mergeSortHelper(books, left, right):
    if left < right:
        mid = left + (right - left) // 2
        mergeSortHelper(books, left, mid)
        mergeSortHelper(books, mid + 1, right)
        merge(books, left, mid, right)


def merge(books, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    left_books = {}
    right_books = {}
    labels = ["title", "author", "genre", "description", "isbn", "img", "year", "rating_count", "page_count",
              "price", "link", "rating"]

    for i in range(n1):
        for x in range(len(labels)):
            left_books[labels[x]][i] = books[labels[x]][left + i]
    for j in range(n2):
        for y in range(len(labels)):
            right_books[labels[y]][j] = books[labels[y]][mid + 1 + j]

    i = 0
    j = 0
    k = left
    while i < n1 and j < n2:
        if left_books[i] <= right_books[j]:
            for x in range(len(labels)):
                books[labels[x]][k] = left_books[labels[x]][i]
            i += 1
        else:
            for x in range(len(labels)):
                books[labels[x]][k] = right_books[labels[x]][j]
            j = j + 1
        k = k + 1
    while i < n1:
        for x in range(len(labels)):
            books[labels[x]][k] = left_books[labels[x]][i]
        i = i + 1
        k = k + 1
    while j < n2:
        for x in range(len(labels)):
            books[labels[x]][k] = right_books[labels[x]][j]
        j = j + 1
        k = k + 1
'''
def mergeSortSwap(books, index1, index2):
    temp = books[index1]
    books[index1] = books[index2]
    books[index2] = temp


def mergeSort(books, form):
    left = 0
    right = len(books['rating']) - 1
    mergeSortHelper(books, left, right)
    if form == "Descending":
        for i in range(len(books) // 2):
            mergeSortSwap(books, i, len(books) - 1 - i)


def mergeSortHelper(books, left, right):
    if left < right:
        mid = left + (right - left) // 2
        mergeSortHelper(books, left, mid)
        mergeSortHelper(books, mid + 1, right)
        merge(books, left, mid, right)


def merge(books, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    left_books = []
    left_indices = []
    right_books = []
    right_indices = []

    # Fill the left_books and right_books lists
    for i in range(n1):
        x = left + i
        left_books.append(books['rating'][left + i])
    for j in range(n2):
        right_books.append(books['rating'][mid + 1 + j])

    i = 0
    j = 0
    k = left

    # Merge the two sublists back into the main list
    while i < n1 and j < n2:
        if left_books[i] <= right_books[j]:
            books['raiting'][k] = left_books[i]
            i += 1
        else:
            books['rating'][k] = right_books[j]
            j += 1
        k += 1

    # If there are any remaining elements in left_books
    while i < n1:
        books['rating'][k] = left_books[i]
        i += 1
        k += 1

    # If there are any remaining elements in right_books
    while j < n2:
        books['rating'][k] = right_books[j]
        j += 1
        k += 1
        
'''