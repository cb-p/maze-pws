import datetime
import pygame
import ui


class App:
    def __init__(self, generator, solver):
        self.running = True
        self.size = 640, 480

        self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption('Maze')

        self.frame_delta = datetime.timedelta(seconds=1/60)
        self.step_delta = datetime.timedelta(seconds=1/60)
        self.last_step_delta = datetime.timedelta()

        pygame.font.init()
        self.font = pygame.font.SysFont('Calibri', 18)

        self.maze = Maze(10, 30, 20, 20)
        self.maze_generator = generator(self.maze)
        self.maze_solver = solver(self.maze, (0, 0), (19, 19))

        self.solving_state = SolvingState.GENERATING

        self.instant_solve_button = ui.Button('Instant Generate', self.font, 10, self.maze.full_height() + 40, 150, 30)

        pygame.init()
    
    def update(self):
        self.last_step_delta += self.frame_delta

        if self.instant_solve_button.update():
            while not self.step_maze():
                pass

        while self.last_step_delta > self.step_delta:
            self.last_step_delta -= self.step_delta
            self.step_maze()

    def step_maze(self):
        if self.solving_state == SolvingState.GENERATING:
            self.maze_generator.step()

            if self.maze.finished:
                self.solving_state = SolvingState.SOLVING
                self.instant_solve_button.set_text("Instant Solve")
        elif self.solving_state == SolvingState.SOLVING:
            self.maze_solver.step()

            if self.maze.finished:
                self.solving_state = SolvingState.IDLE
                self.instant_solve_button.set_disabled(True)
        else:
            return True

        if self.maze.finished:
            self.maze.finished = False
            return True

        return False

    def draw(self):
        self.display_surface.fill((255, 255, 255))
        self.maze.draw(self.display_surface)

        delta_millis = self.frame_delta.days * 24.0 * 60.0 * 60.0 * 1000.0
        delta_millis += self.frame_delta.seconds * 1000.0
        delta_millis += self.frame_delta.microseconds / 1000.0
        title_text_surface = self.font.render('Maze - {} fps ({}ms)'.format(int(1000.0/delta_millis), int(delta_millis)), True, (0, 0, 0))
        self.display_surface.blit(title_text_surface, (10, 10))

        state_text = 'Idle'
        if self.solving_state == SolvingState.GENERATING:
            state_text = 'Generating'
        elif self.solving_state == SolvingState.SOLVING:
            state_text = 'Solving'

        state_text_surface = self.font.render(state_text, True, (0, 0, 0))
        state_text_width = state_text_surface.get_width()
        self.display_surface.blit(state_text_surface, (10 + self.maze.full_width() - state_text_width, 10))

        self.instant_solve_button.draw(self.display_surface)

    def start(self):
        last_frame_time = datetime.datetime.now()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.draw()

            now = datetime.datetime.now()
            self.frame_delta = now - last_frame_time
            last_frame_time = now

            pygame.display.update()

        pygame.quit()


class SolvingState:
    GENERATING = 0
    SOLVING = 1
    IDLE = 2


class Maze:
    def __init__(self, x, y, maze_width, maze_height):
        self.x = x
        self.y = y
        self.maze_width = maze_width
        self.maze_height = maze_height

        self.maze = [[MazeCell() for _ in range(0, self.maze_height)] for _ in range(0, self.maze_width)]
        self.highlighted = (-1, -1)

        self.tile_width = 12
        self.border_width = 2

        self.path = None

        self.finished = False

    def full_width(self):
        return self.maze_width * (self.tile_width + self.border_width) + self.border_width

    def full_height(self):
        return self.maze_height * (self.tile_width + self.border_width) + self.border_width
    
    def connect_cell(self, x, y, direction):
        if direction == Direction.NORTH:
            direction = Direction.opposite(direction)
            y -= 1
            
        if direction == Direction.WEST:
            direction = Direction.opposite(direction)
            x -= 1

        if x < 0 or y < 0 or x > self.maze_width - 1 or y > self.maze_height - 1:
            return

        if direction == Direction.SOUTH:
            self.maze[x][y].connected_south = True
            
        if direction == Direction.EAST:
            self.maze[x][y].connected_east = True
    
    def is_connected(self, x, y, direction):
        if direction == Direction.NORTH:
            direction = Direction.opposite(direction)
            y -= 1
            
        if direction == Direction.WEST:
            direction = Direction.opposite(direction)
            x -= 1

        if x < 0 or y < 0 or x > self.maze_width - 1 or y > self.maze_height - 1:
            return False

        if direction == Direction.SOUTH:
            return self.maze[x][y].connected_south
            
        if direction == Direction.EAST:
            return self.maze[x][y].connected_east
    
    def color(self, x, y, color):
        if x < 0 or y < 0 or x > self.maze_width - 1 or y > self.maze_height - 1:
            return
        
        self.maze[x][y].color = color

    def highlight(self, x, y):
        self.highlighted = (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(self.x, self.y, self.full_width(), self.full_height()))

        for x in range(0, self.maze_width):
            for y in range(0, self.maze_height):
                cell = self.maze[x][y]

                draw_x = self.x + x * (self.tile_width + self.border_width) + self.border_width
                draw_y = self.y + y * (self.tile_width + self.border_width) + self.border_width

                width_offset = self.border_width if cell.connected_east else 0
                color = (0, 255, 0) if x == self.highlighted[0] and y == self.highlighted[1] else cell.color
                pygame.draw.rect(surface, color, pygame.Rect(draw_x, draw_y, self.tile_width + width_offset, self.tile_width))

                if cell.connected_south:
                    pygame.draw.rect(surface, color, pygame.Rect(draw_x, draw_y + self.tile_width, self.tile_width, self.border_width))

        if self.path and len(self.path) > 1:
            for i in range(1, len(self.path)):
                previous_cell = self.path[i - 1]
                current_cell = self.path[i]

                previous_pos = (self.x + previous_cell[0] * (self.tile_width + self.border_width) + (self.border_width + self.tile_width) / 2,
                                self.y + previous_cell[1] * (self.tile_width + self.border_width) + (self.border_width + self.tile_width) / 2)

                current_pos = (self.x + current_cell[0] * (self.tile_width + self.border_width) + (self.border_width + self.tile_width) / 2,
                               self.y + current_cell[1] * (self.tile_width + self.border_width) + (self.border_width + self.tile_width) / 2)

                pygame.draw.line(surface, (255, 0, 0), previous_pos, current_pos, self.border_width)

    def finish(self, path=None):
        self.path = path
        self.finished = True

        for x in range(0, self.maze_width):
            for y in range(0, self.maze_height):
                cell = self.maze[x][y]
                cell.color = (255, 255, 255)


class MazeCell:
    def __init__(self):
        self.connected_east = False
        self.connected_south = False
        self.color = (200, 200, 200)


class Direction:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def opposite(direction):
        if direction == Direction.NORTH:
            return Direction.SOUTH
        elif direction == Direction.EAST:
            return Direction.WEST
        elif direction == Direction.SOUTH:
            return Direction.NORTH
        else:
            return Direction.EAST


class MazeGenerator:
    def __init__(self, maze):
        self.maze = maze

    def step(self):
        pass


class MazeSolver:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end

    def step(self):
        pass


if __name__ == "__main__":
    print("maze.py >> This file is meant to be used as a library, executing it will result in an useless simulation!")

    app = App(MazeGenerator, MazeSolver)
    app.start()
