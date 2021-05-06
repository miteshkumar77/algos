import copy 
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

def checkFdEq(fds1, fds2):
    
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
        strLhs = ','.join(_fd.lhs)
        strRhs = ','.join(_fd.rhs)
        if strLhs not in mp:
            mp[strLhs] = set()

        mp[strLhs].add(strRhs)
    
    mcv = []
    for k, v in mp.items():
        mcv.append(fd(parseAttrs(k), parseAttrs(','.join(v))))
    return mcv
    

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
        return "R({})\nF{{{}}}".format(','.join(sorted(list(self.attrs))), ';'.join([str(f) for f in self.fds]))

    def isSupKey(self, subAttrs):
        return closure(subAttrs, self.fds) == self.attrs
    
    def getKeys(self):
        
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

        return not violation
            

    def decomp3NF(self):
        decomp = []
        needsKey = True
        
        if self.is3NF():
            raise Exception("Decomp 3NF on a 3NF relation")
        
        for _fd in getMinimalCover(self.fds):
            if not any([_fd.lhs.union(_fd.rhs).issubset(i.attrs) for i in decomp]):
                decomp.append(self.getProjection(_fd.lhs.union(_fd.rhs)))

                #if not decomp[-1].is3NF():
                    #raise Exception("Decomposed Relation was not 3NF")

                if any([k.issubset(decomp[-1].attrs) for k in self.getKeys()[0]]):
                    needsKey = False
        
        if needsKey:
            (k, _) = self.getKeys()
            decomp.append(self.getProjection(copy.copy(k[0])))
        
        return decomp

    def decompBCNF(self):
        decomp = []
        self.decompHelper(decomp)
        return decomp
        
    def decompHelper(self, decompSet):
        for _fd in self.fds:
            if not (_fd.rhs.issubset(_fd.lhs) or self.isSupKey(_fd.lhs)):
                Xp = closure(_fd.lhs, self.fds)
                self.getProjection(Xp).decompHelper(decompSet)
                self.getProjection(self.attrs - (Xp - _fd.lhs)).decompHelper(decompSet)
                return
            
        decompSet.append(self)





