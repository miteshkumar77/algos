import normalization as norm
import unittest

class TestNormalization(unittest.TestCase):
    
    def test_closure(self):
        attrs = norm.parseAttrs('A,B,C,D,E,F,G')
        fds = norm.parseFds('A,C->D;A,C->E;B,F->E;A,F,G->B;B,D->C')
        R = norm.relation(attrs, fds)
        tests = [
                    ('A', R, 'A'),
                    ('A,B', R, 'A,B'),
                    ('A,C', R, 'A,C,D,E'),
                    ('B,D', R, 'B,C,D'),
                    ('A,B,C', R, 'A,B,C,D,E'),
                    ('A,C,F,G', R, 'A,B,C,D,E,F,G')
                ]
        for t in tests:
            self.assertEqual((norm.closure(norm.parseAttrs(t[0]), fds)), norm.parseAttrs(t[2]), "closure wrong ans")
   

    def test_keys(self):
        attrs = norm.parseAttrs('A,B,C,D,E,F,G')
        fds = norm.parseFds('A,C->D;A,C->E;B,F->E;A,F,G->B;B,D->C')
        R = norm.relation(attrs, fds)

        (minKeys, supKeys) = R.getKeys()

        print(R)
        print("minKeys: {}".format(";".join(["(" + ",".join(sorted(list(s))) + ")" for s in minKeys])))
        print("supKeys: {}".format(";".join(["(" + ",".join(sorted(list(s))) + ")" for s in supKeys])))
        print("")
        attrs = norm.parseAttrs('A,B,C')
        fds = norm.parseFds('A,B->C')
        R = norm.relation(attrs, fds)

        (minKeys, supKeys) = R.getKeys()
        (minKeys, supKeys) = R.getKeys()
        (minKeys, supKeys) = (sorted(list(minKeys)), sorted(list(supKeys)))
        print(R)
        print("minKeys: {}".format(";".join(["(" + ",".join(sorted(list(s))) + ")" for s in minKeys])))
        print("supKeys: {}".format(";".join(["(" + ",".join(sorted(list(s))) + ")" for s in supKeys])))

    def test_proj(self):
        attrs = norm.parseAttrs('A,B,C,D,E,F,G')
        fds = norm.parseFds('A,C->D;A,C->E;B,F->E;A,F,G->B;B,D->C')
        R = norm.relation(attrs, fds)
        subAttrs = norm.parseAttrs('A,C,D,E')

        print(R)
        print("")
        print(R.getProjection(subAttrs))

    def test_multi1(self):
        print("test_multi1")
        attrs = norm.parseAttrs('A,B,C')
        fds = norm.parseFds('A->B;B->C')
        R = norm.relation(attrs, fds)

        (minKeys, supKeys) = R.getKeys()
        print(R)
        print("minKeys: {}".format(";".join(["(" + ",".join(sorted(list(s))) + ")" for s in minKeys])))
        print("supKeys: {}".format(";".join(["(" + ",".join(sorted(list(s))) + ")" for s in supKeys])))
        print("")
        
        R1 = R.getProjection(norm.parseAttrs('A,B'))
        R2 = R.getProjection(norm.parseAttrs('A,C'))
        
        print(R1)
        print("")
        print(R2)
        print("")

        isDependencyPreserving = norm.checkFdEq(R.fds, R1.fds + R2.fds)
        print("Is Dependency Preserving" if isDependencyPreserving else "Is NOT Dependency Preserving")




