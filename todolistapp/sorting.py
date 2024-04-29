def merge_sort(lst):  # Define a function called merge_sort that takes a list as input
    if len(lst) <= 1:  # If the length of the list is less than or equal to 1
        return lst  # Return the list as it is already sorted

    mid = len(lst) // 2  # Calculate the middle index of the list
    # Recursively call merge_sort on the left half of the list
    left_list = merge_sort(lst[:mid])
    # Recursively call merge_sort on the right half of the list
    right_list = merge_sort(lst[mid:])

    # Return the result of merging the sorted left and right lists
    return merge(left_list, right_list)


def merge(left, right):  # Define a function called merge that takes two lists as input
    sorted_list = []  # Create an empty list to store the sorted elements
    while left and right:  # While both the left and right lists are not empty
        # If the deadline of the first element in the left list is less than or equal to the deadline of the first element in the right list
        if left[0].deadline <= right[0].deadline:
            # Append the first element of the left list to the sorted list and remove it from the left list
            sorted_list.append(left.pop(0))
        else:  # Otherwise
            # Append the first element of the right list to the sorted list and remove it from the right list
            sorted_list.append(right.pop(0))

    while left:  # While the left list is not empty
        # Append the remaining elements of the left list to the sorted list and remove them from the left list
        sorted_list.append(left.pop(0))

    while right:  # While the right list is not empty
        # Append the remaining elements of the right list to the sorted list and remove them from the right list
        sorted_list.append(right.pop(0))

    return sorted_list  # Return the sorted list
