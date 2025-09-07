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


def astar(adj_list, start_node, target_node, h):
    open_set = set([start_node])

    parent = {}
    parent[start_node] = None

    cheapest_path = {v:float('inf') for v in adj_list}
    cheapest_path[start_node] = 0

    heuristic_guess = {v:float('inf') for v in adj_list}
    heuristic_guess[start_node] = h(start_node)

    path_found = False

    while len(open_set) > 0:
        current_node = get_next_node(open_set, heuristic_guess)

        if current_node == target_node:
            path_found = True
            break

        open_set.remove(current_node)

        for (neighbour_node, weight) in adj_list[current_node]:
            new_cheapest_path = cheapest_path[current_node] + weight

            if new_cheapest_path < cheapest_path[neighbour_node]:
                parent[neighbour_node] = current_node
                cheapest_path[neighbour_node] = new_cheapest_path
                heuristic_guess[neighbour_node] = new_cheapest_path + h(neighbour_node)

                if neighbour_node not in open_set:
                    open_set.add(neighbour_node)

    path = []
    if path_found:
        while target_node is not None:
            path.append(target_node)
            target_node = parent[target_node]
        path.reverse()

    return path