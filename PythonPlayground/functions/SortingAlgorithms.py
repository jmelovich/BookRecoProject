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
