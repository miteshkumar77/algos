import copy 
import texttable

def closure(attrs, fds):
    c = copy.copy(attrs)
    csz = len(c)
    nsz = -1
    while(csz != nsz):
        csz = len(c)
        for fd in fds:
            if all([component in c for component in fd.lhs]):
                c.update(fd.rhs)
        nsz = len(c)
    return c

def parseAttrs(strattrs):
    return set(strattrs.strip().split(','))

def parseFds(strfds):
    fds = strfds.split(';')
    fds = [s1.split('->') for s1 in fds]
    fds = [[s22.split(',') for s22 in s2] for s2 in fds]
    return [fd(set(s3[0]), set(s3[1])) for s3 in fds]

def superset(superset, subset):
    spr = set(superset)
    sub = set(subset)
    return spr.union(sub) == spr

def weakSuperset(superset, subset):
    spr = set(superset)
    sub = set(subset)
    return spr != sub and spr.union(sub) == spr

def checkFdEq(fds1, fds2, verbose=False):
    if verbose:
        isEq = True
        for _fd in fds1:
            if not _fd.rhs.issubset(closure(_fd.lhs, fds2)):
                print("fds1: {} not represented in fds2".format(_fd))
                isEq = False
        for _fd in fds2:
            if not _fd.rhs.issubset(closure(_fd.lhs, fds1)):
                print("fds2: {} not represented in fds1".format(_fd))
                isEq = False

        print("fds1: {} and fds2: {} are {}EQUAL".format(';'.join([str(i) for i in fds1]), ';'.join([str(i) for i in fds2]), "" if isEq else "NOT "))
        return isEq

    def intCheck(_fds1, _fds2, cont):
        return all([_fd.rhs.issubset(closure(_fd.lhs, _fds2)) for _fd in _fds1]) and (not cont or intCheck(_fds2, _fds1, False))

    return intCheck(fds1, fds2, True)


def getMinimalBasis(fds):
    
    projFds = []
    for _fd in fds:
        projFds.extend(_fd.getSplit())

    changed = True
    while changed:
        changed = False
        for idx, _fd in enumerate(projFds):
            nextProjFds = projFds[0:idx] + projFds[idx + 1:]
            if closure(_fd.lhs, nextProjFds) == closure(_fd.lhs, projFds):
                projFds = nextProjFds
                changed = True
                break

    changed = True
    while changed:
        changed = False
            
        for idx, _fd in enumerate(projFds):
            for remAttr in _fd.lhs:
                    
                nextProjFds = projFds[0:idx] + projFds[idx + 1:] + [fd(_fd.lhs - set([remAttr]), _fd.rhs)]
                    
                if closure(_fd.lhs - set([remAttr]), nextProjFds) == closure(_fd.lhs - set([remAttr]), projFds):
                    projFds = nextProjFds
                    changed = True
                break
            if changed:
                break

    return projFds

def getMinimalCover(fds):
    mbs = getMinimalBasis(fds)
    mp = dict()
    for _fd in mbs:
        strLhs = ','.join(sorted(list(_fd.lhs)))
        strRhs = ','.join(sorted(list(_fd.rhs)))
        if strLhs not in mp:
            mp[strLhs] = set()

        mp[strLhs].add(strRhs)
    
    mcv = []
    for k, v in mp.items():
        mcv.append(fd(parseAttrs(k), parseAttrs(','.join(v))))
    return mcv
    
