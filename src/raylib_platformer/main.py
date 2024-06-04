import raylibpy


def main():
    raylibpy.init_window(800, 450, "raylib [core] example - basic window")

    raylibpy.set_target_fps(60)

    while not raylibpy.window_should_close():
        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.RAYWHITE)
        raylibpy.draw_text(
            "Congrats! You created your first window!", 190, 200, 20, raylibpy.LIGHTGRAY
        )
        raylibpy.end_drawing()

    raylibpy.close_window()


if __name__ == "__main__":
    main()
