
import math
import random
from graphics import *

WX = 500
WY = 200
e = 0.000001

def argMax(data):
    m = max(data)
    for i in range(len(data)):
        if data[i] == m: return i
    return None
def argMin(data):
    m = min(data)
    for i in range(len(data)):
        if data[i] == m: return i
    return None

class Node(object):
    def __init__(self, name):
        self.name = name
        self.children = dict()

class Attribute(object):
    def __init__(self, name, values):
        self.name = name
        self.values = values[:]

class DecisionTree(object):
    # the goal attribute is located at last list of attributes
    def __init__(self, method, attributes):        
        if method != 'quinlan' and method != 'gain':
            print('Error! The method is only two values which is quinlan or gain')
        self.method = method
        self.attributes = attributes
        self.goal = attributes[-1]        
        print('The decision tree is initalized with ' + method + '\'s algorithm')

    def take(self, attribute, j, examples):
        index = 0
        for i in range(len(self.attributes)):
            if self.attributes[i].name == attribute.name:
                index = i
                break
        return [ex for ex in examples if ex[index] == j]
    
    def pluralityValue(self, examples):
        count = {}        
        for att in self.goal.values:
            count[att] = 0
        
        for ex in examples:
            count[ex[-1]] += 1

        index = argMax(list(count.values()))
        return list(count.keys())[index]        

    def onlyOne(self, examples):
        a = [ex[-1] for ex in examples]        
        return len(set(a)) == 1

    def Quinlan(self, attribute, examples):

        if len(set(attribute.values)) >= len(examples): return 0
        
        cnt = 0        
        for j in attribute.values:
            examples_AJ = self.take(attribute, j, examples)            
            if len(examples_AJ) == 0: continue
            if self.onlyOne(examples_AJ): cnt += 1            
        
        return cnt / len(attribute.values)
    
    def InformationGain(self, attribute, examples):
        
        if len(set(attribute.values)) >= len(examples): return 100
        
        result = 0
        bt = len(examples)
        for j in attribute.values:
            example_AJ = self.take(attribute, j, examples)
            bj = len(example_AJ)
            if bj == 0: continue
            s = 0
            for i in self.goal.values:
                examples_gi = self.take(self.goal, i, example_AJ)
                b_ri = len(examples_gi)
                pi = b_ri / bj                
                s += -pi * math.log2(pi + e)
            result += (bj / bt) * s
        
        return result

    def choose(self, attributes, examples):        
        if self.method == 'quinlan':
            v = [self.Quinlan(attribute, examples)
                 for attribute in attributes[: len(attributes) - 1]]            
            M = max(v)
            m = 100000
            result = attributes[0]
            for i in range(len(v)):
                 if v[i] == M and m > len(attributes[i].values):
                     result = attributes[i]
                     m = len(attributes[i].values)
            return result
        else:
            v = [self.InformationGain(attribute, examples)
                 for attribute in attributes[: len(attributes) - 1]]            
            return attributes[argMin(v)]

    def minus(self, attributes, attribute):
        return [a for a in attributes if a.name != attribute.name]
        
    # the examples is a list of list order of attributes
    def buildTree(self, examples, attributes, parent_examples):
        if len(examples) == 0:
            name = self.pluralityValue(parent_examples)
            return Node(name)
        # every examples have only one of value of goal attribute 
        common = self.onlyOne(examples)                  
        if common: return Node(examples[0][-1])

        if len(attributes) == 1:
            name = self.pluralityValue(examples)
            return Node(name)
        
        att = self.choose(attributes, examples)
        parent = Node(att.name)        
        for j in att.values:
            ex = self.take(att, j, examples)
            at = self.minus(attributes, att)
            subTree = self.buildTree(ex, at, examples)
            parent.children[j] = subTree            
        return parent
        
        
    def fit(self, data):
        print("Fitting the data... ", end='')
        self.root = self.buildTree(data, self.attributes, [])
        print("OK")

    def findSolution(self, root, example):
        if len(root.children) == 0: return root.name
        index = 0
        for i in range(len(self.attributes)):
            if self.attributes[i].name == root.name:
                index = i
                break
        value = example[index]
        for attribute in self.attributes:
            if attribute.name == root.name:                 
                 return self.findSolution(root.children[value], example)
    
    def predict(self, test):                        
        return self.findSolution(self.root, test)

