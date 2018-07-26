# ADT Stack:
#     Stack(self)             # 创建空栈
#     is_empty(self)          # 判断栈是否为空，空时返回True否则返回False
#     push(self, elem)        # 将元素elem加入栈
#     pop(self)               # 删除栈里最后压入的元素并将其返回
#     top(self)               # 取得栈里最后压入的元素，不删除


class LNode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_


class StackUnderflow(ValueError):
    pass


class SStack:
    """基于顺序表实现的栈类"""
    def __init__(self):
        self._elems = []

    def is_empty(self):
        return self._elems == []

    def top(self):
        if self._elems == []:
            raise StackUnderflow("in SStack.top")
        return self._elems[-1]

    def push(self, elem):
        self._elems.append(elem)

    def pop(self):
        if self._elems == []:
            raise StackUnderflow("in SStack.pop")
        return self._elems.pop()


class LStack:
    """基于链接表实现的栈类"""
    def __init__(self):
        self._top: LNode = None

    def is_empty(self):
        return self._top is None

    def top(self):
        if self._top is None:
            raise StackUnderflow("in LStack.top")
        return self._top.elem

    def push(self, elem):
        self._top = LNode(elem, self._top)

    def pop(self):
        if self._top is None:
            raise StackUnderflow("in LStack.pop")
        p = self._top
        self._top = p.next
        return p.elem


if __name__ == '__main__':
    class ESStack(SStack):
        def depth(self):
            return len(self._elems)

    def suffix_exp_evaluator(exp):
        operators = "+-*/"
        st = ESStack()
        for x in exp:
            if x not in operators:
                st.push(float(x))
                continue

            if st.depth() < 2:
                raise SyntaxError("Short of operand(s).")
            a = st.pop()
            b = st.pop()

            if x == "+":
                c = b + a
            elif x == "-":
                c = b - a
            elif x == "*":
                c = b * a
            elif x == "/":
                c = b / a
            else:
                break
            st.push(c)

        if st.depth() == 1:
            return st.pop()
        raise SyntaxError("Extra operand(s).")

    priority = {"(": 1, "+": 3, "-": 3, "*": 5, "/": 5}
    infix_operators = "+-*/()"

    def trans_infix_suffix(line):
        st = SStack()
        exp = []
        for x in tokens(line):
            if x not in infix_operators:
                exp.append(x)
            elif st.is_empty() or x == "(":
                st.push(x)
            elif x == ")":
                while not st.is_empty() and st.top() != "(":
                    exp.append(st.pop())
                if st.is_empty():
                    raise SyntaxError("Missing '('.")
                st.pop()
            else:
                while not st.is_empty() and priority[st.top()] >= priority[x]:
                    exp.append(st.pop())
                st.push(x)

        while not st.is_empty():
            if st.top() == "(":
                raise SyntaxError("Extra '('.")
            exp.append(st.pop())

        return exp

    def tokens(line):
        i, llen = 0, len(line)
        while i < llen:
            while line[i].isspace():
                i += 1
            if i >= llen:
                break
            if line[i] in infix_operators:
                yield line[i]
                i += 1
                continue
            j = i + 1
            while j < llen and not line[j].isspace() and line[j] not in infix_operators:
                if (line[j] == "e" or line[j] == "E") and j + 1 < llen and line[j+1] == "-":
                    j += 1
                j += 1
            yield line[i:j]
            i = j

    line = "(3-5)*(6+17*4)/3"
    print(line)
    print(trans_infix_suffix(line))
    print("Value: ", suffix_exp_evaluator(trans_infix_suffix(line)))