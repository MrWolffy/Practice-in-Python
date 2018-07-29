# ADT Graph:
#     Graph(self)                 # 图构造操作
#     is_empty(self)              # 判断是否为一个空图
#     vertex_num(self)            # 获得这个图中的顶点个数
#     edge_num(self)              # 获得这个图中边的条数
#     vertices(self)              # 获得这个图中的顶点集合
#     edges(self)                 # 获得这个图中的边集合
#     add_vertex(self, vertex)    # 将顶点vertex加入这个图
#     add_edge(self, v1, v2)      # 将从v1到v2的边加入这个图
#     get_edge(self, v1, v2)      # 获得v1到v2边有关的信息，没有时返回特殊值
#     out_edges(self, v)          # 取得从v出发的所有边
#     degree(self, v)             # 检查v的度


inf = float("inf")


class GraphError(ValueError):
    pass


class Graph:
    """基于邻接矩阵实现的图"""
    def __init__(self, mat, unconn=0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise ValueError("Argument for 'Graph")
        self._mat = [mat[i][:] for i in range(vnum)]
        self._unconn = unconn
        self._vnum = vnum

    def vertex_num(self):
        return self._vnum

    def _invalid(self, v):
        return 0 > v or v >= self._vnum

    def add_vertex(self):
        raise GraphError("Adj-Matrix does not support 'add_vertex")

    def add_edge(self, vi, vj, val=1):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + " or " + str(vj) + " is not a valid vertex.")
        self._mat[vi][vj] = val

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + " or " + str(vj) + " is not a valid vertex.")
        return self._mat[vi][vj]

    def out_edges(self, vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._out_edges(self._mat[vi], self._unconn)

    @staticmethod
    def _out_edges(row, unconn):
        edges = []
        for i in range(len(row)):
            if row[i] != unconn:
                edges.append((i, row[i]))
        return edges


class GraphAL(Graph):
    """基于邻接表实现的图"""
    def __init__(self, mat=[], unconn = 0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise ValueError("Argument for 'GraphAL'.")
            self._mat = [Graph.out_edges(mat[i], unconn) for i in range(vnum)]
            self._vnum = vnum
            self._unconn = unconn

    def add_vertex(self):
        self._mat.append([])
        self._vnum += 1
        return self._vnum - 1

    def add_edge(self, vi, vj, val=1):
        if self._vnum == 0:
            raise GraphError("Cannot add edge to empty graph.")
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + " or " + str(vj) + " is not a valid vertex.")
        row = self._mat[vi]
        i = 0
        while i < len(row):
            if row[i][0] == vj:
                self._mat[vi][i] = (vj, val)
                return
            if row[i][j] > vj:
                break
            i += 1
        self._mat[vi].insert(i, (vj, val))

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError(str(vi) + " or " + str(vj) + " is not a valid vertex.")
        for i, val in self._mat[vi]:
            if i == vj:
                return val
        return self._unconn

    def out_edges(self, vi):
        if self._invalid(vi):
            raise GraphError(str(vi) + " is not a valid vertex.")
        return self._mat[vi]


if __name__ == '__main__':
    mat = [[1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1]]
    g = Graph(mat)
    print(g.vertex_num())
    print([[g.get_edge(i, j) for i in range(0, 5)] for j in range(0, 5)])
