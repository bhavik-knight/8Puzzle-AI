###############################################################################
# Name:             Bhavik Bhagat
# Email:            x2020coq@stfx.ca
# Student ID:       202002911
# Course:           csci495, homework3_q6, programming
# Command:          python3 puzzle8.py
###############################################################################


import sys
from time import time


def main():
    # initial state and goal is given
    grid_width = 3

    # assignment problem
    initial = (2, 8, 3, 1, 6, 4, 7, 9, 5)
    goal = (1, 2, 3, 8, 9, 4, 7, 6, 5)

    # check random config: not solvable
    # initial = (1, 2, 3, 4, 5, 6, 9, 8, 7)
    # goal = (1, 2, 3, 4, 5, 6, 7, 8, 9)

    # alternate 15-puzzle (solvable config)
    # ref: https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    # grid_width = 4
    # goal = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)

    # non-solvable
    # initial = (2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)

    # solvable
    # initial = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 14, 15)
    # initial = (3, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)

    # call to astar algorithm to get a winning node
    winning = a_star(initial, goal, grid_width)

    if winning is None:
        print(f"{initial} configuration is not solvable.")
        return -1

    # once we are here, means game is won or cannot find path
    path = list()

    # we have the winning node, now backtrack until we find None
    # if winning is None, we didn't find any solution
    while winning:
        path.append(winning.config)
        winning = winning.prev

    # print the required lists one per line
    for config in path[::-1]:
        Grid(config, goal, grid_width).draw()
        # print(*config)

    return len(path) - 1


def a_star(initial, goal, size):
    # keep track of the already visited config
    closed = set()

    # h_cost dict to make life easier, count heurisitics of initial config
    heuristic_cost = count_misplaced_tiles(initial, goal)

    # one config will only have one total misplaced tile counts
    h_cost = {initial: heuristic_cost}

    # fringe to keep track of all the config to be considered
    fringe = {Node(initial, heuristic_cost)}

    # bookkeeping
    winning_node = None

    # number of iterations
    num_iterations = 0

    # do this forever until some criteria matched
    while True:
        num_iterations += 1
        # print(f"fringe: {len(fringe)}, closed: {len(closed)}")
        # breaking condition #1 - fringe is empty, nothing to remove
        # search has failed, no optimum answer
        if len(fringe) == 0:
            break

        # remove the best config, put it on closed list (aka set)
        # set gives constant-time search, hence bette performance
        current = get_best_cost_config(fringe)
        fringe.remove(current)
        closed.add(current)

        # check if goal is reached
        # breaking condition #2 - goal configuration is achieved
        if current.config == goal:
            winning_node = current
            break

        # reachable configuration up, down, left, right
        grid_up = Grid(current.config, goal, size).move_up()
        grid_down = Grid(current.config, goal, size).move_down()
        grid_left = Grid(current.config, goal, size).move_left()
        grid_right = Grid(current.config, goal, size).move_right()

        # bookkeeping
        tile_type = (grid_up, grid_down, grid_left, grid_right)

        # different move gives different tiles
        # i.e. tile above, below, left, or right
        for tile in tile_type:
            # check if tile is in closed list, open list of illegal move (tile is None)
            # if so, move on to the next tile as we don't want to add this in the fringe
            if tile in map(lambda x: x.config, closed) or \
                tile in map(lambda x: x.config, fringe) or \
                tile is None:
                continue

            # check the cost to reach the child through current node
            # because we are just moving to the child node: it's 1 more than current node's g_cost
            tentative_g_cost = current.g + 1

            # heuristic cost
            heuristic_cost = h_cost.get(tile, 0) + count_misplaced_tiles(tile, goal)
            h_cost[tile] = heuristic_cost

            # create a node from the successor and linked to current node
            child = Node(tile, heuristic_cost, tentative_g_cost)
            child.prev = current
            child.f = child.g + child.h
            fringe.add(child)

    return winning_node


