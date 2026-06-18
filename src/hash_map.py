class HashMap:
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0
    
    def _hash(self, key):
        PRIME = 31
        h = 0
        key = str(key)
        for c in key:
            h = (h*PRIME + ord(c)) % self.capacity
        return h
    
    def put(self, key, value):
        hashKey = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[hashKey]):
            if k == key:
                self.buckets[hashKey][i] = (key, value)
                return
        self.buckets[hashKey].append((key,value))
        self.size += 1

    def get(self, key, default = None):
        hashKey = self._hash(key)
        for k,v in self.buckets[hashKey]:
            if key == k:
                return v
        return default
    
    def delete(self, key):
        hashKey = self._hash(key)
        new_bucket = []
        for k,v in self.buckets[hashKey]:
            if k == key:
                self.size -= 1
            else:
                new_bucket.append((k,v))
        self.buckets[hashKey] = new_bucket

    def keys(self):
        keyset = set()
        for items in self.buckets:
            for k, v in items:
                keyset.add(k)
        return keyset

    def __len__(self):
        return self.size
    
    def __getitem__(self, key):
        hashKey = self._hash(key)
        for k,v in self.buckets[hashKey]:
            if key == k:
                return v
        raise KeyError(key)
    
    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, item):
        hashKey = self._hash(item)
        for k,v in self.buckets[hashKey]:
            if k == item:
                return True
        return False