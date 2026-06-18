class Node:
    def __init__(self, value, key = None):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, node):
        if self.head == None:
            self.head = node
            self.tail = node
            self.length += 1
            return
        self.tail.next = node
        node.prev = self.tail
        self.tail = node
        self.length += 1

    def prepend(self, node):
        if self.head == None:
            self.head = node
            self.tail = node
            self.length += 1
            return
        node.next = self.head
        self.head.prev = node
        self.head = node
        self.length += 1
    
    def __len__(self):
        return self.length
    
    def trim_left(self, count):
        while count > 0 and self.head is not None:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
            self.length -= 1
            count -= 1

    def trim_right(self, count):
        while count > 0 and self.tail is not None:
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
            else:
                self.head = None
            self.length -= 1
            count -= 1

    def delete(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        self.length -= 1

    
    

