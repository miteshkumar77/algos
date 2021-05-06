
class scheduleElem():
    
    def __init__(self, _tr, _op, _res):
        self.tr = _tr
        self.op = _op
        self.res = _res
    def __repr__(self):
        return "{}{}({})".format(self.op, self.tr, self.res)

def getElem(strelem):
    strtr = ''
    op = ''
    for i in strelem[0:strelem.find('(')]:
        if '0' <= i and i <= '9':
            strtr += i
        else:
            op += i
    resource = strelem[strelem.find('(') + 1 : strelem.find(')')]
    return scheduleElem(strtr, op, resource)
    

def parser(strinput):
    tmp = strinput.split(" ")
    return [getElem(e) for e in tmp]
    

def getConflictsBrutalForce(strinput):
    elems = parser(strinput)
    conflicts = []
    for i in reversed(range(len(elems))):
        for j in range(i + 1, len(elems)):
            if elems[j].res == elems[i].res and elems[j].tr != elems[i].tr and (elems[j].op == "w" or elems[i].op == "w"):
                conflicts.append((elems[i], elems[j]))
    
    return conflicts

def isSerializable(strinput):
    conflicts = getConflictsBrutalForce(strinput)
    graph = [(e[0].tr, e[1].tr) for e in conflicts]
    alist = dict()
    pre = dict()
    post = dict()
    for e in graph:
        pre[e[0]] = False
        pre[e[1]] = False
        post[e[0]] = False
        post[e[1]] = False 
        if e[0] not in alist:
            alist[e[0]] = set()
        if e[1] not in alist:
            alist[e[1]] = set()
        alist[e[0]].add(e[1])

    def dfs(node):
        if pre[node] == True and post[node] == False:
            return True
        if post[node] == True:
            return False

        pre[node] = True 
        for neighbor in alist[node]:
            if dfs(neighbor):
                return True
        post[node] = True
        return False
    for k in pre.keys():
        if dfs(k):
            return False

    return True
    
# inputstr = "r1(x) r3(y) w3(y) r1(y) w1(x) r3(z) r3(z) r2(w) w2(y) w2(z)"
# inputstr = "r2(y) r1(x) r3(y) w2(y) r2(z) r1(z) w2(z) w3(z) w1(x)"
# inputstr = "r3(y) w3(y) r1(x) r1(y) w1(x) r2(x) r2(z) w3(z) w2(w)"

#inputstr = "r1(w) r2(x) r2(y) r1(x) w2(z) r3(z) w3(z) w1(x) w3(x) r3(y) w3(y)"

inputstr = "r1(x) w1(x) w1(z) w3(z) r4(z) w2(w) r4(w) r2(w) r3(x) r2(z) w4(w) w4(z)"

conflicts = getConflictsBrutalForce(inputstr)

for c in conflicts:
    print(c)

isSer = isSerializable(inputstr)

if isSer:
    print("SERIALIZABLE:")
else:
    print("NOT SERIALIZABLE:")

for c in conflicts:
    print("{} ===> {}".format(c[0], c[1]))






















