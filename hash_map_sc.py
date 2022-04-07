# Name: Eric Tolson
# Description: Hash Map with Separate Chaining


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears hash map content
        """
        for i in range(self.buckets.length()):  # clear chains if not empty
            if self.buckets[i].length() != 0:
                self.buckets[i] = LinkedList()
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns value associated with key argument.
        Returns none if the key is not in the hash map.
        """
        index = self.hash_function(key) % self.capacity

        node = self.buckets[index].contains(key)  # find key and return value or None

        if node is not None:
            return node.value
        else:
            return None

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value arguments in hash map.
        Updates value if the key exists and adds
        the key/value pair otherwise.
        """
        index = self.hash_function(key) % self.capacity

        if self.buckets[index].length() == 0:  # add key/value node to index if empty
            self.buckets[index].insert(key, value)
            self.size += 1
        else:
            node = self.buckets[index].contains(key)  # replace value if key exists
            if node is not None:
                node.value = value
            else:
                self.buckets[index].insert(key, value)  # add to chain otherwise
                self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes the argument key and associated value from
        the hash map.
        """
        index = self.hash_function(key) % self.capacity

        if self.buckets[index].contains(key) is not None:  # remove key at index if there
            self.buckets[index].remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is
        in the hash map, False, otherwise.
        """
        index = self.hash_function(key) % self.capacity

        node = self.buckets[index].contains(key)  # search for key at index

        if node is not None:
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the hash table.
        """
        empty_buckets = 0

        for i in range(self.buckets.length()):  # iterate buckets and increment empty
            if self.buckets[i].length() == 0:
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        """
        Returns hash table load factor.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes hash table capacity to argument integer.
        """
        if new_capacity < 1:
            return None
        else:
            new_da = DynamicArray()  # append nodes to DA for later transfer to new map

            for i in range(self.buckets.length()):
                for node in self.buckets[i]:
                    new_da.append(node)

            self.clear()  # clear map

            self.buckets = DynamicArray()  # update buckets to new capacity/ update capacity
            for _ in range(new_capacity):
                self.buckets.append(LinkedList())

            self.capacity = new_capacity

            for i in range(new_da.length()):  # rehash existing key/value pairs into adjust map
                self.put(new_da[i].key, new_da[i].value)

    def get_keys(self) -> DynamicArray:
        """
        Returns a dynamic array containing all of
        the keys in the hash map.
        """
        new_da = DynamicArray()

        for i in range(self.buckets.length()):
            for node in self.buckets[i]:
                new_da.append(node.key)

        return new_da
