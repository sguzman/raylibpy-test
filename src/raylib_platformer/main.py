import raylibpy
import math

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
PENDULUM_RADIUS = 20
GRAVITY = 0.98


# Pendulum properties
class DoublePendulum:
    def __init__(
        self, origin_x, origin_y, length1, length2, mass1, mass2, angle1, angle2
    ):
        self.origin = raylibpy.Vector2(origin_x, origin_y)
        self.length1 = length1
        self.length2 = length2
        self.mass1 = mass1
        self.mass2 = mass2
        self.angle1 = angle1
        self.angle2 = angle2
        self.angular_velocity1 = 0.0
        self.angular_velocity2 = 0.0
        self.position1 = raylibpy.Vector2(
            origin_x + length1 * math.sin(angle1), origin_y + length1 * math.cos(angle1)
        )
        self.position2 = raylibpy.Vector2(
            self.position1.x + length2 * math.sin(angle2),
            self.position1.y + length2 * math.cos(angle2),
        )

    def update(self):
        # Equations of motion for double pendulum
        num1 = -GRAVITY * (2 * self.mass1 + self.mass2) * math.sin(self.angle1)
        num2 = -self.mass2 * GRAVITY * math.sin(self.angle1 - 2 * self.angle2)
        num3 = -2 * math.sin(self.angle1 - self.angle2) * self.mass2
        num4 = (
            self.angular_velocity2** 2 * self.length2
            + self.angular_velocity1** 2
            * self.length1
            * math.cos(self.angle1 - self.angle2)
        )
        den = self.length1 * (
            2 * self.mass1
            + self.mass2
            - self.mass2 * math.cos(2 * self.angle1 - 2 * self.angle2)
        )
        self.angular_acceleration1 = (num1 + num2 + num3 * num4) / den

        num1 = 2 * math.sin(self.angle1 - self.angle2)
        num2 = self.angular_velocity1**2 * self.length1 * (self.mass1 + self.mass2)
        num3 = GRAVITY * (self.mass1 + self.mass2) * math.cos(self.angle1)
        num4 = (
            self.angular_velocity2**2
            * self.length2
            * self.mass2
            * math.cos(self.angle1 - self.angle2)
        )
        den = self.length2 * (
            2 * self.mass1
            + self.mass2
            - self.mass2 * math.cos(2 * self.angle1 - 2 * self.angle2)
        )
        self.angular_acceleration2 = (num1 * (num2 + num3 + num4)) / den

        self.angular_velocity1 += self.angular_acceleration1
        self.angular_velocity2 += self.angular_acceleration2
        self.angle1 += self.angular_velocity1
        self.angle2 += self.angular_velocity2

        self.position1.x = self.origin.x + self.length1 * math.sin(self.angle1)
        self.position1.y = self.origin.y + self.length1 * math.cos(self.angle1)
        self.position2.x = self.position1.x + self.length2 * math.sin(self.angle2)
        self.position2.y = self.position1.y + self.length2 * math.cos(self.angle2)


def main():
    raylibpy.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Double Pendulum Simulation")
    raylibpy.set_target_fps(60)

    # Create a double pendulum
    double_pendulum = DoublePendulum(
        SCREEN_WIDTH / 2, 100, 200, 200, 10, 10, math.pi / 2, math.pi / 2
    )

    while not raylibpy.window_should_close():
        # Update double pendulum
        double_pendulum.update()

        # Draw everything
        raylibpy.begin_drawing()
        raylibpy.clear_background(raylibpy.RAYWHITE)

        # Draw double pendulum
        raylibpy.draw_line_v(
            double_pendulum.origin, double_pendulum.position1, raylibpy.BLACK
        )
        raylibpy.draw_circle_v(double_pendulum.position1, PENDULUM_RADIUS, raylibpy.RED)
        raylibpy.draw_line_v(
            double_pendulum.position1, double_pendulum.position2, raylibpy.BLACK
        )
        raylibpy.draw_circle_v(double_pendulum.position2, PENDULUM_RADIUS, raylibpy.RED)

        raylibpy.end_drawing()

    raylibpy.close_window()


if __name__ == "__main__":
    main()
