import raylibpy

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE


def create_grid():
    return [[0.0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def update_grid(grid):
    new_grid = [[0.0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    ni, nj = (x + i) % GRID_WIDTH, (y + j) % GRID_HEIGHT
                    neighbors.append(grid[nj][ni])
            new_grid[y][x] = grid[y][x] * 0.5 + sum(neighbors) / (len(neighbors) * 2)
    return new_grid


def draw_slider(x, y, width, height, value, min_value, max_value):
    mouse_x = raylibpy.get_mouse_x()
    mouse_y = raylibpy.get_mouse_y()
    if raylibpy.is_mouse_button_down(raylibpy.MOUSE_LEFT_BUTTON):
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            value = (mouse_x - x) / width * (max_value - min_value) + min_value
    raylibpy.draw_rectangle(x, y, width, height, raylibpy.LIGHTGRAY)
    slider_x = int(x + (value - min_value) / (max_value - min_value) * width)
    raylibpy.draw_rectangle(slider_x - 5, y, 10, height, raylibpy.DARKGRAY)
    return value


def main():
    raylibpy.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Heat Flow Simulation")
    raylibpy.set_target_fps(60)

    grid = create_grid()
    paused = False
    speed = 0.5
    last_update_time = 0

    while not raylibpy.window_should_close():
        if raylibpy.is_key_pressed(raylibpy.KEY_SPACE):
            paused = not paused

        if raylibpy.is_mouse_button_pressed(raylibpy.MOUSE_LEFT_BUTTON):
            mouse_x = raylibpy.get_mouse_x()
            mouse_y = raylibpy.get_mouse_y()
            grid_x = mouse_x // CELL_SIZE
            grid_y = mouse_y // CELL_SIZE
            grid[grid_y][grid_x] = 1.0

        # Control simulation speed with slider
        speed = draw_slider(10, 50, 150, 20, speed, 0.1, 1.0)

        current_time = raylibpy.get_time()
        if not paused and current_time - last_update_time >= speed:
            grid = update_grid(grid)
            last_update_time = current_time

        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.RAYWHITE)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                heat_value = grid[y][x]
                color = raylibpy.Color(
                    int(heat_value * 255),
                    int(heat_value * 64),
                    int(heat_value * 64),
                    255,
                )
                raylibpy.draw_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, color
                )

        raylibpy.draw_text("Press SPACE to pause/resume", 10, 10, 20, raylibpy.GRAY)
        raylibpy.draw_text("Click to add heat", 10, 30, 20, raylibpy.GRAY)
        raylibpy.draw_text(f"Speed: {round(speed, 2)}", 170, 50, 20, raylibpy.GRAY)

        raylibpy.end_drawing()

    raylibpy.close_window()


if __name__ == "__main__":
    main()
