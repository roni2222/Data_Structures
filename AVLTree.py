

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    # O(1) Complexity
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        if key is not None:
            self.bf = 0

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    "Time complexity O(1) - comparing two keys"

    def is_real_node(self):
        return self.key is not None


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    # O(1) Complexity
    def __init__(self):
        self.root = AVLNode(None, None)
        self.size_property = 0

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    "Time complexity O(logn) - worst case - the key doesn't exist in the tree, AVL Tree - height log(n) "

    def search(self, key):
        node = self.root
        edges = 0
        while node.is_real_node():
            if key == node.key:
                return node, edges + 1
            elif key < node.key:
                node = node.left
            else:
                node = node.right
            edges += 1
        return None, edges + 1

    """searches for a node in the dictionary corresponding to the key, starting at the max

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    # O(log(n)) Complexity
    def finger_search(self, key):
        current = self.max_node()
        edges = 0
        # min sub-tree is self (key is in the left sub-tree of the root)
        if key < self.root.key:
            while current.is_real_node() and current.parent is not None:
                if key == current.key:
                    return current, edges + 1
                elif key < current.key:
                    current = current.parent
                    edges += 1
                else:
                    return None, edges + 1
            current, search_edges = self.search(key)
            return current, edges + search_edges
        # min sub-tree is when the root is larger than our key
        if key > self.root.key:
            while current.is_real_node() and current.parent.key < key:
                if key == current.key:
                    return current, edges + 1
                elif key < current.key:
                    current = current.parent
                    edges += 1
                else:
                    return None, edges + 1
            current, search_edges = self.search(key)
            return current, edges + search_edges
        # go to root
        if key == self.root.key:
            while current.is_real_node() and current.parent is not None:
                current = current.parent
                edges += 1
            return current, edges + 1

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    # Time complexity O(1)
    def get_height(self, node):
        if node.key is None:
            return 0
        return node.height

    # O(log(n)) Complexity
    def virtualsearch(self, key):
        pointer = self.root
        edges = 0
        while pointer.is_real_node():
            if pointer.key == key:
                return pointer, edges
            elif pointer.key < key:
                pointer = pointer.right
            else:
                pointer = pointer.left
            edges += 1

        return pointer, edges

    # O(log(n)) Complexity
    def insert(self, key, val):
        balance_count = 0
        pointer, edges = self.virtualsearch(key)
        pointer.key = key
        pointer.value = val
        pointer.height = 0
        pointer.left = AVLNode(None, None)
        pointer.right = AVLNode(None, None)
        pointer.right.parent = pointer
        pointer.left.parent = pointer
        promote = 0

        y = pointer.parent
        b = True
        while (y != None):
            if b:
                h = y.height
                y.height = max(y.left.height, y.right.height) + 1
                y.bf = y.left.height - y.right.height
                if y.bf > -2 and y.bf < 2 and h == y.height:
                    b = False
                    y = y.parent
                    continue

                if y.bf > -2 and y.bf < 2 and y.height != h:  # case B1 - promote
                    balance_count += 1
                    y = y.parent
                    promote += 1
                    continue

                else:
                    if y.bf == 2:
                        if y.left.bf == 1:  # case B2 - single rotation
                            self.R_rotation(y.left)
                            balance_count += 1
                        else:  # y.left.bf == 0 , case B3 - double rotation
                            self.L_rotation(y.left.right)
                            self.R_rotation(y.left)
                            balance_count += 2
                    elif y.bf == -2:
                        if y.right.bf == -1:  # case B2 - single rotation
                            self.L_rotation(y.right)
                            balance_count += 1

                        else:  # , case B3 - double rotation
                            self.R_rotation(y.right.left)
                            self.L_rotation(y.right)
                            balance_count += 2
                y = y.parent  # changing each nodes' size after rotating
            y = y.parent  # after case A or case B1 changing each nodes' size
        self.size_property += 1
        return pointer, edges, promote

    # O(1) Complexity
    def R_rotation(self, A):
        B = A.parent
        B.left = A.right
        B.left.parent = B
        A.right = B
        A.parent = B.parent
        if A.parent == None:
            self.root = A
        elif A.parent.key > A.key:
            A.parent.left = A
        else:
            A.parent.right = A
        B.parent = A
        B.height = max(B.left.height, B.right.height) + 1
        B.bf = B.left.height - B.right.height
        A.height = max(A.left.height, A.right.height) + 1
        A.bf = A.left.height - A.right.height

    # O(1) Complexity
    def L_rotation(self, A):
        B = A.parent
        B.right = A.left
        B.right.parent = B
        A.left = B
        A.parent = B.parent
        if A.parent == None:
            self.root = A
        elif A.parent.key > A.key:
            A.parent.left = A
        else:
            A.parent.right = A
        B.parent = A
        B.height = max(B.left.height, B.right.height) + 1
        B.bf = B.left.height - B.right.height
        A.height = max(A.left.height, A.right.height) + 1
        A.bf = A.left.height - A.right.height

    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """

    # O(log(n)) Complexity
    def finger_virtual_search(self, key):
        pointer = self.max_node()

        if pointer is None:
            return self.root, 0

        edges = 0

        while pointer.parent is not None and pointer.parent.key > key:
            pointer = pointer.parent
            edges += 1

        t = AVLTree()
        t.root = pointer

        pointer, virtual_edges = t.virtualsearch(key)

        return pointer, edges + virtual_edges

    # O(log(n)) Complexity
    def finger_insert(self, key, val):
        balance_cnt = 0
        pointer, edges = self.finger_virtual_search(key)
        pointer.key = key
        pointer.value = val
        pointer.height = 0
        pointer.left = AVLNode(None, None)
        pointer.right = AVLNode(None, None)
        pointer.right.parent = pointer
        pointer.left.parent = pointer
        promote = 0

        y = pointer.parent
        bb = True
        while (y != None):
            if bb:
                h = y.height
                y.height = max(y.left.height, y.right.height) + 1
                y.bf = y.left.height - y.right.height
                if y.bf > -2 and y.bf < 2 and h == y.height:
                    bb = False
                    y = y.parent
                    continue

                if y.bf > -2 and y.bf < 2 and y.height != h:  # case B1 - promote
                    balance_cnt += 1
                    y = y.parent
                    promote += 1
                    continue

                else:
                    if y.bf == 2:
                        if y.left.bf == 1:  # case B2 - single rotation
                            self.R_rotation(y.left)
                            balance_cnt += 1
                        else:  # y.left.bf == 0 , case B3 - double rotation
                            self.L_rotation(y.left.right)
                            self.R_rotation(y.left)
                            balance_cnt += 2
                    elif y.bf == -2:  # case B2 - single rotation
                        if y.right.bf == -1:
                            self.L_rotation(y.right)
                            balance_cnt += 1

                        else:
                            self.R_rotation(y.right.left)
                            self.L_rotation(y.right)
                            balance_cnt += 2
                y = y.parent  # changing each nodes' size after rotating
            y = y.parent  # after case A or case B1 changing each nodes' size
            self.max_node()
        self.size_property += 1
        return pointer, edges, promote

    # O(log(n)) Complexity
    def successor(self, node):
        pointer = node
        if node.right != None and node.right.is_real_node():
            pointer = pointer.right
            while pointer.is_real_node():
                pointer = pointer.left
            return pointer.parent

        else:
            while (pointer != self.root):
                if pointer.parent.key >= node.key:
                    return pointer.parent
                pointer = pointer.parent
        return None

    # O(1) Complexity
    def delete_leaf_or_one_child(self, node):
        if node == self.root:
            if node.right.is_real_node():
                self.root = node.right
                self.root.parent = None
            elif node.left.is_real_node():
                self.root = node.left
                self.root.parent = None
            else:
                self.root = AVLNode(None, None)

        else:
            pointer = node
            if node.right.is_real_node():
                pointer.right.parent = pointer.parent
                if pointer.parent.right == pointer:
                    pointer.parent.right = pointer.right
                else:
                    pointer.parent.left = pointer.right

            elif node.left.is_real_node():
                pointer.left.parent = pointer.parent
                if pointer.parent.right == pointer:
                    pointer.parent.right = pointer.left
                else:
                    pointer.parent.left = pointer.left

            else:
                if pointer.parent.right == pointer:
                    pointer.parent.right = AVLNode(None, None)
                    pointer.parent.right.parent = pointer.parent
                else:
                    pointer.parent.left = AVLNode(None, None)
                    pointer.parent.left.parent = pointer.parent

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    # O(log(n)) Complexity
    def delete(self, node):
        pointer = node
        balance_count = 0
        if pointer.right.is_real_node() and pointer.left.is_real_node():  # 2 children
            succ = self.successor(pointer)
            pointer.key = succ.key
            pointer.value = succ.value
            pointer = succ
        y = pointer.parent
        self.delete_leaf_or_one_child(pointer)
        b = True
        while (y != None):
            if b:  # rotation is needed
                h = y.height
                y.height = max(y.left.height, y.right.height) + 1
                y.bf = y.left.height - y.right.height
                if y.bf > -2 and y.bf < 2 and h == y.height:
                    b = False
                    y = y.parent
                    continue

                if y.bf > -2 and y.bf < 2 and y.height != h:
                    balance_count += 1
                    y = y.parent
                    continue

                else:
                    balance_count += 1
                    if y.bf == 2:
                        if y.left.bf == 1 or y.left.bf == 0:
                            self.R_rotation(y.left)
                        else:
                            self.L_rotation(y.left.right)
                            self.R_rotation(y.left)
                            balance_count += 1
                    elif y.bf == -2:
                        if y.right.bf == -1 or y.right.bf == 0:
                            self.L_rotation(y.right)

                        else:
                            self.R_rotation(y.right.left)
                            self.L_rotation(y.right)
                            balance_count += 1
                y = y.parent
            y = y.parent
        self.size_property -= 1
        return None

    """joins self with item and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separting self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """

    # O(log(n)) Complexity
    def join(self, tree2, key, val):
        if self.root.key is None:  # self is empty tree
            self.size_property = tree2.size_property + 1
            tree2.insert(key, val)
            self.root = tree2.root
            return
        if tree2.root.key is None:  # tree2 is empty tree
            self.insert(key, val)
            return

        height_diff = abs(self.root.height - tree2.root.height)

        if height_diff < 2:
            new_root = AVLNode(key, val)
            self.size_property = self.size_property + tree2.size_property + 1
            if self.root.key < key:
                new_root.left = self.root
                new_root.right = tree2.root
            else:
                new_root.right = self.root
                new_root.left = tree2.root

            if new_root.left:
                new_root.left.parent = new_root
            if new_root.right:
                new_root.right.parent = new_root

            self.root = new_root
            self.root.height = max(self.root.left.height if self.root.left else -1,
                                   self.root.right.height if self.root.right else -1) + 1
            return

        x = AVLNode(key, val)

        if self.size_property > tree2.size_property:
            tree2_height = tree2.root.height
            if self.root.key < key:
                b = self.root
                while b.height > tree2_height:
                    b = b.right
                x.right = tree2.root
                x.right.parent = x
                x.left = b
                x.parent = b.parent
                if b.parent is None:  # אם b הוא השורש
                    self.root = x
                else:
                    if b == b.parent.right:
                        b.parent.right = x
                    else:
                        b.parent.left = x
                x.left.parent = x
            else:
                b = self.root
                while b.height > tree2_height:
                    b = b.left
                x.left = tree2.root
                x.left.parent = x
                x.right = b
                x.parent = b.parent
                if b.parent is None:  # אם b הוא השורש
                    self.root = x
                else:
                    if b == b.parent.right:
                        b.parent.right = x
                    else:
                        b.parent.left = x
                x.right.parent = x
        else:
            if self.root.key > key:
                b = tree2.root
                while b.height > self.root.height:
                    b = b.right
                x.right = self.root
                x.right.parent = x
                x.left = b
                x.parent = b.parent
                if b.parent is None:  # אם b הוא השורש
                    tree2.root = x
                else:
                    if b == b.parent.right:
                        b.parent.right = x
                    else:
                        b.parent.left = x
                x.left.parent = x
            else:
                b = tree2.root
                while b.height > self.root.height:
                    b = b.left
                x.left = self.root
                x.left.parent = x
                x.right = b
                x.parent = b.parent
                if b.parent is None:  # אם b הוא השורש
                    tree2.root = x
                else:
                    if b == b.parent.right:
                        b.parent.right = x
                    else:
                        b.parent.left = x
                x.right.parent = x

        # balancing is needed - same cases as delete
        balance_count = 0
        y = x
        b = True
        while y is not None:
            if b:
                h = y.height
                y.height = max(y.left.height if y.left else -1, y.right.height if y.right else -1) + 1
                y.bf = (y.left.height if y.left else -1) - (y.right.height if y.right else -1)
                if y.bf > -2 and y.bf < 2 and h == y.height:
                    b = False
                    y = y.parent
                    continue

                if y.bf > -2 and y.bf < 2 and y.height != h:
                    balance_count += 1
                    y = y.parent
                    continue

                else:
                    balance_count += 1
                    if y.bf == 2:
                        if y.left.bf == 1 or y.left.bf == 0:
                            self.R_rotation(y.left)
                        else:
                            self.L_rotation(y.left.right)
                            self.R_rotation(y.left)
                            balance_count += 1
                    elif y.bf == -2:
                        if y.right.bf == -1 or y.right.bf == 0:
                            self.L_rotation(y.right)
                        else:
                            self.R_rotation(y.right.left)
                            self.L_rotation(y.right)
                            balance_count += 1
                y = y.parent
            y = y.parent
        self.size_property = self.size_property + tree2.size_property + 1

    # O(log(n)) Complexity
    # splitting with joins
    def split(self, node):
        smaller_tree = AVLTree()
        greater_tree = AVLTree()

        if node.left and node.left.is_real_node():
            smaller_tree.root = node.left
            smaller_tree.root.parent = None
        if node.right and node.right.is_real_node():
            greater_tree.root = node.right
            greater_tree.root.parent = None

        # going up the tree
        current_node = node
        while current_node.parent is not None:
            parent = current_node.parent

            if parent.left == current_node:  # current_node is left son
                t = AVLTree()
                if parent.right and parent.right.is_real_node():
                    t.root = parent.right
                    t.root.parent = None
                t.join(greater_tree, parent.key, parent.value)
                greater_tree = t
            else:  # current_node is right son
                t2 = AVLTree()
                if parent.left and parent.left.is_real_node():
                    t2.root = parent.left
                    t2.root.parent = None
                t2.join(smaller_tree, parent.key, parent.value)
                smaller_tree = t2

            current_node = parent

        return smaller_tree, greater_tree


    # O(n) Complexity
    def in_order(self, node, result):
        if node.is_real_node() and node != None:
            self.in_order(node.left, result)
            result.append((node.key, node.value))
            self.in_order(node.right, result)
        return result

    # O(n) Complexity
    def avl_to_array(self):
        result = []
        return self.in_order(self.root, result)

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """

    # O(log(n)) Complexity
    def max_node(self):
        if self.root is None or not self.root.is_real_node():
            return None

        pointer = self.root
        while pointer.right.is_real_node():
            pointer = pointer.right
        return pointer

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    # O(1) Complexity
    def size(self):
        return self.size_property

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    # O(1) Complexity
    def get_root(self):
        return self.root









