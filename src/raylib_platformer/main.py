import raylibpy

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
PLAYER_RADIUS = 50
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 200
GRAVITY = 1.0
JUMP_FORCE = 20.0
FRICTION = 0.9  # Add this constant at the top of your file


# Player and platform definitions
class Player:
    def __init__(self, x, y):
        self.position = raylibpy.Vector2(x, y)
        self.velocity = raylibpy.Vector2(0, 0)
        self.on_ground = False


class Platform:
    def __init__(self, x, y):
        self.position = raylibpy.Vector2(x, y)


# Initialize game objects
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
platforms = [Platform(200, 400), Platform(400, 300), Platform(600, 200)]


def main():
    raylibpy.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "2D Platformer")
    raylibpy.set_target_fps(60)

    while not raylibpy.window_should_close():
        # Player movement
        if raylibpy.is_key_down(raylibpy.KEY_A):
            player.velocity.x = -5
        elif raylibpy.is_key_down(raylibpy.KEY_D):
            player.velocity.x = 5
        else:
            player.velocity.x *= FRICTION

        player.position.x += (
            player.velocity.x
        )  # Add this line to update the player's position

        # Player jump
        if raylibpy.is_key_pressed(raylibpy.KEY_SPACE) and player.on_ground:
            player.velocity.y = -JUMP_FORCE

        # Apply gravity
        player.velocity.y += GRAVITY
        player.position.y += player.velocity.y

        # Check for platform collision
        player.on_ground = False
        for platform in platforms:
            if (
                player.position.y + PLAYER_RADIUS > platform.position.y
                and player.position.y + PLAYER_RADIUS
                < platform.position.y + PLATFORM_HEIGHT
                and player.position.x + PLAYER_RADIUS > platform.position.x
                and player.position.x - PLAYER_RADIUS
                < platform.position.x + PLATFORM_WIDTH
            ):
                player.on_ground = True
                player.velocity.y = 0
                player.position.y = platform.position.y - PLAYER_RADIUS

        # Draw everything
        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.RAYWHITE)
        raylibpy.draw_circle_v(player.position, PLAYER_RADIUS, raylibpy.RED)
        for platform in platforms:
            # With this line
            raylibpy.draw_rectangle(
                platform.position.x,
                platform.position.y,
                PLATFORM_WIDTH,
                PLATFORM_HEIGHT,
                raylibpy.BLACK,
            )
        raylibpy.end_drawing()

    raylibpy.close_window()


if __name__ == "__main__":
    main()
