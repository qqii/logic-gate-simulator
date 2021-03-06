import sys
sys.path.append("..")

import unittest
import boolean


class ExpressionTestCase(unittest.TestCase):

    def test_creation(self):
        E = boolean.Expression
        expr_str = "(a+b+c)*d*(~e+(f*g))"
        expr = boolean.parse(expr_str)
        self.assertTrue(E(expr) is expr)
        self.assertTrue(E(expr_str) == expr)
        self.assertTrue(E(1) is boolean.TRUE)
        self.assertTrue(E(True) is boolean.TRUE)
        self.assertTrue(E(0) is boolean.FALSE)
        self.assertTrue(E(False) is boolean.FALSE)


class BaseElementTestCase(unittest.TestCase):

    def test_creation(self):
        BE = boolean.BaseElement
        self.assertTrue(BE(1) is boolean.TRUE)
        self.assertTrue(BE(True) is boolean.TRUE)
        self.assertTrue(BE(boolean.TRUE) is boolean.TRUE)
        self.assertTrue(BE(0) is boolean.FALSE)
        self.assertTrue(BE(False) is boolean.FALSE)
        self.assertTrue(BE(boolean.FALSE) is boolean.FALSE)
        self.assertRaises(TypeError, BE)
        self.assertRaises(TypeError, BE, 2)
        self.assertRaises(TypeError, BE, "a")
        self.assertTrue(boolean.TRUE.__class__() is boolean.TRUE)
        self.assertTrue(boolean.FALSE.__class__() is boolean.FALSE)

    def test_literals(self):
        self.assertTrue(boolean.TRUE.literals == set())
        self.assertTrue(boolean.FALSE.literals == set())

    def test_literalize(self):
        self.assertTrue(boolean.TRUE.literalize() is boolean.TRUE)
        self.assertTrue(boolean.FALSE.literalize() is boolean.FALSE)

    def test_eval(self):
        self.assertTrue(boolean.TRUE.eval() is boolean.TRUE)
        self.assertTrue(boolean.FALSE.eval() is boolean.FALSE)

    def test_dual(self):
        self.assertTrue(boolean.TRUE.dual == boolean.FALSE)
        self.assertTrue(boolean.FALSE.dual == boolean.TRUE)

    def test_equality(self):
        self.assertTrue(boolean.TRUE == boolean.TRUE)
        self.assertTrue(boolean.FALSE == boolean.FALSE)
        self.assertFalse(boolean.TRUE == boolean.FALSE)

    def test_order(self):
        self.assertTrue(boolean.FALSE < boolean.TRUE)
        self.assertTrue(boolean.TRUE > boolean.FALSE)

    def test_printing(self):
        self.assertTrue(str(boolean.TRUE) == "1")
        self.assertTrue(str(boolean.FALSE) == "0")
        self.assertTrue(repr(boolean.TRUE) == "TRUE")
        self.assertTrue(repr(boolean.FALSE) == "FALSE")