def isLosslessChaseTest(decomp, allfds=[], verbose=False):

    def printChaseBoard(bd):
        txttbl = texttable.Texttable()
        txttbl.set_cols_align(["c" for _ in range(len(bd[0]))])
        txttbl.set_cols_valign(["c" for _ in range(len(bd[0]))])
        rows = [[k for k in sorted(list(bd[0].keys()))]] + [[d[k] if d[k] != 0 else ' ' for k in sorted(list(d.keys()))] for d in bd]
        txttbl.add_rows(rows)
        print(txttbl.draw() + "\n")


    allattrs = set() 
    [allattrs.update(d.attrs) for d in decomp]
    allfds = getMinimalBasis(allfds)
    
    table = []
    for idx, r in enumerate(decomp):
        table.append({k:(0 if k in r.attrs else idx + 1) for k in allattrs})
    
    changed = True
    finished = False
    if verbose:
        print("Start Chase Algorithm")
        printChaseBoard(table)
    
    while changed and not finished:
        changed = False
        for _fd in allfds:
            commonSubScripts = dict()
            for row in table:
                rowId = '|'.join([str(row[fdAttr]) for fdAttr in sorted(list(_fd.lhs))])
                if not rowId in commonSubScripts:
                    commonSubScripts[rowId] = row[list(_fd.rhs)[0]]
                else:
                    commonSubScripts[rowId] = min(commonSubScripts[rowId], row[list(_fd.rhs)[0]])
            
            for row in table:
                rowId = '|'.join([str(row[fdAttr]) for fdAttr in sorted(list(_fd.lhs))])
                
                if row[list(_fd.rhs)[0]] != commonSubScripts[rowId]:
                    row[list(_fd.rhs)[0]] = commonSubScripts[rowId]
                    finished = finished or all([v == 0 for v in row.values()])
                    changed = True
                
            if changed:
                if verbose:
                    print("Apply {}".format(_fd))
                    printChaseBoard(table)
                break
    
    if verbose:
        if finished:
            print("Row without subscripts. Lossless decomposition")
        else:
            print("No row without subscripts. Lossy decomosition")
    return finished

class fd():
    
    def __init__(self, _lhs, _rhs):
        if not type(_lhs) is type(set()):
            raise Exception('invalid type for fd lhs')

        if not type(_rhs) is type(set()):
            raise Exception('invalid type for fd rhs')

        self.lhs = _lhs
        self.rhs = _rhs
    
    def __repr__(self):
        return "{}->{}".format(','.join(sorted(list(self.lhs))), ','.join(sorted(list(self.rhs))))
    
    def getSplit(self):
        return [fd(copy.copy(self.lhs), set([i])) for i in self.rhs]


