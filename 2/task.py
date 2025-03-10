import math

alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
alphabet = dict(zip(alphabet, range(1, 34)))

def hash_func(str):
    hash_val = 0
    if len(str) > 10:
        str = str[0:10]
    str = str.lower()
    n = 9
    for char in str:
        hash_val += alphabet[char] * 34 ** n
        n -= 1
    return hash_val

class BPlusTree:

    def __init__(self, order, depth, keys, descedants = None, leaf = False, names = None, pointer = None):
        try:
            if (depth <= 3) and (depth >= 1) and (order <= 4) and (order >= 2):
                self.order = order
                self.depth = depth
                self.leaf = leaf
                if leaf:
                    if len(keys) > order - 1:
                        raise Exception("Wrong number of keys!")
                    self.keys = keys
                    if names:
                        if len(names) > order - 1:
                            raise Exception("Wrong number of names!")
                    else:
                        raise Exception("This tree is leaf, but also doesn't have names!")
                    if pointer:
                        self.pointer = pointer
                    self.descedants = None
                    self.names = names
                else:
                    if len(keys) > order - 1:
                        raise Exception("Wrong number of keys!")
                    self.keys = keys
                    if descedants:
                        if len(descedants) > order:
                            raise Exception("Wrong number of descedants!")
                    else:
                        raise Exception("This tree is not leaf, but also doesn't have descedants!")
                    self.descedants = descedants
                    self.names = None
            else:
                raise Exception("Depth or height out of range!")
        except Exception as e:
            print(e)

    def print_tree(self, cur_depth = 0, with_keys = True):
        depth = cur_depth
        print(" " * 4 * depth, end = "")
        if self.leaf:
            if with_keys:
                print(list(zip(self.keys, self.names)))
            else:
                print(self.names)
        else:
            print(self.keys)
        if self.descedants:
            for descedant in self.descedants:
                descedant.print_tree(cur_depth = cur_depth + 1, with_keys = with_keys)

    def insert_element(self, name, key = None):
        if key is None:
            key = hash_func(name)
        if self.leaf:
            if len(self.keys) < self.order - 1:
                self.keys = self.keys + [key]
                self.keys.sort()
                ind = self.keys.index(key)
                self.names.insert(ind, name)
                return None
            else:
                self.keys = self.keys + [key]
                self.keys.sort()
                middle_ind = math.floor(len(self.keys)/2)
                middle_value = self.keys[middle_ind]
                ind = self.keys.index(key)
                self.names.insert(ind, name)
                leaf1 = BPlusTree(order = self.order, depth = self.depth, keys = self.keys[:middle_ind], leaf = True, names = self.names[:middle_ind])
                leaf2 = BPlusTree(order = self.order, depth = self.depth, keys = self.keys[middle_ind:], leaf = True, names = self.names[middle_ind:], pointer = self.pointer)
                leaf1.pointer = leaf2
                if self.depth == 1:
                    self.keys = [middle_value]
                    self.leaf = False
                    self.names = None
                    leaf1.depth += 1
                    leaf2.depth += 1
                    self.descedants = [leaf1, leaf2]
                else:
                    return (leaf1, leaf2, middle_value)
        else:
            i = 0
            for k in self.keys:
                if key < k:
                    break
                else:
                    i += 1
            if len(self.descedants) <= i:
                if self.descedants[0].leaf:               
                    newdescedant = BPlusTree(order = self.order, depth = self.depth + 1, keys = [key], leaf = True, names = [name])
                    newdescedant.pointer = self.descedants[-1].pointer
                    self.descedants[-1].pointer = newdescedant
                    self.descedants.append(newdescedant)
                    self.keys.append(key)
                    res = None
                else:
                    newdescedant = BPlusTree(order = self.order, depth = self.depth + 1, keys = [key], descedants = [])
                    self.descedants.append(newdescedant)
                    self.keys.append(key)
                    res = self.descedants[i].insert_element(name, key)
            else:
                res = self.descedants[i].insert_element(name, key)
            if res is not None:
                if res[0].leaf:
                    if len(self.keys) < self.order - 1:
                        self.keys = self.keys + [res[2]]
                        self.keys.sort()
                        ind = self.keys.index(res[2])
                        self.descedants[ind] = res[0]
                        self.descedants.insert(ind + 1, res[1])
                    else:
                        keys = self.keys + [res[2]]
                        keys.sort()
                        middle_ind = math.floor(len(self.keys)/2)
                        middle_value = keys[middle_ind]
                        descedants = self.descedants
                        descedants[i] = res[0]
                        descedants.insert(i + 1, res[1])
                        node1 = BPlusTree(order = self.order, depth = 2, descedants = descedants[:i], keys = keys[:middle_ind])
                        node2 = BPlusTree(order = self.order, depth = 2, descedants = descedants[i:], keys = keys[middle_ind+1:])
                        if self.depth == 1:
                            self.descedants = [node1, node2]
                            self.keys = [middle_value]
                        else:
                            return (node1, node2, middle_value)
                else:
                    if len(self.keys) < self.order - 1:
                        self.keys = self.keys + [res[2]]
                        self.keys.sort()
                        ind = self.keys.index(res[2])
                        self.descedants[ind] = res[0]
                        self.descedants.insert(ind + 1, res[1])
                    else:
                        pass # Need to rebalance tree

    def find_element(self, name):
        key = hash_func(name)
        if self.leaf:
            if name in self.names:
                return (key, name)
            else:
                return "Element " + name + " not found"
        else:
            i = 0
            for k in self.keys:
                if key < k:
                    break
                else:
                    i += 1
            return self.descedants[i].find_element(name)
        

"""name = input()
hash_code = hash_func(name)
print(hash_code)"""
test = ["б", "ж", "л"]
leaf1 = BPlusTree(order = 3, depth = 2, keys = [hash_func(test[0])], leaf = True, names = [test[0]])
leaf2 = BPlusTree(order = 3, depth = 2, keys = [hash_func(test[1]), hash_func(test[2])], leaf = True, names = [test[1], test[2]])
leaf1.pointer = leaf2
leaf2.pointer = "last"
test_tree = BPlusTree(order = 3, depth = 1, descedants = [leaf1, leaf2], keys = [hash_func(test[1])])
test_tree.print_tree()

test_tree.insert_element("")
test_tree.insert_element("м")
test_tree.insert_element("ф")
test_tree.insert_element("я")
print()

test_tree.print_tree(with_keys = False)

test_tree.insert_element("в")
print()

test_tree.print_tree(with_keys = False)

test_tree.insert_element("е")
print()

test_tree.print_tree(with_keys = False)

print()
print(test_tree.find_element("ф"))
print(test_tree.find_element("к"))
print(test_tree.find_element("а"))