class MinHeap:
    def __init__(self):
        self.heap = []

    def insertKey(self, k):
        origin = self.heap
        idx = len(origin)
        origin.appen(k)
        parent_id = (idx - 1) / 2
        if k < parent:
            origin(idx), origin(parent_id) = origin(parent_id), origin(idx)
            

