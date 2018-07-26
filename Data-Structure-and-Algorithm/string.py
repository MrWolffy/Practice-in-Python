# ADT String:
#     String(self, sseq)          # 基于字符序列sseq建立一个字符串
#     is_empty(self)              # 判断本字符串是否空串
#     len(self)                   # 取得字符串的长度
#     char(self, index)           # 取得字符串中位置index的字符
#     substr(self, a, b)          # 取得字符串中[a:b]的子串，左闭右开区间
#     match(self, string)         # 查找串string在本字符串中第一个出现的位置
#     concat(self, string)        # 做出本字符串与另一字符串string的拼接串
#     subst(self, str1, str2)     # 做出将本字符串里的子串str1都替换为str2的结果串


def maching_KMP(t: str, p: str, pnext: list) -> int:
    """KMP串匹配，主函数"""
    j, i = 0, 0
    n, m = len(t), len(p)
    while j < n and i < m:
        if i == -1 or t[j] == p[i]:
            j, i = j + 1, i + 1
        else:
            i = pnext[i]
    if i == m:
        return j - 1
    return -1


def gen_pnext(p: str) -> list:
    """生成针对p中各位置i的下一检查位置表，用于KMP算法"""
    i, k, m = 0, -1, len(p)
    pnext = [-1] * m
    while i < m - 1:
        if k == -1 or p[i] == p[k]:
            i, k = i + 1, k + 1
            if p[i] == p[k]:
                pnext[i] = pnext[k]
            else:
                pnext[i] = k
        else:
            k = pnext[k]
    return pnext


if __name__ == '__main__':
    t, p = "ababcabcacbab", "abcac"
    print(maching_KMP(t, p, gen_pnext(p)))
