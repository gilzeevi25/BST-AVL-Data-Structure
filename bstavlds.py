NO_ITEM = -1
OK = 0
"""
Gil Zeevi ID: 203909320
HW3 Data structures 2020/2021 IDC
"""

class Node:
    """
    BST Node
    """

    def __init__(self, key, value=None, left=None, right=None):
        """
        Constructor for BST Node
        :param key: int
        :param value: anything
        :param left: Left son - Node or None
        :param right: Right son - Node or None
        """
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return 'Node: key,value=(' + str(self.key) + ',' + str(self.value) + ')'


class BST:
    """
    BST Data Structure
    """

    def __init__(self, root=None):
        """
        Constructor for BST
        :param root: root of another BST
        """
        self.root = root

    def __repr__(self):
        """
        :return: a string represent the tree
        """
        s = '--------------------------------------'
        next = True
        level_arr = []
        cur_arr = [self.root]
        while next:
            next_arr = []
            for node in cur_arr:
                if node is not None:
                    next_arr.append(node.left)
                    next_arr.append(node.right)
                else:
                    next_arr.append(None)
                    next_arr.append(None)
            level_arr.append(cur_arr)
            for tmp in next_arr:
                if tmp is not None:
                    next = True
                    break
                else:
                    next = False
            cur_arr = next_arr
        d_arr = []
        d = 0
        for i in range(len(level_arr)):
            d_arr.append(d)
            d = 2 * d + 1
        d_arr.reverse()
        for i in range(len(level_arr)):
            s += '\n' + self.__level_repr(level_arr[i], d_arr[i])
        return s

    def __level_repr(self, arr, d):
        """
        helper for repr
        """
        s = ' ' * d
        for node in arr:
            if node is None:
                s = s + '!'
            else:
                s = s + str(node.key)
            s = s + ' ' * (2 * d + 1)
        return s

    def insert(self, key, value): #implemented as shown in BST lecture page 14
        """
        Inserts a new (key,value) pair to the BST.
        In case key already exists in the BST update the node's value
        :param key: int
        :returns None
        """
        x = self.root
        if self.__class__ == BST: #if the tree type is BST , use node class
            z = Node(key, value)
        else: # else, use AVLnode class
            z = AVLNode(key, value)
        y = self.find(key)

        if y != None:
            y.value = z.value
            return None
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x= x.right
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

    def find_min(self,nod): # method to find the minimum value in BST, used in successor method
        n = self.find(nod.key)
        while n.left is not None:
            n = n.left
        return n
    def delete(self, key):
        """
        Remove the node associated with key from the BST.
        If key not in BST don't do anything.
        :param key: int
        :return: OK if deleted successfully or NO_ITEM if key not in the BST
        """
        parent , z = self.find_family(key)
        if z is None:
            return NO_ITEM
        y = z if z.left is None or z.right is None else self.successor(z)
        x = y.left if y.left is not None else y.right
        p_y =self.find_family(y.key,parent_only=True)
        if p_y is None:
            self.root = x
        elif y == p_y.left:
            p_y.left = x
        else:
            p_y.right = x
        if y != z:
            z.key = y.key
        return OK

    def find_family(self,key,parent_only = False):
        """
        a modified find method that returns the nuclear family associated with a key (node, parent)
        :param key: int
               parent_only: default bool, if true ->  return only parent
        :return: family:{parent,node} if key is in BST or None o.w.
        """
        parent, node = None, self.root
        while True:
            if node is None: #didnt find the associated node with the key input? return None
                return (None, None)
            if node.key == key:
                if parent_only:
                    return parent
                return parent, node
            parent, node = (node, node.left) if key < node.key else (node, node.right)
    def successor(self,node): #implemented as shown in BST lecture page 16
        """
        returns the successor of a node in a BST
        :param node: Node
        :return: node: Node
        """
        if node.right is not None:
            return self.find_min(node.right)
        parent =self.find_family(node.key,parent_only=True)
        while parent is not None and node == parent.right:
            node = parent
            parent = self.find_family(parent.key,parent_only=True)
        return parent

    def find(self, key):
        """
        If key is in the BST find the Node associated with key
        otherwise return None
        :param key: int
        :return: Node if key is in BST or None o.w.
        """
        cur = self.root
        while cur is not None:
            if key > cur.key:
                cur = cur.right
            elif key < cur.key:
                cur = cur.left
            else:
                return cur
        return cur

    def inorder_traversal(self):
        if self.root is None:
            return []
        bst = [self.root]
        node = self.root
        inorder = []
        while len(bst) > 0:
            if node:
                while node.left:
                    bst.append(node.left)
                    node = node.left
            popped_node = bst.pop()
            node = None
            if popped_node:
                inorder.append(popped_node.key)
                node = popped_node.right
                bst.append(node)
        return inorder
    def preorder_traversal(self):
        if self.root is None:
            return []
        bst = [self.root]
        preorder = []
        while len(bst)>0:
            node = bst.pop()
            preorder.append(node.key)
            if node.right is not None:
                bst.append(node.right)
            if node.left is not None:
                bst.append(node.left)
        return preorder
    def postorder_traversal(self):
        if self.root is None:
            return []
        bst = [self.root]
        postorder = []
        while len(bst) > 0:
            node = bst.pop()
            postorder.append(node.key)
            if node.left is not None:
                bst.append(node.left)
            if node.right is not None:
                bst.append(node.right)
        return postorder[::-1]

    @staticmethod
    def create_BST_from_sorted_arr(arr):
        """
        Creates a balanced BST from a sorted array of keys according to the algorithm from class.
        The values of each key should be None.
        :param arr: sorted array as Python list
        :return: an object of type BST representing the balanced BST
        """
        root = BST._create_BST_from_sorted_arr_(arr)
        return BST(root)

    @staticmethod
    def _create_BST_from_sorted_arr_(arr):
        if len(arr) > 0: # a bit modified method of what shown in recitation: due to the nature of python, its not necessary to keep the start&end indicators
            mid = len(arr) // 2
            root = Node(arr[mid], None)
            root.left = BST._create_BST_from_sorted_arr_(arr[:mid])
            root.right = BST._create_BST_from_sorted_arr_(arr[mid + 1:])
             #can be modified into ---return BST(root)---, but we were asked to return the root, so all there is left is to create a BST instance in main
        else:
            return None
        return root
