def Min(state, alpha = float('-inf'), beta = float('inf')):
    if end(state):
        return evaluate(state), state

    best_move = None
    best_move_value = float('inf')

    for neighbour_state in generate_states(state):
        opponenets_best_move_value, _ = Max(neighbour_state, alpha, beta)

        if opponenets_best_move_value < best_move_value:
            best_move_value = opponenets_best_move_value
            best_move = neighbour_state

        if best_move_value <= alpha:
            return best_move_value, best_move
        
        if best_move_value < beta:
            beta = best_move_value


    return best_move_value, best_move

def Max(state, alpha = float('-inf'), beta = float('inf')):
    if end(state):
        return evaluate(state), state
    
    best_move = None
    best_move_value = float('-inf')

    for neighbour_state in generate_states(state):
        opponents_best_move_value, _ = Min(neighbour_state, alpha, beta)

        if opponents_best_move_value > best_move_value:
            best_move_value = opponents_best_move_value
            best_move = neighbour_state

        if best_move_value >= beta:
            return best_move_value, best_move
        
        if best_move_value > alpha:
            alpha = best_move_value

    return best_move_value, best_move



def end(state):
    pass

def evaluate(state):
    pass

def generate_states(state):
    pass