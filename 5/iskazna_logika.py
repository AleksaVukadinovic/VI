import copy
from itertools import combinations

def all_valuations(variables):
    for r in range(len(variables) + 1):
        for true_variables in combinations(variables, r):
            result = {x: False for x in variables}
            result.update({x: True for x in true_variables})
            yield result

class Formula:
    def __init__(self):
        self.components = []

    def interpret(self, valuation):
        pass

    def __repr__(self):
        return str(self)

    def __eq__(self, rhs): 
        return Eq(self.copy(), rhs.copy())

    def __and__(self, rhs): 
        return And(self.copy(), rhs.copy())

    def __or__(self, rhs):
        return Or(self.copy(), rhs.copy())

    def __rshift__(self, rhs):
        return Impl(self.copy(), rhs.copy())

    def __invert__(self):
        return Not(self.copy())
    
    def copy(self):
        return copy.deepcopy(self)

    def get_all_variables(self):
        result = set()
        for c in self.components:
            result.update(c.get_all_variables())
        return result

    def is_valid(self):
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == False:
                return False, valuation
        return True, None

    def is_satisfiable(self):
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == True:
                return True, valuation
        return False, None

    def is_contradictory(self):
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == True:
                return False, valuation
        return True, None

    def is_falsifiable(self):
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == False:
                return True, valuation
        return False, None

    def all_valuations_that_interpret_to_true(self):
        result = []
        variables = list(self.get_all_variables())
        for valuation in all_valuations(variables):
            if self.interpret(valuation) == True:
                result.append(valuation)
        return result

    
class Var(Formula):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def interpret(self, valuation):
        return valuation[self.name]

    def get_all_variables(self):
        return set([self.name]) 

    def __str__(self):
        return self.name

class Const(Formula):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def interpret(self, valuation):
        return self.value

    def __str__(self):
        return "{}".format(1 if self.value else 0)

class And(Formula):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.components = [lhs, rhs]

    def interpret(self, valuation):
        return self.components[0].interpret(valuation) and self.components[1].interpret(valuation)

    def __str__(self):
        return f"({self.components[0]}) & ({self.components[1]})"


class Or(Formula):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.components = [lhs, rhs]

    def interpret(self, valuation):
        return self.components[0].interpret(valuation) or self.components[1].interpret(valuation)

    def __str__(self):
        return f"({self.components[0]}) | ({self.components[1]})"


class Impl(Formula):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.components = [lhs, rhs]

    def interpret(self, valuation):
        
        return not self.components[0].interpret(valuation) or self.components[1].interpret(valuation)

    def __str__(self):
        return f"({self.components[0]}) >> ({self.components[1]})"

class Eq(Formula):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.components = [lhs, rhs]
    
    def interpret(self, valuation):
        return self.components[0].interpret(valuation) == self.components[1].interpret(valuation)

    def __str__(self):
        return f"({self.components[0]}) == ({self.components[1]})"

class Not(Formula):
    def __init__(self, op):
        super().__init__()
        self.components = [op]

    def interpret(self, valuation):
        return not self.components[0].interpret(valuation)

    def __str__(self):
        return f"~({self.components[0]})"

def vars(names):
    return [Var(name.strip()) for name in names.split(',')]

def evaluate_formula(formula):
    print(formula)
    print("is_valid: ", formula.is_valid())
    print("is_satisfiable: ", formula.is_satisfiable())
    print("is_falsifiable: ", formula.is_falsifiable())
    print("is_contradictory: ", formula.is_contradictory())
    print("all true valuations: ")
    for val in all_valuations(formula.get_all_variables()):
        if formula.interpret(val):
            print(val)


if __name__ == "__main__":
    '''
    U igri mines dimenzija 2x3 dobijena je sledeca konfiguracija
    |1|A|C|
    |1|B|2|
    A,B,C su neotvorena polja, a brojevi oznacavaju broj mina u okolnim poljima.
    Zapisati u iskaznoj logici uslove koji moraju da vaze.
    '''

    A, B, C = vars("A,B,C")
    formula = (A | B) & ~(A & B) \
            & ~(~A & ~B & ~C) \
            & (A | B) \
            & (B | C) \
            & (A | C) \
            & ~(A & B & C)
    evaluate_formula(formula)


    '''
    Date su dve kutije A,B robot mora da stavi objekat u tacno jednu od njih.
    '''

    A, B = vars("A,B")
    formula = (A | B) & ~(A & B) & ~(~A & ~B)
    evaluate_formula(formula)

    ''' 
    |A|B|
    |C|D|
    Zapisati uslov da se u tabeli 2x2 sa poljima A,B,C,D moze postaviti tacno jedan zeton u 
    svakom redu
    '''

    A, B, C, D = vars("A,B,C,D")
    formula = (A | B) & ~(A & B) & ~(~A & ~B) \
            & (C | D) & ~(C & D) & ~(~C & ~D)
    evaluate_formula(formula)

    '''
    U iskaznoj logici zapisati uslov da bitovi 3-bitnog polja moraju biti jednaki
    '''
    A, B, C = vars("A,B,C")
    formula = (A == B) & (B == C)
    evaluate_formula(formula)

    '''
    Dva dvobitna broja se sabiraju i daju rezultat 3.
    1+2
    2+1
    3+0
    0+3
        A B
        C D
        ---
        1 1
    '''

    A, B, C, D = vars("A,B,C,D")
    formula = (B | D) & ~(B & D) & (A | C) & ~(A & C)

    '''
    U iskoznoj logici zapisati da je 4 bitna reprezentacija broja palindrom ali da 
    bitovi nisu jednaki
    ABCD
    '''

    A, B, C, D = vars("A,B,C,D")
    formula = (A == D) & (B == C) & ~((A==B) & (B==C) & (C==D))
    evaluate_formula(formula)

    '''
    Tri polja se boje crvenom ili plavom. 
    Ukoliko je prvo crveno, druga dva moraju biti iste boje.
    Ukoliko je drugo crveno, trece mora biti plavo.
    '''

    A, B, C = vars("A,B,C") # Crveno - False, Plavo - True
    formula = (~A >> (B == C)) | (~B >> C)
    evaluate_formula(formula)

    '''
     A
    / \\
    B - C
    Temana trougla A,B,C se boje sa dve boje, pri tome ni jedan par temena ne moze imati istu boju.
    '''

    A,B,C = vars("A,B,C")
    formula = ~(A == B) & ~(B == C) & ~(A == C)
    evaluate_formula(formula)


    '''
    |A|B|
    |C|D|
    Tabela 2x2 se boji crvenom ili plavom bojom.
    Ako je polje A ofarbano crvenom onda barem jedno od ostalih polja mora biti plavo.
    Ako je polje D ofarabno plavom onda barem dva ostala moraju biti crvena.
    Ne smeju sva polja biti ofarabana istom bojom.
    '''
    A,B,C,D = vars("A,B,C,D")
    formula = (A >> (~B | ~C | ~D)) & (~D >> ((A & B) | (B & C) | (A & C))) \
        & ~((A == B) & (B == C) & (C == D))
    evaluate_formula(formula)