class SymbolTestCase(unittest.TestCase):

    def test_init(self):
        boolean.Symbol(1)
        boolean.Symbol("a")
        boolean.Symbol(None)
        boolean.Symbol(sum)
        boolean.Symbol((1, 2, 3))
        boolean.Symbol([1, 2])
        self.assertRaises(TypeError, boolean.Symbol, 1, 2)

    def test_isliteral(self):
        self.assertTrue(boolean.Symbol(1).isliteral is True)

    def test_literals(self):
        l1 = boolean.Symbol(1)
        l2 = boolean.Symbol(1)
        self.assertTrue(l1 in l1.literals)
        self.assertTrue(l1 in l2.literals)
        self.assertTrue(l2 in l1.literals)
        self.assertTrue(l2 in l2.literals)
        self.assertRaises(AttributeError, setattr, l1, "literals", 1)

    def test_literalize(self):
        s = boolean.Symbol(1)
        self.assertTrue(s.literalize() is s)

    def test_eval(self):
        s = boolean.Symbol(1)
        self.assertTrue(s.eval() is s)

    def test_equal(self):
        a = boolean.Symbol("a")
        b = boolean.Symbol("a")
        c = boolean.Symbol("b")
        d = boolean.Symbol()
        e = boolean.Symbol()
        # Test __eq__.
        self.assertTrue(a == a)
        self.assertTrue(a == b)
        self.assertFalse(a == c)
        self.assertFalse(b == c)
        self.assertTrue(d == d)
        self.assertFalse(d == e)
        self.assertFalse(a == d)
        # Test __ne__.
        self.assertFalse(a != a)
        self.assertFalse(a != b)
        self.assertTrue(a != c)
        self.assertTrue(b != c)

    def test_order(self):
        S = boolean.Symbol
        self.assertTrue(S("x") < S())
        self.assertTrue(S() > S("x"))
        self.assertTrue(S(1) < S(2))
        self.assertTrue(S(2) > S(1))
        s1, s2 = S(), S()
        self.assertTrue((s1 < s2) == (hash(s1) < hash(s2)))
        self.assertTrue((s1 > s2) == (hash(s1) > hash(s2)))

    def test_printing(self):
        self.assertTrue(str(boolean.Symbol("a")) == "a")
        self.assertTrue(str(boolean.Symbol(1)) == "1")
        self.assertTrue(repr(boolean.Symbol("a")), "Symbol('a')")
        self.assertTrue(repr(boolean.Symbol(1)) == "Symbol(1)")


class NOTTestCase(unittest.TestCase):

    def test_init(self):
        NOT = boolean.NOT
        self.assertRaises(TypeError, NOT)
        self.assertRaises(TypeError, NOT, "a", "b")
        NOT("a")
        self.assertTrue(
            NOT(1) == NOT(True) == NOT(boolean.TRUE) == boolean.FALSE)
        self.assertTrue(
            NOT(0) == NOT(False) == NOT(boolean.FALSE) == boolean.TRUE)

    def test_isliteral(self):
        s = boolean.Symbol(1)
        self.assertTrue(boolean.NOT(s).isliteral)
        self.assertFalse(boolean.parse("~(a+b)").isliteral)

    def test_literals(self):
        a = boolean.Symbol("a")
        l = ~a
        self.assertTrue(l.isliteral)
        self.assertTrue(l in l.literals)
        self.assertTrue(len(l.literals) == 1)
        l = boolean.parse("~(a*a)", eval=False)
        self.assertFalse(l.isliteral)
        self.assertTrue(a in l.literals)
        self.assertTrue(len(l.literals) == 1)

    def test_literalize(self):
        p = boolean.parse
        self.assertTrue(p("~a").literalize() == p("~a"))
        self.assertTrue(p("~(a*b)").literalize() == p("~a+~b"))
        self.assertTrue(p("~(a+b)").literalize() == p("~a*~b"))

    def test_eval(self):
        a = boolean.Symbol("a")
        self.assertTrue(~a == ~a)
        self.assertFalse(a == boolean.parse("~~a", eval=False))
        self.assertTrue(a == ~~a)
        self.assertTrue(~a, ~~~a)
        self.assertTrue(a, ~~~~a)
        self.assertTrue(~(a * a * a) == ~(a * a * a))

    def test_cancel(self):
        a = boolean.Symbol("a")
        parse = lambda x: boolean.parse(x, eval=False)
        self.assertTrue(~a == (~a).cancel())
        self.assertTrue(a == parse("~~a").cancel())
        self.assertTrue(~a == parse("~~~a").cancel())
        self.assertTrue(a == parse("~~~~a").cancel())

    def test_demorgan(self):
        a, b, c = boolean.symbols("a", "b", "c")
        parse = lambda x: boolean.parse(x, eval=False)
        self.assertTrue(parse("~(a*b)").demorgan() == ~a + ~b)
        self.assertTrue(parse("~(a+b+c)").demorgan()
                        == parse("~a*~b*~c"))
        self.assertTrue(parse("~(~a*b)").demorgan() == a + ~b)

    def test_order(self):
        x = boolean.Symbol(1)
        y = boolean.Symbol(2)
        self.assertTrue(x < ~x)
        self.assertTrue(~x > x)
        self.assertTrue(~x < y)
        self.assertTrue(y > ~x)

    def test_printing(self):
        a = boolean.Symbol("a")
        self.assertTrue(str(~a) == "a'")
        self.assertTrue(repr(~a) == "NOT(Symbol('a'))")
        expr = boolean.parse("~(a*a)", eval=False)
        self.assertTrue(str(expr) == "(a∙a)'")
        self.assertTrue(repr(expr) == "NOT(AND(Symbol('a'), Symbol('a')))")


class DualBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.a, self.b, self.c = boolean.symbols("a", "b", "c")
        self.t1 = boolean.DualBase(self.a, self.b, eval=False)
        self.t2 = boolean.DualBase(self.a, self.b, self.c, eval=False)
        self.t3 = boolean.DualBase(self.a, self.a, eval=False)
        self.t4 = boolean.DualBase("a", "b", "c", eval=False)

    def test_init(self):
        self.assertRaises(TypeError, boolean.DualBase)
        for term in (self.t1, self.t2, self.t3, self.t4):
            self.assertTrue(isinstance(term, boolean.DualBase))

    def test_isliteral(self):
        self.assertTrue(self.t1.isliteral is False)
        self.assertTrue(self.t2.isliteral is False)

    def test_literals(self):
        for term in (self.t1, self.t2, self.t3, self.t4):
            self.assertTrue(self.a in term.literals)
        for term in (self.t1, self.t2, self.t4):
            self.assertTrue(self.b in term.literals)
        for term in (self.t2, self.t4):
            self.assertTrue(self.c in term.literals)

    def test_literalize(self):
        p = boolean.parse
        self.assertTrue(p("a+~(b+c)").literalize() == p("a+(~b*~c)"))

    def test_annihilator(self):
        a = boolean.Symbol("a")
        p = lambda x: boolean.parse(x, eval=False)
        self.assertTrue(p("a*a").annihilator is boolean.FALSE)
        self.assertTrue(p("a+a").annihilator is boolean.TRUE)

    def test_identity(self):
        self.assertTrue(boolean.parse("a+b").identity is boolean.FALSE)
        self.assertTrue(boolean.parse("a*b").identity is boolean.TRUE)

    def test_dual(self):
        self.assertTrue(boolean.AND.getdual() is boolean.OR)
        self.assertTrue(boolean.OR.getdual() is boolean.AND)
        self.assertTrue(boolean.parse("a+b").dual is boolean.AND)
        self.assertTrue(boolean.parse("a*b").dual is boolean.OR)

    def test_eval(self):
        a = self.a
        b = self.b
        c = self.c
        _0 = boolean.FALSE
        _1 = boolean.TRUE
        # Idempotence
        self.assertTrue(a == a * a)
        # Idempotence + Associativity
        self.assertTrue(a + b == a + (a + b))
        # Annihilation
        self.assertTrue(_0 == (a * _0))
        self.assertTrue(_1 == (a + _1))
        # Identity
        self.assertTrue(a == (a * _1))
        self.assertTrue(a == (a + _0))
        # Complementation
        self.assertTrue(_0 == a * ~a)
        self.assertTrue(_1 == a + ~a)
        # Absorption
        self.assertTrue(a == a * (a + b))
        self.assertTrue(a == a + (a * b))
        self.assertTrue(b * a == (b * a) + (b * a * c))
        # Elimination
        self.assertTrue(a == (a * ~b) + (a * b))
        expr = boolean.parse("(~a*b*c) + (a*~b*c) + (a*b*~c) + (a*b*c)")
        result = boolean.parse("(a*b)+(b*c)+(a*c)")
        self.assertTrue(expr == result)
        expr = boolean.parse("(~a*b*~c*~d) + (a*~b*~c*~d) + (a*~b*c*~d) +"
                             "(a*~b*c*d) + (a*b*~c*~d) + (a*b*c*d)")
        result = boolean.parse("(~b*~d*a) + (~c*~d*b) + (a*c*d)")
        self.assertTrue(expr == result)
        expr = boolean.parse("(a*b*c*d) + (b*d)")
        result = boolean.parse("b*d")
        self.assertTrue(expr == result)
        expr = boolean.parse("(~a*~b*~c*~d) + (~a*~b*~c*d) + (~a*b*~c*~d) +"
                             "(~a*b*c*d) + (~a*b*~c*d) + (~a*b*c*~d) +"
                             "(a*~b*~c*d) + (~a*b*c*d) + (a*~b*c*d) + (a*b*c*d)")
        # TODO: Test the last expr in DualBaseTestCase.test_eval.

    def test_flatten(self):
        p = lambda x: boolean.parse(x, eval=False)
        a = self.a
        b = self.b
        c = self.c

        t1 = p("a * (b*c)")
        t2 = p("a*b*c")
        self.assertFalse(t1 == t2)
        self.assertTrue(t1.flatten() == t2)

        t1 = p("a + ((b*c) + (a*c)) + b")
        t2 = p("a + (b*c) + (a*c) + b")
        self.assertFalse(t1 == t2)
        self.assertTrue(t1.flatten() == t2)

    def test_distributive(self):
        a = self.a
        b = self.b
        c = self.c
        d = boolean.Symbol("d")
        e = boolean.Symbol("e")
        self.assertTrue((a * (b + c)).distributive() == (a * b) + (a * c))
        t1 = boolean.AND(a, (b + c), (d + e))
        t2 = boolean.OR(boolean.AND(a, b, d), boolean.AND(a, b, e),
                        boolean.AND(a, c, d), boolean.AND(a, c, e))
        self.assertTrue(t1.distributive() == t2)

    def test_equal(self):
        t1 = boolean.DualBase(self.b, self.a, eval=False)
        t2 = boolean.DualBase(self.b, self.c, self.a, eval=False)
        # Test __eq__.
        self.assertTrue(t1 == t1)
        self.assertTrue(self.t1 == t1)
        self.assertTrue(self.t2 == t2)
        self.assertFalse(t1 == t2)
        self.assertFalse(t1 == 1)
        self.assertFalse(t1 == True)
        self.assertFalse(t1 == None)
        # Test __ne__.
        self.assertFalse(t1 != t1)
        self.assertFalse(self.t1 != t1)
        self.assertFalse(self.t2 != t2)
        self.assertTrue(t1 != t2)
        self.assertTrue(t1 != 1)
        self.assertTrue(t1 != True)
        self.assertTrue(t1 != None)

    def test_order(self):
        x, y, z = boolean.symbols(1, 2, 3)
        self.assertTrue(boolean.AND(x, y) < boolean.AND(x, y, z))
        self.assertTrue(not boolean.AND(x, y) > boolean.AND(x, y, z))
        self.assertTrue(boolean.AND(x, y) < boolean.AND(x, z))
        self.assertTrue(not boolean.AND(x, y) > boolean.AND(x, z))
        self.assertTrue(boolean.AND(x, y) < boolean.AND(y, z))
        self.assertTrue(not boolean.AND(x, y) > boolean.AND(y, z))
        self.assertTrue(not boolean.AND(x, y) < boolean.AND(x, y))
        self.assertTrue(not boolean.AND(x, y) > boolean.AND(x, y))

    def test_printing(self):
        parse = lambda x: boolean.parse(x, eval=False)
        a = self.a
        b = self.b
        c = self.c
        self.assertTrue(str(parse("a*a")) == "a∙a")
        self.assertTrue(repr(parse("a*a")) == "AND(Symbol('a'), Symbol('a'))")
        self.assertTrue(str(parse("a+a")) == "a+a")
        self.assertTrue(repr(parse("a+a")) == "OR(Symbol('a'), Symbol('a'))")
        self.assertTrue(str(parse("(a+b)*c")) == "(a+b)∙c")
        self.assertTrue(repr(parse("(a+b)*c")) ==
                        "AND(OR(Symbol('a'), Symbol('b')), Symbol('c'))")


