import heapq
import operator


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


#
# class SimpleGraph:
#     def __init__(self):
#         self.edges = {}
#
#     def neighbors(self, id):
#         return self.edges[id]
#

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.obstacles

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]

        results.sort(key=operator.itemgetter(0, 1))

        # if (x + y) % 2 == 0: results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

#
# def neighbors(node, _map, d_units):
#     dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
#     result = []
#     for dir in dirs:
#         neighbor = [node[0] + dir[0], node[1] + dir[1]]
#         if 0 <= neighbor[0] < len(_map) and 0 <= neighbor[1] < len(_map[0]) and neighbor not in d_units:
#             result.append(neighbor)
#     return result

def create_graph_from_map(_map, d_units, unit):
    grid = GridWithWeights(len(_map[0]), len(_map))
    for i, x in enumerate(_map):
        for j, y in enumerate(x):
            if _map[i][j] == '#' or (i, j) in d_units:
                if (i, j) != (unit._x, unit._y): # ignores the unit itself
                    grid.obstacles.append((i, j))
    return grid
