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
    num = 0

    def __init__(self, order, depth, keys, descedants = None, leaf = False, names = None):
        try:
            if (depth <= 3) and (depth >= 1) and (order <= 4) and (order >= 2):
                self.order = order
                self.depth = depth
                self.leaf = leaf
                if leaf:
                    if len(keys) > order - 1:
                        raise Exception("Wrong number of keys!")
                    self.keys = keys
                    if names is not None:
                        if len(names) > order - 1:
                            raise Exception("Wrong number of names!")
                    else:
                        raise Exception("This tree is leaf, but also doesn't have names!")
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
        print(" " * 6 * depth, end = "")
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
            else:
                self.keys = self.keys + [key]
                self.keys.sort()
                ind = self.keys.index(key)
                self.names.insert(ind, name)
                middle_ind = math.floor(len(self.keys)/2)
                middle_value = self.keys[middle_ind]
                leaf1 = BPlusTree(order = self.order, depth = 2, keys = self.keys[:middle_ind], leaf = True, names = self.names[:middle_ind])
                leaf2 = BPlusTree(order = self.order, depth = 2, keys = self.keys[middle_ind:], leaf = True, names = self.names[middle_ind:])
                self.keys = [middle_value]
                self.leaf = False
                self.names = None
                self.descedants = [leaf1, leaf2]
        else:
            if self.descedants[0].leaf:
                i = 0
                for k in self.keys:
                    if key < k:
                        break
                    else:
                        i += 1
                leaf = self.descedants[i]
                if len(leaf.keys) < self.order - 1:
                    leaf.keys = leaf.keys + [key]
                    leaf.keys.sort()
                    ind = leaf.keys.index(key)
                    leaf.names.insert(ind, name)
                else:
                    leaf.keys = leaf.keys + [key]
                    leaf.keys.sort()
                    ind = leaf.keys.index(key)
                    leaf.names.insert(ind, name)
                    middle_ind = math.floor(len(leaf.keys)/2)
                    middle_value = leaf.keys[middle_ind]
                    if len(self.keys) < self.order - 1:
                        leaf1 = BPlusTree(order = self.order, depth = 2, leaf = True, keys = leaf.keys[:middle_ind], names = leaf.names[:middle_ind])
                        leaf2 = BPlusTree(order = self.order, depth = 2, leaf = True, keys = leaf.keys[middle_ind:], names = leaf.names[middle_ind:])
                        self.keys.insert(i, middle_value)
                        self.descedants[i] = leaf1
                        self.descedants.insert(i + 1, leaf2)
                    else:
                        leaf1 = BPlusTree(order = self.order, depth = 3, leaf = True, keys = leaf.keys[:middle_ind], names = leaf.names[:middle_ind])
                        leaf2 = BPlusTree(order = self.order, depth = 3, leaf = True, keys = leaf.keys[middle_ind:], names = leaf.names[middle_ind:])
                        keys = self.keys + [middle_value]
                        keys.sort()
                        mid_ind = math.floor(len(self.keys)/2)
                        mid_val = keys[mid_ind]
                        self.descedants[i] = leaf1
                        self.descedants.insert(i + 1, leaf2)
                        if len(self.keys) > 1:
                            node1 = BPlusTree(order = self.order, depth = 2, keys = keys[:mid_ind], descedants = self.descedants[:mid_ind + 1])
                            node2 = BPlusTree(order = self.order, depth = 2, keys = keys[mid_ind + 1:], descedants = self.descedants[mid_ind + 1:])
                            self.keys = [mid_val]
                            self.descedants = [node1, node2]
                        else:
                            if i == 0:
                                node1 = BPlusTree(order = self.order, depth = 2, keys = [self.descedants[0].keys[0] + 1], descedants = self.descedants[:mid_ind + 1])
                                node2 = BPlusTree(order = self.order, depth = 2, keys = [self.descedants[1].keys[0] + 1], descedants = self.descedants[mid_ind + 1:])
                                self.keys = [mid_val]
                                self.descedants = [node1, node2]
                            else:
                                node1 = BPlusTree(order = self.order, depth = 2, keys = [self.descedants[0].keys[0] + 1], descedants = self.descedants[:mid_ind + 1])
                                node2 = BPlusTree(order = self.order, depth = 2, keys = keys[mid_ind + 1:], descedants = self.descedants[mid_ind + 1:])
                                self.keys = [mid_val]
                                self.descedants = [node1, node2]
            else:
                i = 0
                for k in self.keys:
                    if key < k:
                        break
                    else:
                        i += 1
                descedant = self.descedants[i]
                j = 0
                for lk in descedant.keys:
                    if key < lk:
                        break
                    else:
                        j += 1
                if len(descedant.descedants) > j:
                    leaf = descedant.descedants[j]
                else:
                    leaf = BPlusTree(order = self.order, depth = 3, keys = [], leaf = True, names = [])
                    descedant.descedants.append(leaf)
                if len(leaf.keys) < self.order - 1:
                    leaf.keys = leaf.keys + [key]
                    leaf.keys.sort()
                    ind = leaf.keys.index(key)
                    leaf.names.insert(ind, name)
                else:
                    if len(descedant.keys) < self.order - 1:
                        leaf.keys = leaf.keys + [key]
                        leaf.keys.sort()
                        ind = leaf.keys.index(key)
                        leaf.names.insert(ind, name)
                        middle_ind = math.floor(len(leaf.keys)/2)
                        middle_value = leaf.keys[middle_ind]
                        leaf1 = BPlusTree(order = self.order, depth = 3, leaf = True, keys = leaf.keys[:middle_ind], names = leaf.names[:middle_ind])
                        leaf2 = BPlusTree(order = self.order, depth = 3, leaf = True, keys = leaf.keys[middle_ind:], names = leaf.names[middle_ind:])
                        descedant.keys.insert(j, middle_value)
                        descedant.descedants[j] = leaf1
                        descedant.descedants.insert(j + 1, leaf2)
                    else:
                        if len(self.keys) < self.order - 1:
                            leaf.keys = leaf.keys + [key]
                            leaf.keys.sort()
                            ind = leaf.keys.index(key)
                            leaf.names.insert(ind, name)
                            middle_ind = math.floor(len(leaf.keys)/2)
                            middle_value = leaf.keys[middle_ind]
                            leaf1 = BPlusTree(order = self.order, depth = 3, leaf = True, keys = leaf.keys[:middle_ind], names = leaf.names[:middle_ind])
                            leaf2 = BPlusTree(order = self.order, depth = 3, leaf = True, keys = leaf.keys[middle_ind:], names = leaf.names[middle_ind:])
                            keys = descedant.keys + [middle_value]
                            keys.sort()
                            mid_ind = math.floor(len(descedant.keys)/2)
                            mid_val = keys[mid_ind]
                            descedant.descedants[j] = leaf1
                            descedant.descedants.insert(j + 1, leaf2)
                            node1 = BPlusTree(order = self.order, depth = 2, keys = keys[:mid_ind], descedants = descedant.descedants[:mid_ind + 1])
                            node2 = BPlusTree(order = self.order, depth = 2, keys = keys[mid_ind + 1:], descedants = descedant.descedants[mid_ind + 1:])
                            self.keys.insert(i, mid_val)
                            self.descedants[i] = node1
                            self.descedants.insert(i + 1, node2)
                        else:
                            all_elems = self.find_all_elements()
                            if len(all_elems) == self.order ** 3 - self.order ** 2:
                                print("Tree has reached its maximum")
                            else:
                                self.rebuild_tree(all_elems + [name]) 

    def rebuild_tree(self, all_elems):
        n = len(all_elems)
        if n < self.num:
            raise Exception
        mid_ind = math.floor(n/2)
        self.leaf = True
        self.depth = 1
        self.keys = [hash_func(all_elems[mid_ind])]
        self.names = [all_elems[mid_ind]]
        self.descedants = None
        if n % 2 != 0:
            for i in range(1, mid_ind + 1):
                self.insert_element(all_elems[mid_ind + i])
                self.insert_element(all_elems[mid_ind - i])
        else:
            for i in range(1, mid_ind):
                self.insert_element(all_elems[mid_ind - i])
                self.insert_element(all_elems[mid_ind + i])
            self.insert_element(all_elems[0])

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
        
    def find_elements_greater_than(self, name):
        key = hash_func(name)
        if self.leaf:
            for i in range(len(self.keys)):
                if self.keys[i] > key:
                    return self.names[i:]
                elif i == len(self.keys) - 1:
                    return []
        else:
            res = []
            if self.descedants[0].leaf:
                i = 0
                for k in self.keys:
                    if k > key:
                        leaf = self.descedants[i]
                        for j in range(len(leaf.keys)):
                            if leaf.keys[j] > key:
                                res.append(leaf.names[j])
                    i += 1
                leaf = self.descedants[i]
                for j in range(len(leaf.keys)):
                    if leaf.keys[j] > key:
                        res.append(leaf.names[j])
            else:
                i = 0
                for k in self.keys:
                    if k > key:
                        descedant = self.descedants[i]
                        j = 0
                        for lk in descedant.keys:
                            if lk > key:
                                leaf = descedant.descedants[j]
                                for x in range(len(leaf.keys)):
                                    if leaf.keys[x] > key:
                                        res.append(leaf.names[x])
                            j += 1
                        leaf = descedant.descedants[j]
                        for x in range(len(leaf.keys)):
                            if leaf.keys[x] > key:
                                res.append(leaf.names[x])
                    i += 1
                descedant = self.descedants[i]
                j = 0
                for lk in descedant.keys:
                    if lk > key:
                        leaf = descedant.descedants[j]
                        for x in range(len(leaf.keys)):
                            if leaf.keys[x] > key:
                                res.append(leaf.names[x])
                    j += 1
                leaf = descedant.descedants[j]
                for x in range(len(leaf.keys)):
                    if leaf.keys[x] > key:
                        res.append(leaf.names[x])    
            return res
        
    def find_elements_lesser_than(self, name):
        key = hash_func(name)
        if self.leaf:
            for i in range(len(self.keys)):
                if self.keys[i] >= key:
                    return self.names[:i]
                elif i == len(self.keys) - 1:
                    return self.names
        else:
            res = []
            if self.descedants[0].leaf:
                for leaf in self.descedants:
                    for i in range(len(leaf.keys)):
                        if leaf.keys[i] < key:
                            res.append(leaf.names[i])
                        else:
                            return res   
            else:
                for descedant in self.descedants:
                    for leaf in descedant.descedants:
                        for i in range(len(leaf.keys)):
                            if leaf.keys[i] < key:
                                res.append(leaf.names[i])
                            else:
                                return res 
            return res

    def find_all_elements(self):
        if self.leaf:
            return self.names
        else:
            res = []
            if self.descedants[0].leaf:
                for leaf in self.descedants:
                    for name in leaf.names:
                        res.append(name)
            else:
                for descedant in self.descedants:
                    for leaf in descedant.descedants:
                        for name in leaf.names:
                            res.append(name)
            return res

    def delete_element(self, name, key = None):
        if key is None:
            key = hash_func(name)
        try:
            if self.leaf:
                if len(self.keys) - 1 >= math.floor((self.order - 1) / 2):
                    ind = self.keys.index(key)
                    self.keys.remove(self.keys[ind])
                    self.names.remove(self.names[ind])
                else:
                    raise TypeError
            else:
                if self.descedants[0].leaf:
                    i = 0
                    for k in self.keys:
                        if key < k:
                            break
                        else:
                            i += 1
                    leaf = self.descedants[i]
                    if key in leaf.keys:
                        if len(leaf.keys) - 1 >= math.floor((self.order - 1) / 2):
                            if len(leaf.keys) == 1:
                                if i == 1:
                                    self.descedants.remove(leaf)
                                else:
                                    self.descedants.remove(leaf)
                                    self.keys[0] = self.descedants[0].keys[0] + 1
                            else:
                                leaf.delete_element(name)
                        else:
                            success = self.redistribute_leafs(name, key, i)
                            if success == 0:
                                if len(self.keys) - 1 >= math.floor((self.order - 1) / 2):
                                    if i == 0:
                                        leaf.keys = leaf.keys + self.descedants[1].keys
                                        leaf.names = leaf.names + self.descedants[1].names
                                        leaf.keys.remove(key)
                                        leaf.names.remove(name)
                                        self.keys.remove(self.keys[0])
                                        self.descedants.remove(self.descedants[1])
                                    else:
                                        leaf.keys = self.descedants[i - 1].keys + leaf.keys
                                        leaf.names = self.descedants[i - 1].names + leaf.names
                                        leaf.keys.remove(key)
                                        leaf.names.remove(name)
                                        self.keys.remove(self.keys[i - 1])
                                        self.descedants.remove(self.descedants[i])
                                else:
                                    raise TypeError
                    else:
                        raise ValueError
                else:
                    i = 0
                    for k in self.keys:
                        if key < k:
                            break
                        else:
                            i += 1
                    descendant = self.descedants[i]
                    j = 0
                    for lk in descendant.keys:
                        if key < lk:
                            break
                        else:
                            j += 1
                    if len(descendant.descedants) > j:
                        leaf = descendant.descedants[j]
                    else:
                        leaf = descendant.descedants[-1]
                    if key in leaf.keys:
                        if len(leaf.keys) - 1 >= math.floor((self.order - 1) / 2):
                            if len(leaf.keys) == 1:
                                if i == 1:
                                    if len(descendant.descedants) == 1:
                                        self.keys = self.descedants[0].keys
                                        self.descedants = self.descedants[0].descedants
                                    else:
                                        descendant.descedants.remove(leaf)
                                else:
                                    if len(descendant.descedants) == 1:
                                        self.keys = self.descedants[1].keys
                                        self.descedants = self.descedants[1].descedants
                                    else:
                                        descendant.descedants.remove(leaf)
                                        descendant.keys[0] = descendant.descedants[0].keys[0] + 1
                            else:
                                leaf.delete_element(name)
                        else:
                            success = descendant.redistribute_leafs(name, key, j)
                            if success == 0:
                                if len(descendant.keys) - 1 >= math.floor((descendant.order - 1) / 2):
                                    if j == 0:
                                        leaf.keys = leaf.keys + descendant.descedants[1].keys
                                        leaf.names = leaf.names + descendant.descedants[1].names
                                        leaf.keys.remove(key)
                                        leaf.names.remove(name)
                                        descendant.keys.remove(descendant.keys[0])
                                        descendant.descedants.remove(descendant.descedants[1])
                                    else:
                                        leaf.keys = descendant.descedants[j - 1].keys + leaf.keys
                                        leaf.names = descendant.descedants[j - 1].names + leaf.names
                                        leaf.keys.remove(key)
                                        leaf.names.remove(name)
                                        descendant.keys.remove(descendant.keys[j - 1])
                                        descendant.descedants.remove(descendant.descedants[j])
                                else:
                                    success = self.redistribute_nodes(name, key, i, j)
                                    if success == 0:
                                        if len(self.keys) - 1 >= math.floor((descendant.order - 1) / 2):
                                            if len(self.descedants) - 1 >= math.floor(descendant.order/ 2):
                                                if i == 0:
                                                    self.descedants[0].keys.append(self.descedants[1].descedants[0].keys[0])
                                                    self.descedants[0].descedants.remove(self.descedants[0].descedants[j])
                                                    for desc in self.descedants[1].descedants:
                                                        self.descedants[0].descedants.append(desc)
                                                    self.keys.remove(self.keys[0])
                                                    self.descedants.remove(self.descedants[1])
                                                else:
                                                    self.descedants[i - 1].keys.append(self.descedants[i].descedants[0].keys[0])
                                                    self.descedants[i].descedants.remove(self.descedants[i].descedants[j])
                                                    for desc in self.descedants[i].descedants:
                                                        self.descedants[i - 1].descedants.append(desc)
                                                    self.keys.remove(self.keys[i - 1])
                                                    self.descedants.remove(self.descedants[i])
                                        else:
                                            if i == 0:
                                                self.descedants[0].descedants.remove(self.descedants[0].descedants[j])
                                                for desc in self.descedants[1].descedants:
                                                    self.descedants[0].descedants.append(desc)
                                                self.descedants[0].keys.append(self.descedants[1].keys[0])
                                                self.keys = self.descedants[0].keys
                                                self.descedants = self.descedants[0].descedants
                                                self.depth -= 1
                                                for desc in self.descedants:
                                                    desc.depth -= 1
                                            else:
                                                self.descedants[i].descedants.remove(self.descedants[i].descedants[j])
                                                for desc in self.descedants[i].descedants:
                                                    self.descedants[i - 1].descedants.append(desc)
                                                self.descedants[i - 1].keys.append(self.descedants[i].keys[0])
                                                self.keys = self.descedants[0].keys
                                                self.descedants = self.descedants[i - 1].descedants
                                                self.depth -= 1
                                                for desc in self.descedants:
                                                    desc.depth -= 1
                    else:
                        raise ValueError
        except ValueError:
            print("There is no such element in tree")
        except TypeError:
            print("Deleting element will make tree unbalanced")

    def redistribute_leafs(self, name, key, i):
        if i == 0:
            if len(self.descedants) > 1:
                if len(self.descedants[1].keys) - 1 >= math.floor((self.order - 1) / 2):
                    if self.descedants[1].keys[0] != self.descedants[1].keys[1]:
                        leaf1 = self.descedants[0]
                        leaf2 = self.descedants[1]
                        leaf1.keys.remove(key)
                        leaf1.names.remove(name)
                        leaf1.keys.append(leaf2.keys[0])
                        leaf1.names.append(leaf2.names[0])
                        self.keys[i] = leaf2.keys[1]
                        leaf2.keys.remove(leaf2.keys[0])
                        leaf2.names.remove(leaf2.names[0])
                        return 1
            return 0
        else:
            if len(self.descedants[i - 1].keys) - 1 >= math.floor((self.order - 1) / 2):
                if self.descedants[i - 1].keys[-1] != self.descedants[i - 1].keys[-2]:
                    leaf1 = self.descedants[i-1]
                    leaf2 = self.descedants[i]
                    leaf2.keys.remove(key)
                    leaf2.names.remove(name)
                    leaf2.keys.insert(0, leaf1.keys[-1])
                    leaf2.names.insert(0, leaf1.names[-1])
                    self.keys[i - 1] = leaf1.keys[-1]
                    leaf1.keys.remove(leaf1.keys[-1])
                    leaf1.names.remove(leaf1.names[-1])
                    return 1
            elif len(self.descedants) > i + 1:
                if len(self.descedants[i + 1].keys) - 1 >= math.floor((self.order - 1) / 2):
                    if self.descedants[i + 1].keys[0] != self.descedants[i + 1].keys[1]:
                        leaf1 = self.descedants[i]
                        leaf2 = self.descedants[i + 1]
                        leaf1.keys.remove(key)
                        leaf1.names.remove(name)
                        leaf1.keys.append(leaf2.keys[0])
                        leaf1.names.append(leaf2.names[0])
                        self.keys[i] = leaf2.keys[1]
                        leaf2.keys.remove(leaf2.keys[0])
                        leaf2.names.remove(leaf2.names[0])
                        return 1
            return 0

    def redistribute_nodes(self, name, key, i, j):
        if i == 0:
            if len(self.descedants) > 1:
                if len(self.descedants[1].keys) - 1 >= math.floor((self.order - 1) / 2):
                    if len(self.descedants[1].descedants) - 1 >= math.floor(self.order/ 2):
                        node1 = self.descedants[0]
                        node2 = self.descedants[1]
                        node1.descedants.remove(node1.descedants[j])
                        node1.descedants.append(node2.descedants[0])
                        node2.descedants.remove(node2.descedants[0])
                        node1.keys[0] = self.keys[0]
                        self.keys[0] = node2.keys[0]
                        node2.keys.remove(node2.keys[0])
                        return 1
            return 0 
        else:
            if len(self.descedants[i - 1].keys) - 1 >= math.floor((self.order - 1) / 2):
                if len(self.descedants[i - 1].descedants) - 1 >= math.floor(self.order/ 2):
                    node1 = self.descedants[i - 1]
                    node2 = self.descedants[i]
                    node2.descedants.remove(node2.descedants[j])
                    node2.descedants.insert(0, node1.descedants[-1])
                    node1.descedants.remove(node1.descedants[-1])
                    node2.keys[0] = self.keys[i - 1]
                    self.keys[i - 1] = node1.keys[-1]
                    node1.keys.remove(node1.keys[-1])
                    return 1
            elif len(self.descedants) > i + 1:
                if len(self.descedants[i + 1].keys) - 1 >= math.floor((self.order - 1) / 2):
                    if len(self.descedants[i + 1].descedants) - 1 >= math.floor(self.order/ 2):
                        node1 = self.descedants[i]
                        node2 = self.descedants[i + 1]
                        node1.descedants.remove(node1.descedants[j])
                        node1.descedants.append(node2.descedants[0])
                        node2.descedants.remove(node2.descedants[0])
                        node1.keys[0] = self.keys[i]
                        self.keys[i] = node2.keys[0]
                        node2.keys.remove(node2.keys[0])
                        return 1
                return 0 
            return 0 