# -------------------------------------------------------------------------------------------------------------------- #


class AVLNode(Node):
    """
    Node of AVL
    """

    def __init__(self, key, value=None, left=None, right=None):
        """
        Constructor for AVL Node
        :param key: int
        :param value: anything
        :param left: Left son - Node or None
        :param right: Right son - Node or None
        """
        super(AVLNode, self).__init__(key, value, left, right)
        self.height = 0

    def __repr__(self):
        return super(AVLNode, self).__repr__() + ',' + 'height=' + str(self.height)

    def get_balance(self):
        """
        :return: The balance of the tree rooted at self: self.left.height-self.right.height
        """
        h_left, h_right = -1, -1
        if self.left:
            h_left = self.left.height
        if self.right:
            h_right = self.right.height
        return h_left-h_right # doesnt return the abs so we can determine if left or right heavy

class AVL(BST):
    """
    AVL Data Structure
    """

    def __init__(self, root=None):
        """
        Constructor for a new AVL
        :param root: root of another AVL
        """
        super(AVL, self).__init__(root)

    def insert(self, key, value):
        """
        Inserts a new (key,value) pair to the BST.
        In case key already exists in the BST update the node's value
        :param key: int
        """
        super(AVL, self).insert(key,value) #using the inherited insert of BST as presented in slide 14 recitation07
        parent = super(AVL, self).find_family(key,parent_only=True)
        while parent is not None:
            parent.height = 1 + max(parent.left.height if parent.left is not None else -1, parent.right.height if parent.right is not None else -1)
            if abs(parent.get_balance()) > 1: # check if balance is needed
                self.rebalance(parent,key) #dive into balancing
            parent = self.find_family(parent.key,parent_only=True)


    def LeftRotation(self,x): #slide 17 recitation07
        x.left = AVLNode(x.key,x.value,x.left,x.right.left)
        x.key = x.right.key
        x.value = x.right.value
        x.right = x.right.right
        # Updating heights:
        x.left.height = 1 + max(x.left.left.height if x.left.left is not None else -1,x.left.right.height if x.left.right is not None else -1)
        x.height = 1 + max(x.left.height if x.left is not None else -1, x.right.height if x.right is not None else -1)

    def RightRotation(self,x): #Symmetrical to LeftRotation
        x.right = AVLNode(x.key,x.value, x.left.right, x.right)
        x.key = x.left.key
        x.value = x.left.value
        x.left = x.left.left
        # Updating heights:
        x.right.height = 1 + max(x.right.left.height if x.right.left is not None else -1, x.right.right.height if x.right.right is not None else -1)
        x.height = 1 + max(x.left.height if x.left is not None else -1, x.right.height if x.right is not None else -1)

    def rebalance(self,p,key = None): #balancing the tree -> given key in case of insertion, and none key in case of deletion
        balance = p.get_balance() # gives p.left.height - p.right.height
        if balance > 1 and (key < p.left.key if key is not None else p.left.get_balance() >=0):     # left left balance
            self.RightRotation(p)
            return
        if balance > 1 and (key > p.left.key if key is not None else p.left.get_balance() < 0):     # left right balance
            self.LeftRotation(p.left)
            self.RightRotation(p)
            return
        if balance < -1 and (key > p.right.key if key is not None else p.right.get_balance() <= 0):   # right right balance
            self.LeftRotation(p)
            return
        if balance < -1 and (key < p.right.key if key is not None else p.right.get_balance() > 0):  # right left balance
            self.RightRotation(p.right)
            self.LeftRotation(p)
            return

    def delete(self, key):
        """
        Remove the node associated with key from the BST.
        If key not in BST don't do anything.
        :param key: int
        :return: OK if deleted successfully or NO_ITEM if key not in the BST
        """
        parent = super(AVL, self).find_family(key,parent_only=True) #get the parent before deleting the child
        out = super(AVL, self).delete(key) #using the inherited delete of BST
        if out == NO_ITEM:
            return NO_ITEM
        while parent is not None:
            parent.height = 1 + max(parent.left.height if parent.left is not None else -1, parent.right.height if parent.right is not None else -1)
            if abs(parent.get_balance()) > 1: # check if balance is needed
                self.rebalance(parent) #dive into balancing
            parent = self.find_family(parent.key,parent_only=True)
        return OK