class OtherTestCase(unittest.TestCase):

    def test_class_order(self):
        order = ((boolean.TRUE, boolean.FALSE),
                 (boolean.Symbol(), boolean.Symbol("x")),
                 (boolean.parse("x*y"),),
                 (boolean.parse("x+y"),),
                 )
        for i, tests in enumerate(order):
            for case1 in tests:
                for j in range(i + 1, len(order)):
                    for case2 in order[j]:
                        self.assertTrue(case1 < case2)
                        self.assertTrue(case2 > case1)

    def test_parse(self):
        a, b, c = boolean.symbols("a", "b", "c")
        parse = boolean.parse
        self.assertTrue(parse("0") == parse("(0)") == boolean.FALSE)
        self.assertTrue(parse("1") == parse("(1)") == boolean.TRUE)
        self.assertTrue(parse("a") == parse("(a)") == a)
        self.assertTrue(parse("~a") == parse("~(a)") == parse("(~a)") == ~a)
        self.assertTrue(parse("~~a") == ~~a)
        self.assertTrue(parse("a*b") == a * b)
        self.assertTrue(parse("~a*b") == ~a * b)
        self.assertTrue(parse("a*~b") == a * ~b)
        self.assertTrue(parse("a*b*c") == parse("a*b*c", eval=False) ==
                        boolean.AND(a, b, c))
        self.assertTrue(parse("~a*~b*~c") == parse("~a*~b*~c", eval=False) ==
                        boolean.AND(~a, ~b, ~c))
        self.assertTrue(parse("a+b") == a + b)
        self.assertTrue(parse("~a+b") == ~a + b)
        self.assertTrue(parse("a+~b") == a + ~b)
        self.assertTrue(parse("a+b+c") == parse("a+b+c", eval=False) ==
                        boolean.OR(a, b, c))
        self.assertTrue(parse("~a+~b+~c") == boolean.OR(~a, ~b, ~c))
        self.assertTrue(parse("(a+b)") == a + b)
        self.assertTrue(parse("a*(a+b)") == a * (a + b))
        self.assertTrue(parse("a*(a+~b)") == a * (a + ~b))
        self.assertTrue(parse("(a*b)+(b*((c+a)*(b+(c*a))))") ==
                        parse("a*b + b*(c+a)*(b+c*a)") ==
                        (a * b) + (b * ((c + a) * (b + (c * a)))))

    def test_subs(self):
        a, b, c = boolean.symbols("a", "b", "c")
        expr = a * b + c
        self.assertEqual(expr.subs({a: b}), b + c)
        self.assertEqual(expr.subs({a: a}), expr)
        self.assertEqual(expr.subs({a: b + c}), boolean.parse("(b+c)*b+c"))
        self.assertEqual(expr.subs({a * b: a}), a + c)
        self.assertEqual(expr.subs({c: boolean.TRUE}), boolean.TRUE)

    def test_normalize(self):
        parse = boolean.parse
        expr = parse("((s+a)*(s+b)*(s+c)*(s+d)*(e+c+d))+(a*e*d)")
        result = boolean.AND(*boolean.normalize(boolean.AND, expr))
        sol = parse("(a+s)*(b+e+s)*(c+d+e)*(c+e+s)*(d+s)")
        self.assertTrue(result == sol)