if __name__ == "__main__":
    print("Choose option:")
    print("1 - Create tree\n2 - Stop program")
    choose = input()
    print()
    if choose == "1":
        print("Enter order of a tree (minimun - 2, maximum - 4):")
        try:
            order = int(input())
            if (order < 2) or (order > 4):
                raise ValueError
            print("Enter first element (only ukrainian letters):")
            elem = input()
            tree = BPlusTree(order = order, depth = 1, leaf = True, keys = [hash_func(elem)], names = [elem])
            while choose != "0":
                print()
                print("Choose option:")
                print("1 - Print tree\n2 - Insert new element into tree\n3 - Insert multiple elements into tree\n4 - Delete element from tree\n5 - Find element")
                print("6 - Find all elements greater than\n7 - Find all elements lesser than\n0- - Stop program")
                choose = input()
                print()
                if choose == "1":
                    tree.print_tree()
                    print()
                elif choose == "2":
                    print("Enter element (only ukrainian letters):")
                    elem = input()
                    tree.insert_element(elem)
                    tree.num += 1
                elif choose == "3":
                    print("Enter elements (only ukrainian letters, separated by comma(example: Іван,Олександр,Василь)):")
                    string = input()
                    elems = string.split(",")
                    for elem in elems:
                        tree.insert_element(elem)
                        tree.num += 1
                        n = len(tree.find_all_elements())
                        if n >= order ** 3 - order ** 2:
                            print("Tree has reached its maximum")
                            break
                elif choose == "4":
                    print("Enter element you want to delete (only ukrainian letters):")
                    elem = input()
                    tree.delete_element(elem)
                    tree.num -= 1
                elif choose == "5":
                    print("Enter element you want to find (only ukrainian letters):")
                    elem = input()
                    res = tree.find_element(elem)
                    if type(res) != str:
                        print(f"\nElement was found: {res}")
                    else:
                        print("\nElement was not found")
                elif choose == "6":
                    print("Enter element (only ukrainian letters). Program will find all elements greater than given:")
                    elem = input()
                    res = tree.find_elements_greater_than(elem)
                    if len(res) > 0:
                        print(f"\nElements were found: {res}")
                    else:
                        print(f"\nThere are not elements greater than given")
                elif choose == "7":
                    print("Enter element (only ukrainian letters). Program will find all elements lesser than given:")
                    elem = input()
                    res = tree.find_elements_lesser_than(elem)
                    if len(res) > 0:
                        print(f"\nElements were found: {res}")
                    else:
                        print(f"\nThere are not elements lesser than given")
        except ValueError:
            print("Wrong input!")
        except Exception:
            print("Something gone wrong!")