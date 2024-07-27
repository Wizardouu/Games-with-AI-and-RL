


def find_difference_index(array1, array2):
    for i in range(len(array1)):
        for j in range(len(array1[0])):
            if array1[i][j] != array2[i][j]:
                return (i, j)  # Return the index where the difference is found
    return None


def find_first_zero_cell(arr):
    for i in range(8, -1, -1):
        for j in range(8,-1, -1):
            if arr[i][j] == 0:
                return (i, j)