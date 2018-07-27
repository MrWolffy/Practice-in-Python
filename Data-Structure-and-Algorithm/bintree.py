# ADT BinTree:
#     BinTree(self, data, left, right)    # 构造操作，创建一个新二叉树
#     is_empty(self)                      # 判断self是否为一个空二叉树
#     num_nodes(self)                     # 求二叉树的结点个数
#     data(self)                          # 获取二叉树根存储的数据
#     left(self)                          # 获得二叉树的左子树
#     right(self)                         # 获得二叉树的右子树
#     set_left(self, btree)               # 用btree取代原来的左子树
#     set_right(self, btree)              # 用btree取代原来的右子树
#     traversal(self)                     # 遍历二叉树中各结点数据的迭代器
#     forall(self, op)                    # 对二叉树中的每个结点的数据执行操作op


from stack import *


class BinTNode:
    def __init__(self, dat, left=None, right=None):
        self.data = dat
        self.left: BinTNode = left
        self.right: BinTNode = right


class BinTree:
    def __init__(self, node=None):
        self._root: BinTNode = node

    def is_empty(self):
        return self._root is None

    def root(self):
        return self._root

    def leftchild(self):
        return self._root.left

    def rightchild(self):
        return self._root.right

    def set_root(self, rootnode):
        self._root = rootnode

    def set_left(self, leftchild):
        self._root.left = leftchild

    def set_right(self, rightchild):
        self._root.right = rightchild

    def count_nodes(self):
        def count_BinTNodes(node: BinTNode):
            if node is None:
                return 0
            else:
                return 1 + count_BinTNodes(node.left) + count_BinTNodes(node.right)
        return count_BinTNodes(self._root)

    def preorder_elements(self):
        t, s = self._root, SStack()
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t.right)
                yield t.data
                t = t.left
            t = s.pop()

    def levelorder_elements(self):
        t, s = self._root, SStack()
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t.right)
                s.push(t)
                t = t.left
            t = s.pop()
            if t is not None:
                yield t.data
                t = s.pop()

    def postorder_elements(self):
        t, s = self._root, SStack()
        while t is not None or not s.is_empty():
            while t is not None:
                s.push(t)
                t = t.left if t.left is not None else t.right
            t = s.pop()
            yield t.data
            if not s.is_empty() and s.top().left == t:
                t = s.top().right
            else:
                t = None


if __name__ == '__main__':
    btree = BinTree(BinTNode("a",
                             BinTNode("b"),
                             BinTNode("c",
                                      BinTNode("d",
                                               BinTNode("f"),
                                               BinTNode("g")),
                                      BinTNode("e",
                                               BinTNode("i"),
                                               BinTNode("h")))))
    for each in btree.preorder_elements():
        print(each, end=" ")
    print()
    for each in btree.levelorder_elements():
        print(each, end=" ")
    print()
    for each in btree.postorder_elements():
        print(each, end=" ")
    print()
