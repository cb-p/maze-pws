from maze import *
from generators.recursive_backtracking import *


class BreadthFirstSolver(MazeSolver):

    def __init__(self, maze, start, end):
        super().__init__(maze, start, end)
        self.queue = []
        self.visited = []
        self.queue.append(self.start)
        self.end = end
        self.old_pos = [[0] * maze.maze_height for _ in range(maze.maze_width)]
        self.path = [self.end]

    def step(self):
        if len(self.queue) != 0:
            current = self.queue[0]

            self.maze.color(current[0], current[1], (255, 0, 0))
            self.maze.highlight(current[0], current[1])
            if current == self.end:
                self.generate_path()

                return

            current = self.queue.pop(0)

            self.visited.append(current)
            all_directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
            directions = []

            for direction in all_directions:
                if self.maze.is_connected(current[0], current[1], direction):
                    directions.append(direction)

            if len(directions) != 0:
                for direction in directions:
                    new_pos = None
                    if direction == Direction.NORTH:
                        if not (current[0], current[1] - 1) in self.visited:
                            new_pos = (current[0], current[1] - 1)
                    if direction == Direction.EAST:
                        if not (current[0] + 1, current[1]) in self.visited:
                            new_pos = (current[0] + 1, current[1])
                    if direction == Direction.SOUTH:
                        if not (current[0], current[1] + 1) in self.visited:
                            new_pos = (current[0], current[1] + 1)
                    if direction == Direction.WEST:
                        if not (current[0] - 1, current[1]) in self.visited:
                            new_pos = (current[0] - 1, current[1])

                    if new_pos:
                        self.old_pos[new_pos[0]][new_pos[1]] = current
                        self.queue.append(new_pos)

    def generate_path(self):
        current = self.path[len(self.path) - 1]

        self.maze.highlight(current[0], current[1])
        self.maze.color(current[0], current[1], (0, 0, 255))

        self.path.append(self.old_pos[current[0]][current[1]])

        if self.path[-1] == self.start:
            self.path.reverse()
            self.maze.finish(self.path)


if __name__ == "__main__":
    app = App(RecursiveBacktrackingGenerator, BreadthFirstSolver)
    app.start()
