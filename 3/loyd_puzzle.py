import copy
from collections import defaultdict

def get_next_node(open_set, heuristic_guess):
  next_node = None
  min_d = float('inf')
  for candidate in open_set:
      if candidate in heuristic_guess:
          guess = heuristic_guess[candidate]
          if guess < min_d:
              min_d = guess
              next_node = candidate

  return next_node

def h(state):
    state = deserialize(state)
    H = 0
    n = len(state)
    for i in range(n):
        for j in range(n):
            H += abs(state[i][j] % n -j) + abs(state[i][j] / n - i)
    
    return H


def astar(start_node, target_node, h):
  open_set = set([start_node])

  parents = {}
  parents[start_node] =  None

  cheapest_paths = defaultdict(lambda: float('inf'))
  cheapest_paths[start_node] = 0

  heuristic_guess = defaultdict(lambda: float('inf'))
  heuristic_guess[start_node] = h(start_node)

  path_found = False
  while len(open_set) > 0:
      current_node = get_next_node(open_set, heuristic_guess)

      if current_node == target_node:
          path_found = True
          break

      open_set.remove(current_node)
      for (neighbour_node, weight) in get_neighbours(current_node):
          new_cheapest_path =  cheapest_paths[current_node] + weight

          if new_cheapest_path < cheapest_paths[neighbour_node]:
              parents[neighbour_node] = current_node
              cheapest_paths[neighbour_node] = new_cheapest_path
              heuristic_guess[neighbour_node] = new_cheapest_path + h(neighbour_node)
              
              if neighbour_node not in open_set:
                open_set.add(neighbour_node)
  
  path = []
  if path_found:
      while target_node is not None:
          path.append(target_node)
          target_node = parents[target_node]
      path.reverse()

  return path

def serialize(matrix):
    result = []
    for row in matrix:
        for col in row:
            result.append(str(col))
    return ':'.join(result)
  
def deserialize(state):
   splited =  state.split(':')
   splited = [int(x) for x in splited]
   return [splited[:3], splited[3:6], splited[6:]]

def get_neighbours(state):
    matrix = deserialize(state)
    blank_i, blank_j = -1, -1

    n = len(matrix)
    for i in range(n):
      for j in range(n):
         if matrix[i][j] == 0:
            blank_i, blank_j = i, j
            break
    
    neighbours = []
    if blank_i > 0:
        new_matrix = copy.deepcopy(matrix)
        new_matrix[blank_i][blank_j] = new_matrix[blank_i - 1][blank_j]
        new_matrix[blank_i - 1][blank_j] = 0
        neighbours.append(serialize(new_matrix))

    if blank_i < (n-1):
        new_matrix = copy.deepcopy(matrix)
        new_matrix[blank_i][blank_j] = new_matrix[blank_i + 1][blank_j]
        new_matrix[blank_i + 1][blank_j] = 0
        neighbours.append(serialize(new_matrix))

    if blank_j > 0:
        new_matrix = copy.deepcopy(matrix)
        new_matrix[blank_i][blank_j] = new_matrix[blank_i][blank_j -1]
        new_matrix[blank_i][blank_j - 1] = 0
        neighbours.append(serialize(new_matrix))

    if blank_j < (n-1):
        new_matrix = copy.deepcopy(matrix)
        new_matrix[blank_i][blank_j] = new_matrix[blank_i][blank_j+1]
        new_matrix[blank_i][blank_j + 1] = 0
        neighbours.append(serialize(new_matrix))

    return zip(neighbours, [1 for _ in range(len(neighbours))])

if __name__ == '__main__':
  start = [
    [4, 1, 3],
     [0, 2, 5],
     [7, 8, 6]
  ]
  target = [
     [1, 2, 3],
     [4, 5, 6],
     [7, 8, 0]
  ]

  serialized = serialize(start)
  deserialized = deserialize(serialized)
  path = astar(serialize(start), serialize(target), h)
  print(path)