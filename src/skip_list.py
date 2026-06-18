import random

class SkipNode:
    def __init__(self, value, levels):
        self.value = value
        self.next = [None] * levels


class SkipList:
    def __init__(self, max_levels):
        self.max_levels = max_levels
        self.head = SkipNode(None, max_levels)
        self.size = 0

    def _random_level(self):
        level = 1
        while random.random() < 0.5 and level < self.max_levels:
            level += 1
        return level

    def search(self, value):
        current = self.head
        for level in range(self.max_levels-1, -1,-1):
            while current.next[level] and current.next[level].value < value:
                current = current.next[level]
        current = current.next[0]
        return current is not None and current.value == value
    
    def insert(self, value):
        update = [None] * self.max_levels
        current = self.head
        for level in range(self.max_levels-1, -1, -1):
            while current.next[level] and current.next[level].value < value:
                current = current.next[level]
            update[level] = current
        
        level = self._random_level()

        new_node = SkipNode(value, level)
        for i in range(level):
            new_node.next[i] = update[i].next[i]
            update[i].next[i] = new_node

        self.size += 1

    def delete(self, value):
        update = [None] * self.max_levels
        current = self.head
        for level in range(self.max_levels-1, -1, -1):
            while current.next[level] and current.next[level].value < value:
                current = current.next[level]
            update[level] = current
        node = update[0].next[0]
        if node is None or node.value != value:
            return
        for i in range(self.max_levels):
            if update[i].next[i] != node:
                break
            update[i].next[i] = node.next[i]

        self.size -= 1

    def __len__(self):
        return self.size




        


