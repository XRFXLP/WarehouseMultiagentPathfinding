from os import system
from time import sleep
from itertools import product
from copy import deepcopy
def print_maze(maze):
    for i in maze:
        for j in i:
            if j == '  ':
                print('  ', end=" ")
            else:
                print(j,    end=" ")
        print()
    print('\n')

def distance(a, b):
    y, x = a
    y1, x1 = b
    return ((y - y1) ** 2 + (x - x1) ** 2) ** 0.5

class Agent:
    '''
    self.state = 0  -> Have to pick up the stuff
    self.state = 1  -> Have to drop the stuff
    self.state = 2  -> Have to relax
    '''
    def __init__(self, name, location, pick_up, drop, end, state = 0, visited = set()):
        self.name = name
        self.location = location
        self.pick = pick_up
        self.drop = drop
        self.end = end
        self.state = state
        self.repo = {0: self.pick, 1: self.drop, 2: self.end}
        self.visited = set([location]) | visited

    def clone(self):
        return Agent(self.name, self.location, self.pick, self.drop, self.end, self.state, set(self.visited))

    def movable(self, what):
        if what[0] in ['#', 'R']:
            return False
        return True

    @property
    def done(self):
        return self.state == 3


    def get_dirs(self, maze):
        if   self.state == 0 and self.location == self.pick:
            self.state = 1
            self.visited = set([self.location])
        elif self.state == 1 and self.location == self.drop:
            self.state = 2
            self.visited = set([self.location])
        elif self.state == 2 and self.location == self.end:
            self.state = 3
            self.visited = set([self.location])

        if self.state == 3:
            return [(self.location)]
        H, W = len(maze), len(maze[0])

        to_go = self.repo[self.state]
        dirs = []
        for dy, dx in (1, 0), (0, -1), (-1, 0), (0, 1):
            y_, x_ = self.location[0] + dy, self.location[1] + dx
            if -1 < y_ < H and -1 < x_ < W and self.movable(maze[y_][x_]) and (y_, x_) not in self.visited:
                dirs.append((y_, x_))

        return sorted(dirs, key=lambda x: distance(x, self.repo[self.state]))

    def move(self, maze, location):
        y, x = self.location
        maze[y][x] = '  '
        self.location = location
        y, x = self.location
        maze[y][x] = 'R' + str(self.name)
        self.visited.add(self.location)


def arrange_data(table, blocks, height, width):
    maze = [[ '  ' for i in range(width)] for j in range(height)]
    for i, j in blocks:
        maze[i][j] = '##'

    for i, ((a1, a2), (b1, b2), (c1, c2), (d1, d2)) in enumerate(table):
        maze[a1][a2] = 'R' + str(i + 1)
        maze[b1][b2] = 'E' + str(i + 1)
        maze[c1][c2] = 'P' + str(i + 1)
        maze[d1][d2] = 'D' + str(i + 1)

    return maze


def main(table, height, width, blocks):
    AG = [Agent(i + 1, a, c, d, b) for i, (a, b, c, d) in enumerate(table)]
    maze = arrange_data(table, blocks, height, width)
    def recurse(agents, maze, move_made):
        print_maze(maze)
        sleep(0.1)
        system('clear')

        if all(i.done for i in agents):
            return move_made

        for moves in product(*[i.get_dirs(maze) for i in agents]):

            '''
            Cloning the data to avoid unintended residual mutation from branches of the parent
            This is an inefficient process, and in order to increase the efficiency
            it should be replaced with intelligent deletion of residual actions
            Like most of the solution of sudoku floating around the
            the internet
            '''

            dup_maze = deepcopy(maze)
            dup_agents = [ag.clone() for ag in agents]
            for agent, (y, x) in zip(dup_agents, moves):
                if not agent.done:
                    if not agent.movable(dup_maze[y][x]):
                        break
                    else:
                        agent.move(dup_maze, (y, x))
            else:
                A = recurse(dup_agents, dup_maze, move_made + [moves])
                if A:
                    return A
        return False

    return recurse(AG, maze, [])
table = [
    #  R        E       P       D
    [(4, 0), (4, 4), (4, 12), (4, 11)],
]

blocks = [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)]

main(table, 18, 18, blocks)
