# Name: Eric Tolson
# OSU Email: tolsone@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/11/22
# Description: Hash Map with Open Addressing


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
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
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears hash map content
        """
        for i in range(self.buckets.length()):  # iterate DA and clear content
            if self.buckets[i] is not None:
                self.buckets[i] = None

        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        Returns None if key is not in the map.
        """
        index = self.hash_function(key) % self.capacity

        if self.buckets[index] is None:  # if key index is None
            return
        elif self.buckets[index].key == key:  # if has index key equals argument and is not tombstone
            if self.buckets[index].is_tombstone is False:
                return self.buckets[index].value
            else:
                return
        else:
            probe_count = 1  # quadratic probe to search for key with same logic as above
            probe_index = self.quadratic_probing(index, probe_count)

            while self.buckets[probe_index] is not None:
                if self.buckets[probe_index].key == key:
                    if self.buckets[probe_index].is_tombstone is False:
                        return self.buckets[probe_index].value
                    else:
                        return
                probe_count += 1
                probe_index = self.quadratic_probing(index, probe_count)

    def quadratic_probing(self, index: int, probe_count: int) -> int:
        """
        Takes hashed index and probe count
        arguments and returns resulting
        quadratic probe index. Helper function.
        """
        return (index + (probe_count ** 2)) % self.capacity

    def put(self, key: str, value: object) -> None:
        """
        Inserts key, value pair arguments into
        the hash table.
        """
        if self.table_load() >= .5:  # double table capacity if load is too great.
            self.resize_table(self.capacity * 2)

        entry = HashEntry(key, value)  # create hash entry

        index = self.hash_function(key) % self.capacity  # generate index and insert if available

        if self.buckets[index] is None:
            self.buckets[index] = entry
            self.size += 1
        elif self.buckets[index].is_tombstone is True:
            self.buckets[index] = entry
            self.size += 1
        elif self.buckets[index].key == key:
            self.buckets[index] = entry
        else:
            probe_count = 1  # probe to find available index
            probe_index = self.quadratic_probing(index, probe_count)

            while self.buckets[probe_index] is not None:
                if self.buckets[probe_index].is_tombstone is True:
                    self.buckets[probe_index] = entry
                    self.size += 1
                    return
                elif self.buckets[probe_index].key == key:
                    self.buckets[probe_index] = entry
                    return
                probe_count += 1
                probe_index = self.quadratic_probing(index, probe_count)

            self.buckets[probe_index] = entry
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and associated value
        from the hash map.
        """
        # quadratic probing required

        index = self.hash_function(key) % self.capacity

        if self.buckets[index] is None:  # if key index is None
            return
        elif self.buckets[index].key == key:  # if index key equals argument, remove if not already removed
            if self.buckets[index].is_tombstone is False:
                self.buckets[index].is_tombstone = True
                self.size -= 1
            return
        else:
            probe_count = 1  # quadratic probe to search for key and remove if not already removed
            probe_index = self.quadratic_probing(index, probe_count)

            while self.buckets[probe_index] is not None:
                if self.buckets[probe_index].key == key:
                    if self.buckets[probe_index].is_tombstone is False:
                        self.buckets[probe_index].is_tombstone = True
                        self.size -= 1
                    return
                probe_count += 1
                probe_index = self.quadratic_probing(index, probe_count)

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the hash map contains the key,
        false otherwise.
        """
        if self.size == 0:  # if there are no keys
            return False
        else:
            index = self.hash_function(key) % self.capacity

            if self.buckets[index] is None:  # check initial index for key
                return False
            elif self.buckets[index].is_tombstone is True:
                return False
            elif self.buckets[index].key == key:
                return True
            else:
                probe_count = 1  # quadratic probe to search for key
                probe_index = self.quadratic_probing(index, probe_count)

                while self.buckets[probe_index] is not None:
                    if self.buckets[index].is_tombstone is True:
                        return False
                    elif self.buckets[probe_index].key == key:
                        return True
                    probe_count += 1
                    probe_index = self.quadratic_probing(index, probe_count)

                return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_buckets = 0

        for i in range(self.buckets.length()):  # iterate DA and increment empties.
            if self.buckets[i] is None:
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize hash table to new capacity input.
        """
        if new_capacity < 1 or new_capacity < self.size:  # return none if no need for resize
            return
        else:
            new_da = DynamicArray()  # create array for hash entry storage
            for i in range(self.buckets.length()):  # append hash entries to new array
                if self.buckets[i] is not None:
                    if self.buckets[i].is_tombstone is False:
                        new_da.append(self.buckets[i])

            self.buckets = DynamicArray()  # reset buckets

            for _ in range(new_capacity):
                self.buckets.append(None)

            self.size = 0  # reset size and capacity
            self.capacity = new_capacity

            for i in range(new_da.length()):  # rehash existing key/value pairs into adjusted map
                self.put(new_da[i].key, new_da[i].value)

    def get_keys(self) -> DynamicArray:
        """
        Returns a Dynamic Array containing all of
        the keys in the hashmap.
        """
        new_da = DynamicArray()

        for i in range(self.buckets.length()):  # append all active keys to DA for return
            if self.buckets[i] is not None:
                if self.buckets[i].is_tombstone is False:
                    new_da.append(self.buckets[i].key)

        return new_da


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
