def mergeSort(arr):
    if len(arr) <= 1:
        return arr
    middle = len(arr) // 2
    left = mergeSort(arr[: middle])
    right = mergeSort(arr[middle:])

    i_left = 0
    i_right = 0

    for i in range(len(arr)):
        if i_left == middle:
            arr[i] = right[i_right]
            i_right += 1
        elif i_right == len(arr) - middle:
            arr[i] = left[i_left]
            i_left += 1
        elif left[i_left] < right[i_right]:
            arr[i] = left[i_left]
            i_left += 1
        else:
            arr[i] = right[i_right]
            i_right += 1
    return arr

print(mergeSort([3,6,8,10,1,2,1]))
