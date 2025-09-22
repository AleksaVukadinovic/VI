from itertools import product
import os

class CNF:
    def __init__(self):
        self.clauses = []
        self.number_to_var_name = {}
        self.var_name_to_number = {}
    
    def add_clause(self, clause):
        for literal in clause:
            var_name = literal.strip('-')
            if var_name not in self.var_name_to_number:
                var_number = len(self.var_name_to_number) + 1
                self.var_name_to_number[var_name] = var_number
                self.number_to_var_name[var_number] = var_name
        self.clauses.append(clause)

    # BITAN DEO
    def dimacs(self):
        result = f'p cnf {len(self.var_name_to_number)} {len(self.clauses)}\n'
        for clause in self.clauses:
            for literal in clause:
                result = ''
                if literal[0] == '-':
                    result += '-'
                result += f'{self.var_name_to_number[literal.strip('-')]} '
            result += '0\n'
        return result
    
    def get_var_name(self, number: int):
        return self.vars[number]

    def get_var_number(self, name: str):
        return self.var_name_to_number[name]
    
def minisat_solve(problem_name, problem_dimacs, number_to_var):
    with open(f'{problem_name}.cnf', 'w') as handle:
        handle.write(problem_dimacs)
    os.system(f'minisat {problem_name}.cnf {problem_name}_result.cnf')

    with open(f'{problem_name}_result.cnf', 'r') as result_file:
        lines = result_file.readlines()

    if lines[0].startswith('SAT'):
        print('SAT')
        var_values = {}
        for var in lines[1].split(' ')[:-1]:
            var_number = int(var.strip('-'))
            var_name = number_to_var[var_number]
            var_values[var_name] = 0 if var.startswith('-') else 1
        true_vars = list(filter(lambda v: v[1] == 1, var_values.items()))
        true_vars.sort()
        for var in true_vars:
            print(var)
    else:
        print('UNSAT')
