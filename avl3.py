import sys


class Node:
    __slots__ = ("key", "left", "right", "h")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.h = 1


def h(v):
    return v.h if v else 0


def upd(v):
    v.h = 1 + max(h(v.left), h(v.right))


def bal(v):
    return h(v.right) - h(v.left)


def rot_left(a):
    b = a.right
    a.right = b.left
    b.left = a
    upd(a)
    upd(b)
    return b


def rot_right(a):
    b = a.left
    a.left = b.right
    b.right = a
    upd(a)
    upd(b)
    return b


def fix(v):
    upd(v)
    if bal(v) == 2:
        if bal(v.right) < 0:
            v.right = rot_right(v.right)
        return rot_left(v)
    if bal(v) == -2:
        if bal(v.left) > 0:
            v.left = rot_left(v.left)
        return rot_right(v)
    return v


def insert(v, x):
    if v is None:
        return Node(x)
    if x < v.key:
        v.left = insert(v.left, x)
    elif x > v.key:
        v.right = insert(v.right, x)
    else:
        return v
    return fix(v)


def pop_min(v):
    if v.left is None:
        return v.right, v.key
    v.left, m = pop_min(v.left)
    return fix(v), m


def remove(v, x):
    if v is None:
        return None
    if x < v.key:
        v.left = remove(v.left, x)
    elif x > v.key:
        v.right = remove(v.right, x)
    else:
        if v.left is None:
            return v.right
        if v.right is None:
            return v.left
        v.right, v.key = pop_min(v.right)
    return fix(v)


class AVL:
    def __init__(self):
        self.root = None

    def add(self, x):
        self.root = insert(self.root, x)

    def delete(self, x):
        self.root = remove(self.root, x)

    def exists(self, x):
        v = self.root
        while v:
            if x == v.key:
                return True
            v = v.left if x < v.key else v.right
        return False

    def next(self, x):
        v, ans = self.root, None
        while v:
            if v.key >= x:
                ans = v.key
                v = v.left
            else:
                v = v.right
        return ans

    def prev(self, x):
        v, ans = self.root, None
        while v:
            if v.key <= x:
                ans = v.key
                v = v.right
            else:
                v = v.left
        return ans

    def preorder(self):
        res = []
        st = [self.root] if self.root else []
        while st:
            v = st.pop()
            res.append(v.key)
            if v.right:
                st.append(v.right)
            if v.left:
                st.append(v.left)
        return res


def main():
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    t = AVL()
    out = []
    i = 1
    for _ in range(q):
        cmd = data[i]
        i += 1
        if cmd == b"root":
            out.append(str(t.root.key) if t.root else "Empty")
        elif cmd == b"height":
            out.append(str(h(t.root)))
        elif cmd == b"print":
            res = t.preorder()
            out.append(" ".join(map(str, res)) if res else "Empty")
        else:
            x = int(data[i])
            i += 1
            if cmd == b"add":
                t.add(x)
            elif cmd == b"del":
                t.delete(x)
            elif cmd == b"exists":
                out.append("YES" if t.exists(x) else "NO")
            elif cmd == b"next":
                ans = t.next(x)
                out.append("None" if ans is None else str(ans))
            elif cmd == b"prev":
                ans = t.prev(x)
                out.append("None" if ans is None else str(ans))
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
