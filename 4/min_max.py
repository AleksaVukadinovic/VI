import copy

def Min(state):
    if end(state):
        return evaluate(state), state
    
    current_best_value = float('inf')
    best_move = None
    for next_state in get_next_states(state):
        opponents_best_move, _ = Max(next_state)
        if opponents_best_move < current_best_value:
            best_move = next_state
            current_best_value = opponents_best_move

    return current_best_value, best_move

def Max(state):
    if end(state):
        return evaluate(state), state
    
    current_best_value = float('-inf')
    best_move = None
    for next_state in get_next_states(state):
        opponents_best_move, _ = Min(next_state)
        if opponents_best_move > current_best_value:
            best_move = next_state
            current_best_value = opponents_best_move

    return current_best_value, best_move

def get_next_states(state):
    result = []
    for i in range(0, 3):
        for j in range(0, 3):
            if state.board[i][j] == XOState.empty:
                next_state = copy.deepcopy(state)
                next_state.play_move([i, j])
                result.append(next_state)
    return result

def evaluate(state):
    result = 0
    if get_winner(state) == 'X':
        result = 1/state.move_count # 10 - state.move_count
    elif get_winner(state) == 'O':
        result -= 1/state.move_count # -(10 - state.move_count)
    return result

class XOState:
    empty = ' '
    def __init__(self):
        self.board = [
            [XOState.empty, XOState.empty, XOState.empty],
            [XOState.empty, XOState.empty, XOState.empty],
            [XOState.empty, XOState.empty, XOState.empty]
        ]
        self.current_player = 'X'
        self.move_count = 0
        self.last_move = None
        
    def play_move(self, move):
        i, j = move[0], move[1]
        self.board[i][j] = self.current_player
        self.current_player = 'X' if self.current_player == 'O' else 'O'
        self.move_count += 1
        self.last_move = [i, j]
    
    def draw_board(self):
        print(' | '.join(self.board[0]))
        print(' | '.join(self.board[1]))
        print(' | '.join(self.board[2]))
        print
        
def get_winner(game):
    board = game.board

    for i in range(0, 3):
        if board[0][i] != XOState.empty and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    for i in range(0, 3):
        if board[i][0] != XOState.empty and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]

    if board[0][0] != XOState.empty and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] != XOState.empty and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None

def end(game):
    winner = get_winner(game)
    return game.move_count == 9 or winner is not None    

def read_next_move():
    move = input()
    move = move.split(',')
    return [int(move[0]), int(move[1])]

game = XOState()
game.draw_board()

while True:
    next_move = read_next_move()
    game.play_move(next_move)
    game.draw_board()

    if get_winner(game) == 'X':
        print('Player X won')
        break

    if end(game):
        print('Tie')
        break
    
    evaluation, next_state = Min(game)
    game.play_move(next_state.last_move)
    game.draw_board()

    if get_winner(game) == '0':
        print('Player O won')
        break