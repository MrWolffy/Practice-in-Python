# ADT Queue:
#     Queue(self)                 # 创建空队列
#     is_empty(self)              # 判断队列是否为空
#     enqueue(self, elem)         # 将元素elem加入队列
#     dequeue(self)               # 删除队列里最早进入的元素并将其返回
#     peek(self)                  # 查看队列里最早进入的元素，不删除


class LNode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_


class QueueUnderflow(ValueError):
    pass


class LQueue:
    """基于链接表实现的队列"""
    def __init__(self):
        self._head = None
        self._rear = None

    def is_empty(self) -> bool:
        return self._head is None

    def enqueue(self, elem):
        if self._rear is None:
            self._head = LNode(elem, self._head)
            self._rear = self._head
        else:
            self._rear.next = LNode(elem)
            self._rear = self._rear.next

    def dequeue(self):
        if self._head is None:
            raise QueueUnderflow("in pop")
        e = self._head.elem
        self._head = self._head.next
        return e

    def peek(self):
        if self._head is None:
            raise QueueUnderflow("in pop")
        return self._head.elem


class SQueue:
    """基于list实现的队列"""
    def __init__(self, init_len=8):
        self._len = init_len
        self._elems = [0] * init_len
        self._head = 0
        self._num = 0

    def is_empty(self):
        return self._num == 0

    def peek(self):
        if self._num == 0:
            raise QueueUnderflow("in peek")
        return self._elems[self._head]

    def dequeue(self):
        if self._num == 0:
            raise QueueUnderflow("in dequeue")
        e = self._elems[self._head]
        self._head = (self._head + 1) % self._len
        self._num -= 1
        return e

    def enqueue(self, e):
        if self._num == self._len:
            self.__extend()
        self._elems[(self._head + self._num) % self._len] = e
        self._num += 1

    def __extend(self):
        old_len = self._len
        self._len *= 2
        new_elems = [0] * self._len
        for i in range(old_len):
            new_elems[i] = self._elems[(self._head + i) % old_len]
        self._elems, self._head = new_elems, 0


if __name__ == '__main__':
    maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def maze_solve_queue(maze, start, end):
        if start == end:
            print("Path finds.")
            return
        qu = SQueue()
        maze[start[0]][start[1]] = 2
        qu.enqueue(start)
        while not qu.is_empty():
            pos = qu.dequeue()
            for i in range(4):
                nextp = (pos[0] + dirs[i][0], pos[1] + dirs[i][1])
                if maze[nextp[0]][nextp[1]] == 0:
                    if nextp == end:
                        print("Path finds.")
                        return
                    maze[nextp[0]][nextp[1]] = 2
                    qu.enqueue(nextp)
        print("No path.")

    maze_solve_queue(maze, (1, 1), (10, 12))
