import normalization as norm
import unittest

class TestParsing(unittest.TestCase):

    def test_parseAttrs(self):
        
        tests = [
                    ("A,B,C", (set(["A","B","C"]), None))
                    , ("A ,B,C ", (set(["A","B","C"]), None))
                    , (",B,C ", (set(), "Invalid attributes"))
                    , ("", (set(), "Empty attribute set not allowed"))
                    , ("test_attribute, testAttribute, testAttr", (set(), "Invalid attributes"))
                    , ("A, B, C", (set(["A","B","C"]), None))
                    , ("  A  ,B,C,D, E", (set(["A","B","C","D","E"]), None))
                    , (",,,", (set(), "Invalid attributes"))
                ]

        for test in tests:
            self.assertTupleEqual(norm.parseAttrs(test[0]), test[1])

    def test_parseFds(self):
        

        tests = [
                    (
                        "A,B,C->D,E;B->F",
                        (
                            [
                                (set(["A","B","C"]), set(["D","E"])), 
                                (set(["B"]), set(["F"]))
                            ],
                            None
                        )
                    ), 
                    (
                        " A, B ->  C;  D, E   -> G",
                        (
                            [
                                (set(["A","B"]), set(["C"])),
                                (set(["D","E"]), set(["G"]))
                            ],
                            None
                        )
                    ),
                    (
                        "A,B; C->D ",
                        (
                            [],
                            "Invalid functional dependency input"
                        )
                    )
                ]

        for test in tests:
            _fd, err = norm.parseFds(test[0])
            _fd = [(i.lhs, i.rhs) for i in _fd]
            tkey = lambda x : ".".join(x[0]) + "|" + ".".join(x[1])
            self.assertTupleEqual((sorted(_fd, key=tkey), err), (sorted(test[1][0], key=tkey), test[1][1]))
        
    def test_closure(self):
        attrs, _ = norm.parseAttrs('A,B,C,D,E,F,G')

        fds, _ = norm.parseFds('A,C->D;A,C->E;B,F->E;A,F,G->B;B,D->C')
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
            self.assertEqual((norm.closure(norm.parseAttrs(t[0])[0], fds)), norm.parseAttrs(t[2])[0], "closure wrong ans")


if __name__ == "__main__":
    unittest.main()
