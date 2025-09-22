from itertools import combinations

# Jedino bitno da se zapamti
def all_valuations(variables):
    valuations = []
    for r in range(len(variables) + 1):
        for true_variables in combinations(variables, r):
            result = {x: False for x in variables}
            result.update({x: True for x in true_variables})
            valuations.append(result)
    return valuations