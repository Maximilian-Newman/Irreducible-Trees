# onlu accurate up to 14 nodes

TREES = []

def get_tree(ID):
    for tree in TREES:
        if tree.ID == ID:
            return tree

lastID = 0
def new_ID():
    global lastID
    lastID += 1
    return lastID



class Node:
    def __init__(self, ID, parentID):
        self.connections = []
        self.ID = ID
        self.parentID = parentID
    
    def size(self):
        return len(self.connections)
    
    def deep_size(self, exclude=None):
        size = 1
        for n in self.connections:
            node = get_tree(self.parentID).get_node(n)
            if node.ID != exclude:
                size += node.deep_size(self.ID)
        return size
    
    def depth(self, exclude=None):
        depth = 0
        for n in self.connections:
            node = get_tree(self.parentID).get_node(n)
            if node.ID != exclude:
                nD = node.depth(self.ID)
                if nD > depth:
                    depth = node.depth(self.ID)
        return depth + 1

    def clone(self, parentID):
        new = Node(self.ID, parentID)
        new.connections = self.connections.copy()
        return new

    def get_text(self, exclude):
        text = "("
        for n in self.connections:
            node = get_tree(self.parentID).get_node(n)
            if node.ID != exclude:
                text += node.get_text(self.ID)
        text += ")"
        return text

    def sort(self):
        new = []
        stats = []
        for i in range(0,len(self.connections)):
            size = get_tree(self.parentID).get_node(self.connections[i]).size()
            depth = get_tree(self.parentID).get_node(self.connections[i]).depth()
            stats.append([size, depth, i])
            
        stats = sorted(stats)
        for n in stats:
            new.append(self.connections[n[2]])
        
        self.connections = new


class Tree:
    def __init__(self):
        self.nodes = []
        self.ID = new_ID()

    def get_node(self, ID):
        for node in self.nodes:
            if node.ID == ID:
                return node

    def biggest_node_size(self):
        size = 0
        for node in self.nodes:
            if node.size() > size:
                size = node.size()
        return size

    def sort(self):
        for node in self.nodes:
            node.sort()

    def num_reducible(self):
        num = 0
        for node in self.nodes:
            if len(node.connections) == 2:
                num += 1
        return num
                

    def clone(self):
        new = Tree()
        for i in range(0, len(self.nodes)):
            new.nodes.append(self.nodes[i].clone(new.ID))
        return new

    def get_texts(self):
        texts = []
        biggest = self.biggest_node_size()
        for node in self.nodes:
            if node.size() == biggest:
                texts.append(node.get_text(None))
        return texts


def compare(tree1, tree2):
    
    if tree1.biggest_node_size() != tree2.biggest_node_size():
        return False
    
    texts1 = tree1.get_texts()
    texts2 = tree2.get_texts()

    for t1 in texts1:
        for t2 in texts2:
            if t1 == t2:
                return True
    
    return False
    """
    sizes1 = []
    sizes2 = []
    depth1 = []
    depth2 = []
    for node in tree1.nodes:
        sizes1.append([node.size(), node.depth()])
    for node in tree2.nodes:
        sizes2.append([node.size(), node.depth()])
    sizes1 = sorted(sizes1)
    sizes2 = sorted(sizes2)
    
    if sizes1 == sizes2:
        return True

    return False
    """


TREES.append(Tree())
TREES[0].nodes.append(Node(0,0))
numNodes = 1

while True:
    i=0
    while i < len(TREES):
        tree1 = TREES[i]
        rem = False
        if tree1.num_reducible() >=2:
            TREES.pop(i)
            rem = True
        else:
            for tree2 in TREES:
                if tree1.ID != tree2.ID:
                    if compare(tree1, tree2):
                        TREES.pop(i)
                        rem = True
                        break
        if rem == False:
            i+=1
    """
    for tree in TREES:
        sizes = []
        for node in tree.nodes:
            sizes.append(node.size())
        print(tree.get_texts(), "       ", sorted(sizes))"""

    numIrreducible = 0
    for tree in TREES:
        if tree.num_reducible() == 0:
            numIrreducible += 1
            #print(tree.get_texts())

    
    print("Number of nodes: {:<5} Irreducible trees: {:<5} Tracked trees (debugging): {:<5}".format(numNodes, numIrreducible, len(TREES)))
    newTrees = []
    for tree in TREES:
        for i in range(0, len(tree.nodes)):
            nTree = tree.clone()
            newNode = Node(len(tree.nodes), nTree.ID)
            newNode.connections.append(i)
            nTree.nodes.append(newNode)
            nTree.nodes[i].connections.append(len(tree.nodes))
            for node in nTree.nodes:
                node.parentID = nTree.ID
            newTrees.append(nTree)
    
    TREES = newTrees

    for tree in TREES:
        tree.sort()
    
    numNodes += 1
    
