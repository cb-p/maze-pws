from maze import *
from generators.recursive_backtracking import *


class DepthFirstSolver(MazeSolver):
    def __init__(self, maze, start, end):
        super().__init__(maze, start, end)
        self.stack = [(0, 0)]
        self.backtracking = False
        self.previous_directions = []
        self.previous_direction = 99

    def step(self):
        current_pos = self.stack[len(self.stack) - 1]

        self.maze.color(current_pos[0], current_pos[1], (255, 0, 0))
        self.maze.highlight(current_pos[0], current_pos[1])

        if current_pos == self.end:
            self.maze.finish(self.stack)
            return

        all_directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        directions = []

        for direction in all_directions:
            if self.maze.is_connected(current_pos[0], current_pos[1], direction):
                directions.append(direction)

        if len(directions) != 0:
            for direction in directions:
                new_pos = current_pos
                if direction == Direction.NORTH:
                    new_pos = (new_pos[0], new_pos[1] - 1)
                elif direction == Direction.EAST:
                    new_pos = (new_pos[0] + 1, new_pos[1])
                elif direction == Direction.SOUTH:
                    new_pos = (new_pos[0], new_pos[1] + 1)
                elif direction == Direction.WEST:
                    new_pos = (new_pos[0] - 1, new_pos[1])

                if new_pos in self.stack:
                    continue

                if self.backtracking and direction <= self.previous_direction:
                    continue

                self.backtracking = False
                self.stack.append(new_pos)
                self.previous_directions.append(direction)
                return

        self.backtracking = True
        self.maze.color(current_pos[0], current_pos[1], (255, 255, 255))
        self.stack.pop()
        self.previous_direction = self.previous_directions.pop()


if __name__ == "__main__":
    app = App(RecursiveBacktrackingGenerator, DepthFirstSolver)
    app.start()
