# Helper function for shell sort to help with rearranging the position of elements after the first swap
def Shell_Helper(numbers, iteration, current):
    if (current - iteration) >= 0:
        if numbers[current] < (numbers[current - iteration]):
            temp = numbers[current]
            numbers[current] = numbers[current - iteration]
            numbers[current - iteration] = temp
            Shell_Helper(numbers, iteration, current - iteration)


# Main function for completing Shell sort on a list
def Shell_Sort(numbers):  # Function to rearrange elements within the list in ascending order
    size = len(numbers)
    iteration = size // 2
    while iteration > 0:
        for i in range(size):
            if i + iteration < size:
                if numbers[i + iteration] < numbers[i]:  # Swaps two elements if they are out of order
                    temp = numbers[i]
                    numbers[i] = numbers[i + iteration]
                    numbers[i + iteration] = temp
                    Shell_Helper(numbers, iteration, i)  # Helper to continue swapping the current element
        iteration = iteration // 2


def Quick_Helper(Updated_list, numbers):
    size = len(numbers)
    leftlist = []
    rightlist = []
    pivot = numbers[size - 1]
    for i in range(size - 1):
        if numbers[i] <= pivot:
            leftlist.append(numbers[i])
        elif numbers[i] > pivot:
            rightlist.append(numbers[i])
    if len(leftlist) > 0:
        Quick_Helper(Updated_list, leftlist)
    Updated_list.append(pivot)
    if len(rightlist) > 0:
        Quick_Helper(Updated_list, rightlist)


def Quick_Sort(numbers):
    Updated_list = []
    Quick_Helper(Updated_list, numbers)
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
