class MinHeap:
    def __init__(self):
        self.heap = []
        self.size = 0

    def _bubble_up(self, i):
        while i > 0:
            p_i = (i - 1) // 2
            if self.heap[i] >= self.heap[p_i]:
                break
            self.heap[p_i], self.heap[i] = self.heap[i], self.heap[p_i]
            i = p_i

    def _bubble_down(self, i):
        while True:
            smallest = i
            lc = 2*i + 1
            rc = 2*i + 2
            if lc < self.size and self.heap[lc] < self.heap[smallest]:
                smallest = lc
            if rc < self.size and self.heap[rc] < self.heap[smallest]:
                smallest = rc
            if smallest == i:
                break
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

    # def _bubble_down(self, i):    
        # while i < self.size:
        #     lc_i = i*2 + 1
        #     rc_i = i*2 + 2
        #     if lc_i >= self.size and rc_i >= self.size:
        #         break
        #     elif lc_i < self.size and rc_i < self.size:
        #         if self.heap[lc_i] > self.heap[i] < self.heap[rc_i]:
        #             break
        #         elif self.heap[lc_i] < self.heap[rc_i]:
        #             if self.heap[lc_i] < self.heap[i]:
        #                 self.heap[lc_i], self.heap[i] = self.heap[i], self.heap[lc_i]
        #                 i = lc_i
        #             elif self.heap[rc_i] < self.heap[i]:
        #                 self.heap[rc_i], self.heap[i] = self.heap[i], self.heap[rc_i]
        #                 i = rc_i
        #     elif lc_i < self.size and self.heap[lc_i] < self.heap[i]:
        #         self.heap[lc_i], self.heap[i] = self.heap[i], self.heap[lc_i]
        #         i = lc_i
        #     elif rc_i < self.size and self.heap[rc_i] < self.heap[i]:
        #         self.heap[rc_i], self.heap[i] = self.heap[i], self.heap[rc_i]
        #         i = rc_i
        #     else:
        #         break


    def push(self, value): 
        self.heap.append(value)
        self.size += 1
        self._bubble_up(self.size - 1)

    def pop(self):
        if self.size == 0:
            raise IndexError("heap is empty")
        min_val = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.size -= 1
        if self.size > 0:
            self._bubble_down(0)
        return min_val
    
    def peek(self):
        if self.size == 0:
            return None
        return self.heap[0]


    def heapify(self, arr):
        self.heap = arr
        self.size = len(arr)
        for i in range((self.size // 2)-1, -1, -1):
            self._bubble_down(i)

    def __len__(self):
        return self.size