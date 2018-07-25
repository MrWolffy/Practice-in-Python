# ADT List:                   # 一个表抽象数据类型
#     List(self)              # 表构造操作，创建一个新表
#     is_empty(self)          # 判断self是否为一个空表
#     len(self)               # 获得self的长度
#     prepend(self, elem)     # 将元素elem加入表中作为第一个元素
#     append(self, elem)      # 将元素elem加入表中作为最后一个元素
#     insert(self, elem, i)   # 将elem加入表中作为第i个元素，其他元素的顺序不变
#     del_first(self)         # 删除表中的首元素
#     del_last(self)          # 删除表中的尾元素
#     del(self, i)            # 删除表中第i个元素
#     search(self, elem)      # 查找元素elem在表中出现的位置，不出现时返回-1
#     forall(self, op)        # 对表中每个元素执行操作op


class LNode:
    """表中结点"""
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_


class LinkedListUnderflow(ValueError):
    pass


class LList:
    """链表类"""
    def __init__(self):
        self._head = None

    def is_empty(self) -> bool:
        """判断表空"""
        return self._head is None

    def prepend(self, elem):
        """在表头插入数据"""
        self._head = LNode(elem, self._head)

    def pop(self):
        """删除表头结点并返回这个结点里的数据"""
        if self._head is None:
            raise LinkedListUnderflow("in pop")
        e = self._head.elem
        self._head = self._head.next
        return e

    def append(self, elem):
        """在链表的最后插入元素"""
        if self._head is None:
            self._head = LNode(elem)
            return
        p = self._head
        while p.next is not None:
            p = p.next
        p.next = LNode(elem)

    def pop_last(self):
        """删除表中最后元素并把它返回"""
        if self._head is None:
            raise LinkedListUnderflow("in pop_last")
        p = self._head
        if p.next is None:
            e = p.elem
            self._head = None
            return e
        while p.next.next is not None:
            p = p.next
        e = p.next.elem
        p.next = None
        return e

    def find(self, pred):
        """查找第一个满足pred条件的元素"""
        p = self._head
        while p is not None:
            if pred(p.elem):
                return p.elem
            p = p.next

    def __str__(self):
        p = self._head
        seqlist = []
        while p is not None:
            seqlist.append(p.elem)
            p = p.next
        return str(seqlist)

    def elements(self):
        """迭代器"""
        p = self._head
        while p is not None:
            yield p.elem
            p = p.next

    def filter(self, pred):
        """筛选生成器"""
        p = self._head
        while p is not None:
            if pred(p.elem):
                yield p.elem
            p = p.next


class LList1(LList):
    """链表对象增加尾结点引用"""
    def __init__(self):
        LList.__init__(self)
        self._rear: LNode = None

    def prepend(self, elem):
        """在表头插入数据"""
        self._head = LNode(elem, self._head)
        if self._rear is None:
            self._rear = self._head

    def append(self, elem):
        """在链表的最后插入元素"""
        if self._rear is None:
            self._head = LNode(elem, self._head)
            self._rear = self._head
        else:
            self._rear.next = LNode(elem)
            self._rear = self._rear.next

    def pop_last(self):
        """在尾端删除元素"""
        if self._head is None:
            raise LinkedListUnderflow("in pop_last")
        p = self._head
        if p.next is None:
            e = p.elem
            self._head = None
            return e
        while p.next.next is not None:
            p = p.next
        e = p.next.elem
        p.next = None
        self._rear = p
        return e


class CLList:
    """循环单链表类"""
    def __init__(self):
        self._rear: LNode = None

    def is_empty(self):
        """判空"""
        return self._rear is None

    def prepend(self, elem):
        """前端插入"""
        p = LNode(elem)
        if self._rear is None:
            p.next = p
            self._rear = p
        else:
            p.next = self._rear.next
            self._rear.next = p

    def append(self, elem):
        """后端插入"""
        self.prepend(elem)
        self._rear = self._rear.next

    def pop(self):
        """前端弹出"""
        if self._rear is None:
            raise LinkedListUnderflow("in pop")
        p = self._rear.next
        if self._rear is p:
            self._rear = None
        else:
            self._rear.next = p.next
        return p.elem

    def pop_last(self):
        """后端弹出"""
        if self._rear is None:
            raise LinkedListUnderflow("in pop_last")
        p = self._rear
        if p.next is None:
            e = p.elem
            self._rear = None
            return e
        while p.next is not self._rear:
            p = p.next
        e = p.next.elem
        p.next = self._rear.next
        self._rear = p
        return e

    def elements(self):
        """迭代器"""
        if self.is_empty():
            return
        p = self._rear.next
        while True:
            yield p.elem
            if p is self._rear:
                break
            p = p.next


class DLNode(LNode):
    """双链表结点"""
    def __init__(self, elem, prev=None, next_=None):
        LNode.__init__(self, elem, next_)
        self.prev = prev


class DLList(LList1):
    def __init__(self):
        LList1.__init__(self)

    def prepend(self, elem):
        """前端插入"""
        p = DLNode(elem, None, self._head)
        if self._head is None:
            self._rear = p
        else:
            p.next.prev = p
        self._head = p

    def append(self, elem):
        """尾端插入"""
        p = DLNode(elem, self._rear, None)
        if self._head is None:
            self._head = p
        else:
            p.prev.next = p
        self._rear = p

    def pop(self):
        """前端弹出"""
        if self._head is None:
            raise LinkedListUnderflow("in pop")
        e = self._head.elem
        self._head = self._head.next
        if self._head is not None:
            self._head.prev = None
        return e

    def pop_last(self):
        """尾端弹出"""
        if self._head is None:
            raise LinkedListUnderflow("in pop_last")
        e = self._rear.elem
        self._rear = self._rear.prev
        if self._rear is None:
            self._head = None
        else:
            self._rear.next = None
        return e


if __name__ == '__main__':
    class Josephus(CLList):
        def turn(self, m):
            for i in range(m):
                self._rear = self._rear.next

        def __init__(self, n, k, m):
            CLList.__init__(self)
            for i in range(n):
                self.append(i + 1)
            self.turn(k - 1)
            while not self.is_empty():
                self.turn(m - 1)
                print(self.pop(), end=("\n" if self.is_empty() else ", "))

    Josephus(10, 2, 7)
