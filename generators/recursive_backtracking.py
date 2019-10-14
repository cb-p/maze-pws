import random
from maze import *


class RecursiveBacktrackingGenerator(MazeGenerator):
    def __init__(self, maze):
        super().__init__(maze)
        self.stack = [(0, 0)]
        self.visited = [(0, 0)]

    def step(self):
        current_pos = self.stack[len(self.stack) - 1]

        self.maze.color(current_pos[0], current_pos[1], (255, 255, 255))
        self.maze.highlight(current_pos[0], current_pos[1])

        if len(self.visited) == self.maze.maze_width * self.maze.maze_height:
            self.maze.finish()
            return

        current_x, current_y = current_pos
        directions = []
        if current_pos[0] > 0 and (current_x - 1, current_y) not in self.visited:
            directions.append(Direction.WEST)
        if current_pos[0] < self.maze.maze_width - 1 and (current_x + 1, current_y) not in self.visited:
            directions.append(Direction.EAST)
        if current_pos[1] > 0 and (current_x, current_y - 1) not in self.visited:
            directions.append(Direction.NORTH)
        if current_pos[1] < self.maze.maze_height - 1 and (current_x, current_y + 1) not in self.visited:
            directions.append(Direction.SOUTH)

        if len(directions) == 0:
            self.stack.pop(len(self.stack) - 1)
            return

        direction = random.choice(directions)
        new_pos = current_pos
        if direction == Direction.NORTH:
            new_pos = (new_pos[0], new_pos[1] - 1)
        elif direction == Direction.EAST:
            new_pos = (new_pos[0] + 1, new_pos[1])
        elif direction == Direction.SOUTH:
            new_pos = (new_pos[0], new_pos[1] + 1)
        elif direction == Direction.WEST:
            new_pos = (new_pos[0] - 1, new_pos[1])

        self.stack.append(new_pos)
        self.visited.append(new_pos)

        self.maze.connect_cell(current_pos[0], current_pos[1], direction)


if __name__ == "__main__":
    app = App(RecursiveBacktrackingGenerator, MazeSolver)
    app.start()
