from src.hash_map import HashMap
from src.linked_list import Node, DoublyLinkedList

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = HashMap()
        self.list = DoublyLinkedList()
    
    def get(self, key):
        if key not in self.map:
            return None
        node = self.map[key]
        self.list.delete(node)
        self.list.prepend(node)
        return node.value
    
    def put(self, key, value):
        #self.map[key] = Node(value)
        if key in self.map:
            node = self.map[key]
            node.value = value
            self.list.delete(node)
            self.list.prepend(node)
        else:
            if self.capacity == len(self.map):
                tail = self.list.tail
                self.list.delete(tail)
                self.map.delete(tail.key)
            node = Node(value, key)
            self.list.prepend(node)
            self.map[key] = node

    def delete(self, key):
        node = self.map[key]
        if node:
            self.list.delete(node)
            self.map.delete(key)
            