class BooleanAlgebraTestCase(unittest.TestCase):

    def test_implementation(self):
        class Filter(boolean.BooleanAlgebra):

            def __init__(self, *, bool_expr=None):
                boolean.BooleanAlgebra.__init__(self, bool_expr=bool_expr,
                                                bool_base=Filter)

            def eval(self):
                subs_dict = {}
                for obj in self.bool_expr.objects:
                    subs_dict[obj.bool_expr] = obj.eval()
                return self.bool_expr.subs(subs_dict)

        class ConstFilter(Filter):

            def __init__(self, value):
                Filter.__init__(self)
                self.value = boolean.BaseElement(value)

            def eval(self):
                return self.value

        a = ConstFilter(True)
        b = ConstFilter(False)
        self.assertEqual(type(a + b), Filter)
        self.assertEqual((a + b).eval(), boolean.TRUE)
        self.assertEqual((a * b).eval(), boolean.FALSE)


class TruthTableTestCase(unittest.TestCase):

    def test_incorrect_data(self):
        args = [[],
                (),
                {},
                None,
                5,
                9.4]
        for a in args:
            self.assertRaises(TypeError, boolean.truth_table, a)

    def test_BaseElement(self):
        self.assertEqual([{boolean.TRUE: boolean.TRUE}],
                         boolean.truth_table(boolean.TRUE))
        self.assertEqual([{boolean.FALSE: boolean.FALSE}],
                         boolean.truth_table(boolean.FALSE))

    def test_correct_permutations(self):
        expr_list = (boolean.Symbol("A") + boolean.Symbol("B"),
                     boolean.Symbol("A"),
                     boolean.Symbol(None) * boolean.Symbol("B"),
                     ~boolean.Symbol("A") + boolean.Symbol("B"))

        for expr in expr_list:
            table = boolean.truth_table(expr)
            self.assertEqual(len(table), 2 ** len(expr.symbols))

            for i in range(1, len(table)):
                self.assertEqual(table[1].keys(), table[i].keys())
                self.assertNotEqual(table[0].values(), table[i].values())
                for v in table[0].values():
                    self.assertTrue(v in (boolean.TRUE, boolean.FALSE))

            for s in expr.symbols:
                self.assertTrue(s in table[0].keys())
            self.assertTrue(s in table[0].keys())

    def test_format_str(self):
        expr = boolean.Symbol("A")
        table = boolean.truth_table(expr, True)
        for row in table:
            for k, v in row.items():
                self.assertIsInstance(k, str)
                self.assertIsInstance(v, str)
                self.assertTrue(v in (str(boolean.TRUE), str(boolean.FALSE)))


