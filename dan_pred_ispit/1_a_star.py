import math
from typing import List
from collections import defaultdict

def euclid(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

class Edge:
    def __init__(self, start, end, weight: float):
        self.start = start
        self.end = end
        self.weight = weight

def iterate_edges(graph: List[List[Edge]], current):
    return graph[current]

def heuristic(current, target):
    return euclid(current, target)

def astar_book(graph: List[List[Edge]], start, end, h):
    open_set, closed_set = set([start]), set()

    cheapest_distance = defaultdict(lambda: float('inf'))
    cheapest_distance[start] = 0

    parent = {start: None}

    path_found = False

    def get_best():
        result, result_value = None, float('inf')
        for node in open_set:
            new_value = cheapest_distance[node] + h(node, end)
            
            if not result or new_value < result_value:
                result = node
                result_value = new_value

        return result

    while len(open_set) > 0:
        current = get_best()

        if current == end:
            path_found = True
            break

        for edge in iterate_edges(graph, current):
            neighbour = edge.end
            new_neighbour_distance = cheapest_distance[current] + edge.weight

            if neighbour not in open_set and neighbour not in closed_set:
                open_set.add(neighbour)
                parent[neighbour] = current
                cheapest_distance[neighbour] = new_neighbour_distance
            elif new_neighbour_distance < cheapest_distance[neighbour]:
                parent[neighbour] = current
                cheapest_distance[neighbour] = new_neighbour_distance

                if neighbour in closed_set:
                    closed_set.remove(neighbour)
                    open_set.remove(neighbour)
            
        open_set.remove(current)
        closed_set.add(current)


    if path_found:
        path = []
        while end is not None:
            path.append(end)
            end = parent[end]
        path.reverse()
        return path
    else:
        return None