def travelTheTree(tree, s):        
    if len(tree.children) == 0:
        print(s + " ==> " + tree.name)
        return 1
    t = s
    if len(s) > 0: t += " and "        
    t += "(" + tree.name    
    max_height = 0
    for c in tree.children.keys():
        d = travelTheTree(tree.children[c], t + " = " + c + ") ")
        max_height = max(max_height, d)
    return max_height + 1

def readData(fileName):
    f = open(fileName, 'r')
    na = int(f.readline()) #this is number of attributes
    attributes = []
    for i in range(na):    
        L = (f.readline()).split()
        name = str(L[0])
        values = L[1 : ]        
        attributes.append(Attribute(name, values))

    examples = []    
    ne = int(f.readline()) #this is number of examples
    for i in range(ne):
        L = (f.readline()).split()        
        examples.append(L)

    return (attributes, examples)    

def readTestData(fileName):
    f = open(fileName, 'r')
    examples = [line.split() for line in f]
    f.close()
    return examples

def randColor():
    r = random.randrange(100, 256)
    b = random.randrange(100, 256)
    g = random.randrange(100, 256)
    color = color_rgb(r, g, b)
    return color

def draw(win, node, top, L, R, h, a, color):    
    
    bottom = top + h
    I = Point((L + R) / 2, (top + bottom) / 2)    
    
    new_top = bottom + a
    
    n_children = len(node.children)

    if n_children > 0: 
    
        delta = (R - L) / n_children

        keys = list(node.children.keys())
        values = list(node.children.values())

        color2 = randColor()
        
        for i in range(len(keys)):        
            I1 = draw(win, values[i], new_top, L + i * delta, L + (i + 1) * delta, h, a, color2)
            line = Line(I, I1)

            center = Point((I.getX() + I1.getX()) / 2, (I.getY() + I1.getY()) / 2)
            message = Text(center, keys[i])
            message.draw(win)
            
            line.draw(win)

    m = min(h / 2, (L + R) / 2)    
    pa = Point(I.getX() - m, top)
    pb = Point(I.getX() + m, bottom)
    #C = Circle(I, min(h / 2, (L + R) / 2))
    C = Oval(pa, pb)
    C.setFill(color)
    C.draw(win)
    
    message = Text(I, node.name)
    message.draw(win)
    
    return I

def main(fpath, method):
    (attributes, examples) = readData(fpath)

    dt = DecisionTree(method, attributes)
    
    dt.fit(examples)

    print("All rules from the data:")
    
    height = travelTheTree(dt.root, '')
    
    win = GraphWin("Decision Tree", WX + 20, WY + 200)
    
    a = WY / (5 * height - 1)
    h = 4 * a        

    color = randColor()
    
    draw(win, dt.root, 10, 10, WX + 10, h, a, color)

    '''examples = readTestData(ftest)

    n_test = len(examples)
    cnt = 0
    
    for example in examples:
        data = example[ : len(example) - 1]
        ans = dt.predict(data)
        if (example[-1] == ans): cnt += 1

    accuracy = cnt / n_test
    print("Accuracy = " + str(accuracy))'''
    
    while True:
        data = input("Enter your test case(press \"exit\" to exit): ")
        data = data.split()
        if data[0] == 'exit': break
        print("Output: " + str(dt.predict(data)))

fpath = input("Enter the path of file train: ")
method = input("Enter the method which you use to build the decision tree(quinlan : Quinlan, gain : InformationGain): ")
while (method != 'quinlan' and method != 'gain'):
    method = input('Try again: ')
#ftest = input("Enter the path of file test: ")
main(fpath, method)




