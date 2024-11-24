# Helper function for shell sort to help with rearranging the position of elements after the first swap
import copy


def Swap(books, index1, index2):
    labels = ["title", "author", "genre", "description", "isbn", "img", "year", "rating_count", "page_count",
              "price", "link", "rating"]
    for i in range(len(labels)):
        category = labels[i]
        temp = books[category][index1]
        books[category][index1] = books[category][index2]
        books[category][index2] = temp

def Shell_Helper(books, iteration, current, form):
    if form == 'Ascending':
        if (current - iteration) >= 0:
            if books['rating'][current] < (books['rating'][current - iteration]):
                Swap(books, current, current - iteration)
                Shell_Helper(books, iteration, current - iteration, form)
    if form == 'Descending':
        if (current - iteration) >= 0:
            if books['rating'][current] > (books['rating'][current - iteration]):
                Swap(books, current, current - iteration)
                Shell_Helper(books, iteration, current - iteration, form)


# Main function for completing Shell sort on a list
def Shell_Sort(books, form):  # Function to rearrange elements within the list in ascending order
    if form == 'Ascending':
        size = len(books['rating'])
        iteration = size // 2
        while iteration > 0:
            for i in range(size):
                if i + iteration < size:
                    if books['rating'][i + iteration] < books['rating'][i]:  # Swaps two elements if they are out of order
                        Swap(books, i, i + iteration)
                        Shell_Helper(books, iteration, i, form)  # Helper to continue swapping the current element
            iteration = iteration // 2
    elif form == 'Descending':
        size = len(books['rating'])
        iteration = size // 2
        while iteration > 0:
            for i in range(size):
                if i + iteration < size:
                    if books['rating'][i + iteration] > books['rating'][i]:  # Swaps two elements if they are out of order
                        Swap(books, i, i + iteration)
                        Shell_Helper(books, iteration, i, form)  # Helper to continue swapping the current element
            iteration = iteration // 2


def Change_book(Updated_list, books, pivot_index, current_index):
    labels = ["title", "author", "genre", "description", "isbn", "img", "year", "rating_count", "page_count",
              "price", "link", "rating"]
    for i in range(len(labels)):
        Updated_list[labels[i]][current_index] = books[labels[i]][pivot_index]

def Quick_Helper(Updated_list, Original, books, index, current_index, iteration, form):
    size = len(books)
    leftlist = []
    leftlist_index = []
    rightlist = []
    rightlist_index = []
    pivot = books[size - 1]
    pivot_index = index[len(index) - 1]
    if form == 'Descending':
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
    elif form == 'Ascending':
        for i in range(size - 1):
            if books[i] <= pivot:
                leftlist.append(books[i])
                if iteration == 0:
                    leftlist_index.append(i)
                else:
                    leftlist_index.append(index[i])
            elif books[i] > pivot:
                rightlist.append(books[i])
                if iteration == 0:
                    rightlist_index.append(i)
                else:
                    rightlist_index.append(index[i])
    if len(leftlist) > 0:
        current_index = Quick_Helper(Updated_list, Original, leftlist, leftlist_index, current_index, 1, form)
    Change_book(Updated_list, Original, pivot_index, current_index)
    current_index += 1
    if len(rightlist) > 0:
        current_index = Quick_Helper(Updated_list, Original, rightlist, rightlist_index, current_index, 1, form)

    return current_index



def Quick_Sort(books, form):
    Updated_list = copy.deepcopy(books)
    current_index = 0
    index = []
    for i in range(len(books['rating'])):
        index.append(i)
    Quick_Helper(Updated_list, books, books['rating'], index, current_index, 0, form)
    return Updated_list


def mergeSort(books, left, right):
    if left < right:
        mid = left + (right - left) / 2
        mergeSort(books, left, mid)
        mergeSort(books, mid + 1, right)

        merge(books, left, mid, right)


def merge(books, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid
    left_books = []
    right_books = []

    for i in range(n1):
        left_books.append(books[left + i])
    for j in range(n2):
        right_books.append(books[mid + 1 + j])

    i = 0
    j = 0
    k = left

    while i < n1 and j < n2:
        if left_books[i] <= right_books[j]:
            books[k] = left_books[i]
            i = i + 1
        else:
            books[k] = right_books[j]
            j = j + 1
        k = k + 1
    while i < n1:
        books[k] = left_books[i]
        i = i + 1
        k = k + 1
    while j < n2:
        books[k] = right_books[j]
        j = j + 1
        k = k + 1
