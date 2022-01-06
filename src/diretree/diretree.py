import os
import pickle


class NODE:
    def __init__(self, path):
        self.name = None
        self.path = None
        self.revpath = None
        self.deepth = None
        self.mtime = None
        self.parent = None
        self.child = None

        self.name = os.path.basename(path)
        self.path = path
        stat = os.stat(path)
        self.mtime = stat.st_mtime

    def __str__(self):
        return self.name

    def get_parent(self):
        return self.parent

    def get_child(self):
        return self.child

    def set_revpath(self):
        if self.deepth == 0:
            self.revpath = "."
        elif self.deepth > 0:
            back = self.deepth
            self.revpath = \
                os.path.join("./", "/".join(self.path.split("/")[-back:]))
        else:
            print("Opps.")

    def set_parent(self, parent):
        self.parent = parent


class TREE:
    def traverse_tree_hire(self):
        data_out = []
        queue = []
        queue.append(self)
        while(queue):
            item = queue[0]
            queue = queue[1:]
            data_out.append((item, item.deepth))
            if item.nodetype == "directory":
                for child in item.child:
                    queue.append(child)
        return data_out

    def print_tree(self):
        nodes = self.traverse_tree_hire()
        node_dic = {}
        for node in nodes:
            if node[1] not in node_dic:
                node_dic[node[1]] = [node[0]]
            else:
                node_dic[node[1]].append(node[0])
        keys = list(node_dic.keys())
        keys.sort()
        for i in keys:
            for node in node_dic[i]:
                print(node.name, node.deepth, node.revpath, " ", end="")
            print()

    def compare_tree(self, other):
        record = []
        queue1 = []
        queue2 = []
        queue1.append(self)
        queue2.append(other)
        while(queue1):
            node1 = queue1[0]
            queue1 = queue1[1:]
            node2 = queue2[0]
            queue2 = queue2[1:]
            if node1.nodetype != node2.nodetype:
                record.append(
                    [node1.deepth, node1.revpath, "D/F", "type", node1.nodetype, node2.nodetype])
            elif node1.nodetype == "directory":
                child_dic1 = {cc.name: cc for cc in node1.child}
                child_dic2 = {cc.name: cc for cc in node2.child}
                childname1 = set(child_dic1.keys())
                childname2 = set(child_dic2.keys())
                com = childname1 & childname2
                unq_child1 = childname1 - childname2
                unq_child2 = childname2 - childname1
                for name in com:
                    queue1.append(child_dic1[name])
                    queue2.append(child_dic2[name])
                for name in unq_child1:
                    if child_dic1[name].nodetype == "directory":
                        nodetype_miss = "D"
                    else:
                        nodetype_miss = "F"
                    record.append([child_dic1[name].deepth, child_dic1[name].revpath, nodetype_miss, "miss", "Y", "N"])
                for name in unq_child2:
                    if child_dic2[name].nodetype == "directory":
                        nodetype_miss = "D"
                    else:
                        nodetype_miss = "F"
                    record.append([child_dic2[name].deepth, child_dic2[name].revpath, nodetype_miss, "miss", "N", "Y"])
            elif node1.nodetype == "file":
                if node1.size != node2.size:
                    record.append([node1.deepth, node1.revpath, "F", "size", node1.size, node2.size])
        return record

    def merge_tree(self, other):
        pass


class FILE_NODE(NODE, TREE):
    def __init__(self, path):
        NODE.__init__(self, path)
        self.nodetype = "file"
        self.size = os.stat(path).st_size


class DIR_NODE(NODE, TREE):
    def __init__(self, path):
        NODE.__init__(self, path)
        self.nodetype = "directory"
        self.child = []

    def add_child(self, child):
        self.child.append(child)


class LINK_NODE(NODE, TREE):
    pass


def make_tree(nodepath, parent=None):
    if os.path.islink(nodepath):
        print("node path is a link, ignored.")
        return
    elif os.path.isdir(nodepath):
        node = DIR_NODE(nodepath)
    elif os.path.isfile(nodepath):
        node = FILE_NODE(nodepath)
    else:
        print("opps.")
        if not os.path.exists(nodepath):
            print(nodepath, "not exists.")
        return
    if parent:
        parent.add_child(node)
        node.set_parent(parent)
        node.deepth = parent.deepth + 1
        node.set_revpath()
        if os.path.isdir(nodepath):
            for subnode in os.listdir(nodepath):
                subnodepath = os.path.join(nodepath, subnode)
                make_tree(subnodepath, node)
    else:
        node.deepth = 0
        node.set_revpath()
        if os.path.isdir(nodepath):
            for subnode in os.listdir(nodepath):
                subnodepath = os.path.join(nodepath, subnode)
                make_tree(subnodepath, node)
        return node
    return


def dump_tree(tree, dump_file):
    pickle.dump(tree, dump_file)
    return


def load_tree(dump_file):
    if os.path.exists(dump_file):
        tree = pickle.load(open(dump_file, "rb"))
    else:
        print(dump_file, "is not exists.")
        exit()
    return tree


def test():
    return 0


if __name__ == "__main__":
    test()