class relation():

    def __init__(self, _attrs, _fds):
        if not type(_attrs) is type(set()):
            raise Exception('invalid type for relation attrs')

        self.attrs = _attrs
        self.fds = _fds
        self.minKeys = None
        self.supKeys = None

    def __repr__(self):
        return "R({})   F{{{}}}".format(','.join(sorted(list(self.attrs))), ';'.join([str(f) for f in self.fds]))

    def isSupKey(self, subAttrs):
        return closure(subAttrs, self.fds) == self.attrs
    
    def getKeys(self, verbose=False):
        
        if not (self.minKeys is None or self.supKeys is None):
            return (self.minKeys, self.supKeys)

        minKeys = []
        supKeys = []
        fSupKeys = []
        curComb = set()

        def iterCombs(attrItr):
            try:
                currAttr = next(attrItr)
                iterCombs(copy.copy(attrItr))
                curComb.add(currAttr)
                iterCombs(copy.copy(attrItr))
                curComb.remove(currAttr)
            except StopIteration:
                if self.isSupKey(curComb):
                    if verbose:
                        print("{{{}}}+ => {{{}}}".format(','.join(curComb), ','.join(closure(curComb, self.fds))))
                    supKeys.append(copy.copy(curComb))
        iterCombs(iter(self.attrs))
        
        for k in supKeys:
            if not any([weakSuperset(k, k2) for k2 in supKeys]):
                minKeys.append(k)
            else:
                fSupKeys.append(k)
        self.minKeys = minKeys
        self.supKeys = fSupKeys

        return (self.minKeys, self.supKeys)

    def getProjection(self, subAttrs):
        projFds = []
        
        curComb = set()

        def iterCombs(attrItr):
            try:
                currAttr = next(attrItr)
                iterCombs(copy.copy(attrItr))
                curComb.add(currAttr)
                iterCombs(copy.copy(attrItr))
                curComb.remove(currAttr)
            except StopIteration:
                if curComb.issubset(subAttrs):
                    addRhs = closure(curComb, self.fds).intersection(subAttrs).difference(curComb)
                    addLhs = copy.copy(curComb)
                    if len(addRhs) > 0:
                        projFds.append(fd(addLhs, addRhs))


        iterCombs(iter(subAttrs))
    
        projFds = getMinimalBasis(projFds)

        return relation(subAttrs, projFds)           
    
    def isBCNF(self, verbose=False):
        violation = False
        for _fd in self.fds:
            if _fd.rhs.issubset(_fd.lhs):
                continue
            elif verbose:
                print("not trivial: {}".format(_fd))

            if self.isSupKey(_fd.lhs):
                continue
            elif verbose:
                print("lhs not super key: {}, closure(lhs) = {}".format(_fd, ','.join(closure(_fd.lhs, self.fds))))

            violation = True
        if verbose:
            print("{} is BCNF".format(self) if not violation else "{} is NOT BCNF".format(self))
        return not violation

    def is3NF(self, verbose=False):
        (minKeys, _) = self.getKeys()
        print(minKeys)
        primeAttrs = set()
        for k in minKeys:
            primeAttrs = primeAttrs.union(k)

        violation = False
        for _fd in self.fds:
            if _fd.rhs.issubset(_fd.lhs):
                continue
            elif verbose:
                print("not trivial: {}".format(_fd))

            if self.isSupKey(_fd.lhs):
                continue
            elif verbose:

                print("lhs not super key: {}, closure(lhs) = {}".format(_fd, ','.join(closure(_fd.lhs, self.fds))))

            if all([e in primeAttrs for e in _fd.rhs]):
                continue
            elif verbose:
                print("rhs not all prime attrs: {}".format(_fd))

            violation = True

        if verbose:
            print("{} is 3NF".format(self) if not violation else "{} is NOT 3NF".format(self))
        return not violation
            

    def decomp3NF(self, verbose=False):
        decomp = []
        needsKey = True
        
        if self.is3NF():
            raise Exception("Decomp 3NF on a 3NF relation")
        
        for _fd in getMinimalCover(self.fds):
            if not any([_fd.lhs.union(_fd.rhs).issubset(i.attrs) for i in decomp]):
                decomp.append(self.getProjection(_fd.lhs.union(_fd.rhs)))
                
                if verbose:
                    print("Add relation to 3NF decomp: {}".format(decomp[-1]))
                    self.isBCNF(verbose=True)
                    

                if any([k.issubset(decomp[-1].attrs) for k in self.getKeys()[0]]):
                    needsKey = False
                    if verbose:
                        print("relation {} contains attributes of key {{{}}}".format(decomp[-1], ','.join(k)))
        
        if needsKey:
            if verbose:
                print("No decomp relations contain a key so far")

            (k, _) = self.getKeys()
            decomp.append(self.getProjection(copy.copy(k[0])))

            if verbose: 
                print("Add relation to 3NF decomp: {}".format(decomp[-1]))
                self.isBCNF(verbose=True)

        
        return decomp

    def decompBCNF(self, verbose=False):
        decomp = []
        self.decompHelper(decomp, verbose, "")
        if verbose:
            unionFds = []
            [unionFds.extend(el.fds) for el in decomp]
            print("DEPENDENCY PRESERVING BCNF DECOMP" if checkFdEq(self.fds, unionFds, verbose=True) else "NOT DEPENDENCY PRESERVING BCNF DECOMP")
        return decomp
        
    def decompHelper(self, decompSet, verbose, idstr):
        for _fd in self.fds:
            if not (_fd.rhs.issubset(_fd.lhs) or self.isSupKey(_fd.lhs)):
                Xp = closure(_fd.lhs, self.fds)
                if verbose:
                    print("NOT BCNF, continue recursion: {}: {}".format(idstr, self))
                self.getProjection(Xp).decompHelper(decompSet, verbose, idstr + "_1")
                self.getProjection(self.attrs - (Xp - _fd.lhs)).decompHelper(decompSet, verbose, idstr + "_2")
                return
        if verbose: 
            print("BCNF, stop recursion: {}: {}".format(idstr, self))
        decompSet.append(self)






