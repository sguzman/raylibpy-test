import raylibpy
import random
import math

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
MIN_BALL_RADIUS = 5
MAX_BALL_RADIUS = 10
NUM_BALLS = 100
GRAVITY = 0.1
CONTAINER_RADIUS = SCREEN_WIDTH // 2 - 50


class Ball:
    def __init__(self, x, y, radius):
        self.position = raylibpy.Vector2(x, y)
        self.velocity = raylibpy.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.radius = radius
        self.color = raylibpy.Color(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255
        )


def distance(v1, v2):
    return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2)


def normalize(v):
    length = math.sqrt(v.x**2 + v.y**2)
    if length == 0:
        return raylibpy.Vector2(0, 0)
    return raylibpy.Vector2(v.x / length, v.y / length)


def dot_product(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


def spawn_ball(balls):
    x = random.uniform(MAX_BALL_RADIUS, SCREEN_WIDTH - MAX_BALL_RADIUS)
    y = random.uniform(MAX_BALL_RADIUS, SCREEN_HEIGHT - MAX_BALL_RADIUS)
    radius = random.uniform(MIN_BALL_RADIUS, MAX_BALL_RADIUS)
    balls.append(Ball(x, y, radius))


def update_ball(ball):
    ball.velocity.y += GRAVITY
    ball.position.x += ball.velocity.x
    ball.position.y += ball.velocity.y

    # Check collision with container
    dist_to_center = distance(
        ball.position, raylibpy.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    )
    if dist_to_center + ball.radius > CONTAINER_RADIUS:
        normal = raylibpy.Vector2(
            ball.position.x - SCREEN_WIDTH / 2, ball.position.y - SCREEN_HEIGHT / 2
        )
        normal = normalize(normal)
        velocity_dot_normal = dot_product(ball.velocity, normal)
        ball.velocity = ball.velocity - 2 * velocity_dot_normal * normal
        overlap = dist_to_center + ball.radius - CONTAINER_RADIUS
        ball.position -= normal * overlap


def handle_ball_collisions(balls):
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1 = balls[i]
            ball2 = balls[j]
            dist = distance(ball1.position, ball2.position)
            if dist < ball1.radius + ball2.radius:
                normal = normalize(
                    raylibpy.Vector2(
                        ball2.position.x - ball1.position.x,
                        ball2.position.y - ball1.position.y,
                    )
                )
                velocity_dot_normal1 = dot_product(ball1.velocity, normal)
                velocity_dot_normal2 = dot_product(ball2.velocity, normal)
                ball1.velocity = (
                    ball1.velocity
                    - normal * velocity_dot_normal1
                    + normal * velocity_dot_normal2
                )
                ball2.velocity = (
                    ball2.velocity
                    - normal * velocity_dot_normal2
                    + normal * velocity_dot_normal1
                )

                # Separate the balls to prevent them from sticking together
                overlap = ball1.radius + ball2.radius - dist
                ball1.position -= normal * (overlap / 2)
                ball2.position += normal * (overlap / 2)


def main():
    raylibpy.init_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "2D Particle Simulation with Gravity"
    )
    raylibpy.set_target_fps(60)

    balls = [
        Ball(
            random.uniform(MAX_BALL_RADIUS, SCREEN_WIDTH - MAX_BALL_RADIUS),
            random.uniform(MAX_BALL_RADIUS, SCREEN_HEIGHT - MAX_BALL_RADIUS),
            random.uniform(MIN_BALL_RADIUS, MAX_BALL_RADIUS),
        )
        for _ in range(NUM_BALLS)
    ]

    while not raylibpy.window_should_close():
        if raylibpy.is_mouse_button_pressed(raylibpy.MOUSE_LEFT_BUTTON):
            mouse_x = raylibpy.get_mouse_x()
            mouse_y = raylibpy.get_mouse_y()
            radius = random.uniform(MIN_BALL_RADIUS, MAX_BALL_RADIUS)
            balls.append(Ball(mouse_x, mouse_y, radius))

        for ball in balls:
            update_ball(ball)

        handle_ball_collisions(balls)

        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.RAYWHITE)

        # Draw container
        raylibpy.draw_circle(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, CONTAINER_RADIUS, raylibpy.LIGHTGRAY
        )

        for ball in balls:
            raylibpy.draw_circle_v(ball.position, ball.radius, ball.color)

        raylibpy.end_drawing()

    raylibpy.close_window()


if __name__ == "__main__":
    main()