if __name__ == "__main__":
    # unittest.main()
    
    attrs = norm.parseAttrs("A,B,C,D")
    fds = norm.parseFds("A->B;B->C;C,D->A")
    R = norm.relation(attrs, fds)
    
    l = [R.getProjection(norm.parseAttrs(i)) for i in ["A,D", "A,C", "B,C,D"]]
    norm.isLosslessChaseTest(l, fds, verbose=True)



    exit()

    attrs = norm.parseAttrs("A,B,C,D,E,F,G")
    fds = norm.parseFds("A,C->D;A,C->E;B,F->E;A,F,G->B;B,D->C")
    R = norm.relation(attrs, fds)
    
    (minKeys, supKeys) = R.getKeys()
    print(R)
    print("minKeys: {}".format(";".join(["(" + ",".join(sorted(list(s))) + ")" for s in minKeys])))
    print("supKeys: {}".format(";".join(["(" + ",".join(sorted(list(s))) + ")" for s in supKeys])))
    print("")

    R1 = R.getProjection(norm.parseAttrs('A,B,C,E,G'))
    R2 = R.getProjection(norm.parseAttrs('A,B,C,D,F'))


    print(R1)
    print("")
    print(R2)
    print("")

    isDependencyPreserving = norm.checkFdEq(R.fds, R1.fds + R2.fds)
    print("Is Dependency Preserving" if isDependencyPreserving else "Is NOT Dependency Preserving")


    fds = norm.parseFds("A,C->B,F;B,C->B,E;A,B,C->F;F->A,B,C;B,C,E->G")
    ans = norm.parseFds("A,C->F;B,C->E;F->A;F->B;F->C;B,C->G")
    mbs = norm.getMinimalBasis(fds)
    print("MINIMAL BASIS: ")
    print(mbs)
    
    areEqual = norm.checkFdEq(mbs, ans)
    

    print("Correct Answer" if areEqual else "Incorrect Answer")
    
    mcv = norm.getMinimalCover(mbs)

    areEqual = norm.checkFdEq(mcv, ans)
    
    print("MINIMAL COVER: ")
    print(mcv)
    print("Correct Answer" if areEqual else "Incorrect Answer")

    
    attrs1 = norm.parseAttrs("city,state,street,zip")
    fds1 = norm.parseFds("city,state,street->zip;zip->city,state")
    
    Address = norm.relation(attrs1, fds1)

    (minKeys, _) = Address.getKeys()

    print("KEYS: ")
    print(minKeys)

    print("IS BCNF" if Address.isBCNF() else "IS NOT BCNF")
    print("IS 3NF" if Address.is3NF() else "IS NOT 3NF")
    
    attrs2 = norm.parseAttrs("A,B,C,D,E,F")
    fds2 = norm.parseFds("A,B->C;A,B->F;C->A;B,C->D")

    Rdecomp = norm.relation(attrs2, fds2)
    (minKeys, _) = Rdecomp.getKeys()
    
    print("KEYS: ")
    print(minKeys)


    print("IS BCNF" if Rdecomp.isBCNF() else "IS NOT BCNF")
    print("IS 3NF" if Rdecomp.is3NF() else "IS NOT 3NF")
    
    p1 = Rdecomp.getProjection(norm.parseAttrs("A,B,C,F"))
    print(p1)
    
    testFds = norm.parseFds("A,B->C,F;C->A")
    testFds2 = norm.parseFds("A,B->C,F;C->A;A->D")
    print("THEY ARE EQUAL" if norm.checkFdEq(p1.fds, testFds) else "THEY ARE NOT EQUAL")
    print("THEY ARE EQUAL" if norm.checkFdEq(p1.fds, testFds2) else "THEY ARE NOT EQUAL")

    print("3NF DECOMP")
    for dr in Rdecomp.decomp3NF():
        print(dr)
        print("IS 3NF" if dr.is3NF() else "IS NOT 3NF")
        print("")

    
    attrs3 = norm.parseAttrs("name,artist,genre,dateFounded,dateJoined")
    fds3 = norm.parseFds("name->genre,dateFounded;name,artist->dateJoined")
    MusicGroup = norm.relation(attrs3, fds3)
    
    (minKeys, _) = MusicGroup.getKeys()
    print("KEYS: ")
    print(minKeys)
    print("IS BCNF" if MusicGroup.isBCNF() else "IS NOT BCNF")
    print("IS 3NF" if MusicGroup.is3NF() else "IS NOT 3NF")
    
    print("BCNF DECOMP")
    for dr in MusicGroup.decompBCNF(verbose=True):
        print(dr)
        print("IS 3NF" if dr.is3NF() else "IS NOT 3NF")
        print("IS BCNF" if dr.isBCNF() else "IS NOT BCNF")
        print("")
    


    


























