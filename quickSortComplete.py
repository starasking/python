def partition(arr, low, high):
    index = (high + low)//2
    pivot = arr[index]
    arr[index], arr[high] = arr[high], arr[index]

    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    up = i
    for j in range(up+1, high):
        if arr[j] == pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    down = i + 1
    return (up, down)


def quickSort(arr, low, high):
    while (low < high):
        (up, down) = partition(arr, low, high)
        if(up - low) > (high - down):
            quickSort(arr, low, up)
            low = down
        else:
            quickSort(arr, down, high)
            high = up

arr = [10, 7, 9, 5, 1, 5]
print(arr)
quickSort(arr, 0, len(arr) -1)
print(arr)

