def partition(arr, low, high):
    pivot = arr[high]
    i = low -1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)

def quickSortInPlace(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quickSortInPlace(arr, low, pi - 1)
        quickSortInPlace(arr, pi + 1, high)

arr = [10, 7, 9, 8, 1, 5]
print(arr)
quickSortInPlace(arr, 0, len(arr) -1)
print(arr)