def get_best_cost_config(fringe):
    # if fringe is empty, no need to find anything
    # return nothing in that case
    if len(fringe) == 0:
        return None

    # bookkeeping
    best_node, min_cost = None, sys.maxsize

    # iterate over the fringe and fetch minimum cost config
    for node in fringe:
        if node.f < min_cost:
            min_cost = node.f
            best_node = node

    # return the min cost node
    return best_node


# to calculate the heuristic cost - number of misplaced tiles
def count_misplaced_tiles(current, goal):
    return sum(not(current[i] == goal[i]) for i in range(len(goal)))


# Grid class for puzzle
class Grid:
    # initialize with given config, goal is also given
    # constructor of the class
    def __init__(self, start, goal, size=3):
        self.start = start
        self.goal = goal
        self.size = size
        self.grid = dict()
        self.blank = tuple()
        self.move_dict = dict()

        # generate dictionary to store the  config
        # keys are tuple: indices of grid
        for i in range(self.size):
            for j in range(self.size):
                self.grid[(i, j)] = 0

        # call to generate grid
        self.blank = self.generate_grid(self.size)

        # move dictionary that tells what to do on move
        self.move_dict = {
            "up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)
        }

    # generic move function that moves blank tile to given tile
    def move(self, x, y):
        move_name = None
        for k, (vx, vy) in self.move_dict.items():
            if (vx, vy) == (x, y):
                move_name = k
                break

        # if no legal move, return None
        if not self.is_legal(move_name):
            return None

        # get blank tile new position
        old_blank_x, old_blank_y = self.blank
        self.blank = (old_blank_x + x, old_blank_y + y)

        # swap blank and actual tile position
        self.grid[(old_blank_x, old_blank_y)], self.grid[self.blank] =\
            self.grid[self.blank], self.grid[(old_blank_x, old_blank_y)]

        # return the configuration after the move
        return self.get_grid()

    # moves, up, down, left, right
    def move_up(self):
        return self.move(-1, 0)

    def move_down(self):
        return self.move(1, 0)

    def move_left(self):
        return self.move(0, -1)

    def move_right(self):
        return self.move(0, 1)

    # check if the move is legal
    def is_legal(self, move_name):
        x, y = self.move_dict[move_name]
        old_x, old_y = self.blank
        new_x, new_y = old_x + x, old_y + y
        return (0 <= new_x < self.size) and (0 <= new_y < self.size)

    # return the grid
    def get_grid(self):
        return tuple(self.grid.values())

    # to generate the grid from the given initial config
    def generate_grid(self, size):
        blank = None
        # iterate over the grid
        for row, col in self.grid:
            tile = self.start[row * size + col]

            # return the blank tile position
            if tile == (size**2):
                blank = (row, col)

            # attach tile to grid
            self.grid[(row, col)] = tile

        return blank

    # check if game is won
    def is_won(self):
        return self.get_grid() == self.goal

    # function to draw grid
    def draw(self):
        print("-" * 80)
        for i in range(self.size):
            for j in range(self.size):
                # size**2 (9) is blank, so print _ for that
                if self.grid[(i, j)] == self.size**2:
                    print(f"_\t", end="")
                    continue
                print(f"{self.grid[(i, j)]}\t", end="")
            print()
        print("-" * 80)
        return None

    # default function to print grid
    def __repr__(self):
        for v in self.grid.values():
            print(v, end=" ")
        # since this function must return something, returning empty string
        return ""


# class to save configuration as Node
class Node:
    # constructor
    def __init__(self, config, h, g = 0):
        self.config = config
        self.prev = None
        self.g = g
        self.h = h
        self.f = 0

    def __repr__(self):
        return f"{self.config}"

    # default function to print Node
    def __str__(self):
        return f"{self.config}: {self.f} = {self.g} + {self.h}"


if __name__ == "__main__":
    print("=" * 80)
    start = time()
    print(f"Length of the path: {main()}")
    print("=" * 80)
    print(f"time taken: {time() - start:^} s")
    print("=" * 80)
