from maze import *
from math import cos, pi


class MountainGenerator(MazeGenerator):
    def __init__(self, maze):
        super().__init__(maze)
        self.current_pos = [0, 0]

        self.top_steps = 20

    def step(self):
        if self.current_pos[0] < self.maze.maze_width - 1:
            self.maze.connect_cell(self.current_pos[0], self.current_pos[1], Direction.EAST)

        if self.current_pos[1] < self.maze.maze_height - 1:
            self.maze.connect_cell(self.current_pos[0], self.current_pos[1], Direction.SOUTH)

        steps_x = 1 - (-cos((float(self.current_pos[0]) / float(self.maze.maze_width)) * pi * 4) + 1) * 0.5
        steps_y = 1 - (-cos((float(self.current_pos[1]) / float(self.maze.maze_width)) * pi * 4) + 1) * 0.5
        self.maze.set_steps(self.current_pos[0], self.current_pos[1], int(steps_x * steps_y * (self.top_steps - 1) + 1))

        self.maze.color(self.current_pos[0], self.current_pos[1], (255, 255, 255))

        self.current_pos[0] += 1

        if self.current_pos[0] >= self.maze.maze_width:
            self.current_pos[0] = 0
            self.current_pos[1] += 1

        if self.current_pos[1] >= self.maze.maze_height:
            self.maze.finish()


if __name__ == "__main__":
    app = App(MountainGenerator, MazeSolver)
    app.start()
