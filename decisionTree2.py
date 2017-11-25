
import math

class Attribute:
    def __init__(self, name):
        self.name = name
        self.data = []

class Example: #this contains dict mapping pair: Attribute -> Value of that attribute
    def __init__(self, data, goalAtt):
        self.data = data
        self.goal = goalAtt    

class DecisionTreeNode:
    def __init__(self, name):
        self.name = name
        self.children = {}

def take(A, v, examples):
    result = []
    for ex in examples:
        #for j in ex.data.keys():
         #   print j.name, ': ', ex.data[j],'\n'
        if (ex.data[A] == v):
            result.append(ex)
        #print '\n'
    return result

def pluralityValue(examples):
    count = {}
    goal = examples[0].goal
    for att in goal.data:
        count[att] = 0
    for ex in examples:
        count[ex.data[goal]] += 1

    M = 0
    name = ''
    for att in goal.data:
        if (count[att] > M):
            M = count[att]
            name = att
    return DecisionTreeNode(name)

def TA(att, examples):
    
    result = 0
    bt = len(examples)
    goal = examples[0].goal
    for j in att.data:
        attAJ = take(att, j, examples)
        bj = len(attAJ)    
        Sum = 0
        for i in goal.data:
            bri = 0
            for ex in attAJ:
                if (ex.data[goal] == i):
                    bri += 1            
            if (bri > 0):
                Sum += (float(-bri) / bj) * math.log(float(bri) / bj, 2)
            
        
        result = result + (float(bj) / bt) * Sum
    return result

def Quinlan(att, examples):
    #print att.name
    result = 0
    goal = examples[0].goal
    for j in att.data:
        attAJ = take(att, j, examples)
     #   print len(attAJ)
        if (len(attAJ) <= 1): continue
        
        if (len(common(attAJ)) > 0):
            result += 1
    return result    

def argmin(attributes, examples):
    M = 0.0
    result = attributes[0]
    goal = examples[0].goal
    '''for att in attributes:        
        if (att.name != goal.name): # skip the goal attribute
            T = TA(att, examples)
            if (T > M):
                result = att
                M = T
    print '==> choose: ', result.name
    '''
    for att in attributes:        
        if (att.name != goal.name): # skip the goal attribute
            T = Quinlan(att, examples)
            if (T > M):
                result = att
                M = T
            #print T
    print ('==> choose: ', result.name)
    return result

def minus(attributes, A):
    result = []
    for att in attributes:
        if (att.name != A.name):
            result.append(att)
    return result

def common(examples):
    goal = examples[0].goal
    result = examples[0].data[goal]
    start = examples[0].data[goal]
    for ex in examples:
        if (ex.data[goal] != start):
            return ''
    return result

def buildTree(examples, attributes, parent_examples): #this can build the tree
    if (len(examples) == 0):
        return pluralityValue(parent_examples)
    else:
        if ( len(common(examples)) > 0 ):
            return DecisionTreeNode(common(examples))
        else:
            if ( len(attributes) == 1):
                return pluralityValue(examples)
            else:        
                A = argmin(attributes, examples)    #this returns a attribute chosen to split
                tree = DecisionTreeNode(A.name)
                for vk in A.data:
                    exs = take(A, vk, examples)
                    ats = minus(attributes, A)
                    subtree = buildTree(exs, ats, examples)
                    #print subtree.name
                    tree.children[vk] = subtree     #this add a pair <branch, subtree>
                return tree

#-------------------------------------------------#
def travelTheTree(tree, s):
    t = s
    if (len(s) > 0):
        t = t + ' and '
    t = t + tree.name    
    if (len(tree.children) == 0):
        print (t)
        return
    for c in tree.children.keys():
        travelTheTree(tree.children[c], t + ':' + c)
# tesing....
def findSolution(tree, ex, attributes):
    if (len(tree.children) == 0):
        return tree.name    
    for att in attributes:
        if (att.name == tree.name):
            return findSolution(tree.children[ex.data[att]], ex, attributes)

    
def test(tree, examples, attributes):
    total = len(examples)
    goal = examples[0].goal
    cnt = 0 
    for ex in examples:
        result = findSolution(tree, ex, attributes)
        if (result == ex.data[goal]):
            cnt += 1        
    return float(cnt) / total * 100

# main
#fileName = raw_input("Enter the file name: ")
fileName = 'data3.txt'
f = open(fileName, 'r')
na = int(f.readline()) #this is number of attributes
attributes = []
for i in range(0, na):    
    l = (f.readline()).split()
    a = Attribute(str(l[0]))
    a.data = l[1 : len(l)]
    attributes.append(a)

examples = []
goal = attributes[na - 1]
ne = int(f.readline()) #this is number of examples
for i in range(0, ne):
    l = (f.readline()).split()
    data = {}
    for j in range(0, na):        
        data[attributes[j]] = l[j]            
    examples.append(Example(data, goal))

    
root = buildTree(examples, attributes, [])
travelTheTree(root, '')

'''ntest = int(f.readline())
examples = []
for i in range(0, ntest):
    l = (f.readline()).split()
    data = {}
    for j in range(0, na):        
        data[attributes[j]] = l[j]            
    examples.append(Example(data, goal))

print ('percent = ', test(root, examples, attributes))'''
