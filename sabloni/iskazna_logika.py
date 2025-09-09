from itertools import combinations

def all_valuations(variables):
    for r in range(len(variables) + 1):
        for true_variables in combinations(variables, r):
            valuation = {x:False for x in variables}
            valuation.update({x: True for x in true_variables})
            yield valuation
            

class Formula:
    def __init__(self):
        pass

    def interpret(self, valuation):
        pass

    def __eq__(self, value):
        return Eq(self, value)
    
    def __and__(self, value):
        return And(self, value)
    
    def __or__(self, value):
        return Or(self, value)
    
    def __invert__(self):
        return Not(self)
    
    def __rshift__(self, value):
        return Impl(self, value)
    
    def get_all_variables(self):
        variables = set()
        for variable in self.components:
            variables.update(variable.get_all_variables())
        return variables
    
    def is_valid(self):
        for valuation in all_valuations(self.get_all_variables()):
            if self.interpret(valuation) == False:
                return False, valuation
        return True, None
    
    def is_satisfiable(self):
        valuations = all_valuations(self.get_all_variables())
        for valuation in valuations:
            if self.interpret(valuation):
                return True, valuation
        return False, None

    def is_falsifiable(self):
        valuations = all_valuations(self.get_all_variables())
        for valuation in valuations:
            if self.interpret(valuation) == False:
                return True, valuation
        return False, None
    
    def is_contradiction(self):
        valuations = all_valuations(self.get_all_variables())
        for valuation in valuations:
            if self.interpret(valuation):
                return False, valuation
        return True, None

class Const(Formula):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def interpret(self, valuation):
        return self.value
    
    def __str__(self):
        return "1" if self.value else "0"
    
    def get_all_variables(self):
        return set()

class Var(Formula):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def interpret(self, valuation):
        return valuation[self.name]
    
    def __str__(self):
        return self.name
    
    def get_all_variables(self):
        return set([self.name])

class And(Formula):
    def __init__(self, left, right):
        super().__init__()
        self.components = [left, right]
    
    def interpret(self, valuation):
        return self.components[0].interpret(valuation) and self.components[1].interpret(valuation)
    
    def __str__(self):
        return f"({self.components[0]} & {self.components[1]})"
    
class Or(Formula):
    def __init__(self, left, right):
        super().__init__()
        self.components = [left, right]
    
    def interpret(self, valuation):
        return self.components[0].interpret(valuation) or self.components[1].interpret(valuation)
    
    def __str__(self):
        return f"({self.components[0]} | {self.components[1]})"
    
class Eq(Formula):
    def __init__(self, left, right):
        super().__init__()
        self.components = [left, right]
    
    def interpret(self, valuation):
        return self.components[0].interpret(valuation) == self.components[1].interpret(valuation)
    
    def __str__(self):
        return f"({self.components[0]} == {self.components[1]})"
    

class Impl(Formula):
    def __init__(self, left, right):
        super().__init__()
        self.components = [left, right]
    
    def interpret(self, valuation):
        return not self.components[0].interpret(valuation) or self.components[1].interpret(valuation)
    
    def __str__(self):
        return f"({self.components[0]} >> {self.components[1]})"
    
class Not(Formula):
    def __init__(self, op):
        super().__init__()
        self.components = [op]

    def interpret(self, valuation):
        return not self.components[0].interpret(valuation)
    
    def __str__(self):
        return f"~({self.components[0]})"

if __name__ == "__main__":
    A, B, C, D = Var("A"), Var("B"), Var("C"), Var("D")
    formula = (A == B) & (B == C) & ~(A == B & B == C & C == D)
    print(formula)
    print(formula.get_all_variables())
    valuation = {
        "A" : True,
        "B" : False,
        "C" : True,
        "D" : True,
    }

    print("Is valid:", formula.is_valid())
    print("Is satisfiable:", formula.is_satisfiable())
    print("Is falsifiable:", formula.is_falsifiable())
    print("Is contradiction:", formula.is_contradiction())
    
    for valuation in all_valuations(formula.get_all_variables()):
        if formula.interpret(valuation):
            print(valuation)