class ParseTestCase(unittest.TestCase):

    def test_and(self):
        expr = boolean.Symbol("A") * boolean.Symbol("B")
        star = boolean.parse("A*B")
        dot = boolean.parse("A∙B")
        decimal = boolean.parse("A.B")
        hat = boolean.parse("A^B")
        l_and = boolean.parse("A∧B")

        self.assertEqual(expr, star)
        self.assertEqual(expr, dot)
        self.assertEqual(expr, decimal)
        self.assertEqual(expr, hat)
        self.assertEqual(expr, l_and)

    def test_or(self):
        expr = boolean.Symbol("A") + boolean.Symbol("B")
        plus = boolean.parse("A+B")
        l_or = boolean.parse("A∨B")

        self.assertEqual(expr, plus)
        self.assertEqual(expr, l_or)

    def test_not(self):
        expr = ~boolean.Symbol("A")
        prime = boolean.parse("A'")
        tilde = boolean.parse("~A")
        l_not = boolean.parse("¬A")
        p_not = boolean.parse("!A")

        self.assertEqual(expr, prime)
        self.assertEqual(expr, tilde)
        self.assertEqual(expr, l_not)
        self.assertEqual(expr, p_not)

    def test_incorrect(self):
        self.assertRaises(TypeError, boolean.parse, "A)")
        self.assertRaises(TypeError, boolean.parse, "-")
        self.assertRaises(TypeError, boolean.parse, None)

if __name__ == "__main__":
    unittest.main(verbosity=2)
