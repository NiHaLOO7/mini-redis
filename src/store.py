from src.hash_map import HashMap
from src.linked_list import Node, DoublyLinkedList
from src.lru_cache import LRUCache
from src.min_heap import MinHeap
from src.skip_list import SkipList, SkipNode
import time

class RedisStore:
    def __init__(self, capacity, aof = None):
        self.store = HashMap()
        self.expires = HashMap()
        self.lru = LRUCache(capacity)
        self.ttl_heap = MinHeap()
        self.aof = aof
    
    def set(self, key, value):
        self.store.put(key, value)
        self.lru.put(key, value)

    def get(self, key):
        self._cleanup_expired()
        value = self.store.get(key)
        if value is not None:
            self.lru.get(key)
        return value

    def delete(self, key):
        self.store.delete(key)
        self.lru.delete(key)

    def incr(self, key):
        # Removes the one % chance of more than O(1) during 
        # coillision everytime we use this value
        value = self.store.get(key, 0) + 1 
        self.store[key] = value
        self.lru.put(key, value)
        return value

    def exists(self, key):
        return key in self.store
    
    def _push(self, key, value, method):
        linked_list = DoublyLinkedList()
        if self.exists(key):
            linked_list = self.store[key]
        self.store.put(key, linked_list)
        self.lru.put(key, linked_list)
        getattr(linked_list, method)(Node(value))

    def _pop(self, key, is_left):
        if not self.exists(key):
            return None
        linked_list = self.store[key]
        node_to_remove = linked_list.head if is_left else linked_list.tail
        if node_to_remove is None:
            return None
        linked_list.delete(node_to_remove)
        self.lru.get(key)
        return node_to_remove.value

    def lpush(self, key, value):
        self._push(key, value, 'prepend')

    def rpush(self, key, value):
        self._push(key, value, 'append')

    def lpop(self, key):
        return self._pop(key, True)
    
    def rpop(self, key):
        return self._pop(key, False)
    
    def lrange(self, key, start, end):
        value_list = []
        if not self.exists(key) or end < start:
            return value_list
        linked_list = self.store[key]
        start = start if start >=0 else len(linked_list) + start
        end = end if end >=0 else len(linked_list) + end
        curr = linked_list.head
        curr_no = 0
        while curr is not None and curr_no <= end:
            if curr_no >= start:
                value_list.append(curr.value)
            curr = curr.next
            curr_no += 1
        self.lru.get(key)
        return value_list
    
    def hset(self, key, inner_key, inner_value):
        h_map = self.store.get(key, HashMap())
        h_map[inner_key] = inner_value
        self.store[key] = h_map
        self.lru.put(key, h_map)

    def hget(self, key, inner_key):
        if not self.exists(key):
            return None
        h_map = self.store.get(key)
        if inner_key not in h_map:
            return None
        self.lru.get(key)
        return h_map[inner_key]
    
    def hdel(self, key, inner_key):
        if not self.exists(key):
            return False
        h_map = self.store.get(key)
        if inner_key not in h_map:
            return False
        h_map.delete(inner_key)
        self.lru.get(key)
        return True

    def hgetall(self, key):
        if not self.exists(key):
            return None
        self.lru.get(key)
        return self.store.get(key)


    def sadd(self, key, value):
        h_map = self.store.get(key, HashMap())
        h_map[value] = True
        self.store[key] = h_map
        self.lru.put(key, h_map)
    
    def sismember(self, key, value):
        if not self.exists(key):
            return False
        return value in self.store.get(key)
    
    def srem(self, key, value):
        if not self.exists(key):
            return False
        h_set = self.store.get(key)
        if value not in h_set:
            return False
        h_set.delete(value)
        self.lru.get(key)
        return True
    
    def smembers(self, key):
        if not self.exists(key):
            return None
        self.lru.get(key)
        return self.store.get(key).keys()
    
    def zadd(self, key, score, value):
        skip_list = self.store[key] = self.store.get(key, SkipList(16))
        skip_list.insert((score, value))
        self.lru.put(key, skip_list)

    def zrem(self, key, score, value):
        if not self.exists(key):
            return False
        skip_list = self.store.get(key)
        if not skip_list.search((score, value)):
            return False
        skip_list.delete((score, value))
        self.lru.get(key)
        return True
    
    def zrange(self, key, start, end):
        value_list = []
        if not self.exists(key) or end < start:
            return value_list
        skip_list = self.store[key]
        start = start if start >=0 else len(skip_list) + start
        end = end if end >=0 else len(skip_list) + end
        curr = skip_list.head.next[0]
        curr_no = 0
        while curr is not None and curr_no <= end:
            if curr_no >= start:
                value_list.append(curr.value)
            curr = curr.next[0]
            curr_no += 1
        self.lru.get(key)
        return value_list
    

    def expire(self, key, exp_duration):
        curr_time = time.time()
        exp_time = curr_time + exp_duration
        self.expires[key] = exp_time
        self.ttl_heap.push((exp_time, key))

    def ttl(self, key):
        if key not in self.expires:
            return -1
        remaining_time = self.expires[key] - time.time()
        if remaining_time > 0:
            return remaining_time
        self.expires.delete(key)
        self.lru.delete(key)
        self.store.delete(key)
        if self.aof:
            self.aof.log(["DEL", key])
        return -2

    def _cleanup_expired(self):
        while len(self.ttl_heap) > 0 and self.ttl_heap.peek()[0] <= time.time():
            exp, key = self.ttl_heap.pop()
            if key in self.expires:
                self.expires.delete(key)
                self.lru.delete(key)
                self.store.delete(key)
                if self.aof:
                    self.aof.log(["DEL", key])


    
        
    


        