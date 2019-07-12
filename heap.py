import random

class MinHeap:
    def __init__(self):
        self.heap = []

    def insertKey(self, k):
        origin = self.heap
        idx = len(origin)
        origin.append(k)
        parent_idx = (idx - 1) // 2
        if idx == 0:
            self.heap = origin
        else:
            while origin[idx] < origin[parent_idx]:
                origin[idx], origin[parent_idx] = origin[parent_idx], origin[idx]
                idx = parent_idx
                if idx == 0:
                    break
                else:
                    parent_idx = (idx - 1) // 2
        self.heap = origin

    def delete(self, k):
        origin = self.heap
        if k not in origin:
            return
        else:
            idx = origin.index(k)
            last_idx = len(origin) - 1
            origin[idx], origin[last_idx] = origin[last_idx], origin[idx]
            origin.pop()
            self.flowDown(idx)

    def flowDown(self, idx):
        origin = self.heap
        left_idx = idx * 2 + 1
        right_idx = idx * 2 + 2
        while right_idx < len(origin):
            if origin[idx] <= origin[left_idx] and origin[idx] <= origin[right_idx]:
                break
            elif origin[left_idx] <= origin[right_idx] and origin[idx] > origin[left_idx]:
                origin[idx], origin[left_idx] = origin[left_idx], origin[idx]
                idx = left_idx
            elif origin[left_idx] >= origin[right_idx] and origin[idx] > origin[right_idx]:
                origin[idx], origin[right_idx] = origin[right_idx], origin[idx]
                idx = right_idx
            left_idx = idx * 2 + 1
            right_idx = idx * 2 + 2
        if left_idx == len(origin) - 1 and origin[idx] > origin[left_idx]:
            origin[idx], origin[left_idx] = origin[left_idx], origin[idx]
            
heap = MinHeap()

dk = 0
for i in range(20):
    k = random.randint(1, 20)
    if i == 10:
        dk = k
    print(k)
    heap.insertKey(k)

print(heap.heap)
print('delete %d' % dk)
heap.delete(dk)
print(heap.heap)
