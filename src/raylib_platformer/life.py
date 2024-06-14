import raylibpy
import random

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE


def create_grid():
    return [
        [random.randint(0, 1) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)
    ]


def count_neighbors(grid, x, y):
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            ni, nj = (x + i) % GRID_WIDTH, (y + j) % GRID_HEIGHT
            neighbors += grid[nj][ni]
    return neighbors


def update_grid(grid):
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = count_neighbors(grid, x, y)
            if grid[y][x] == 1 and (neighbors == 2 or neighbors == 3):
                new_grid[y][x] = 1
            elif grid[y][x] == 0 and neighbors == 3:
                new_grid[y][x] = 1
            else:
                new_grid[y][x] = 0
    return new_grid


def main():
    raylibpy.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Game of Life")
    raylibpy.set_target_fps(10)

    grid = create_grid()
    paused = False

    while not raylibpy.window_should_close():
        if raylibpy.is_key_pressed(raylibpy.KEY_SPACE):
            paused = not paused

        if not paused:
            grid = update_grid(grid)

        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.RAYWHITE)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x] == 1:
                    raylibpy.draw_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                        raylibpy.BLACK,
                    )
                else:
                    raylibpy.draw_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                        raylibpy.RAYWHITE,
                    )

        raylibpy.draw_text("Press SPACE to pause/resume", 10, 10, 20, raylibpy.GRAY)

        raylibpy.end_drawing()

    raylibpy.close_window()


if __name__ == "__main__":
    main()
