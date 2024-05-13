import math
from settings import BORDER_WIDTH, BORDER_HEIGHT, BOUNCE, MAX_HEALTH

class Sprite:
    @staticmethod
    def is_on_screen(sprite, screen_width, screen_height, x_offset, y_offset):
        if (
            sprite.x - x_offset < screen_width / 2
            and sprite.x - x_offset > -screen_width / 2
            and sprite.y - y_offset < screen_height / 2
            and sprite.y - y_offset > -screen_height / 2
        ):
            return True
        else:
            return False

    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx = 0.0
        self.dy = 0.0
        self.heading = 0
        self.da = 0.0
        self.thrust = 0
        self.bounce = BOUNCE
        self.width = 20
        self.height = 20
        self.state = "active"
        self.max_health = MAX_HEALTH
        self.health = self.max_health

    def is_collision(self, other):
        if self.x < other.x + other.width and self.x + self.width > other.x and self.y < other.y + other.height and self.y + self.height > other.y:
            return True
        else:
            return False

    def collide(self, other):
        temp_dx = self.dx
        temp_dy = self.dy

        self.dx = other.dx
        self.dy = other.dy

        other.dx = temp_dx
        other.dy = temp_dy

        self.health -= 10
        other.health -= 10

    def border_chk(self):
        if self.x >= BORDER_WIDTH - 20:
            self.dx *= -self.bounce
        elif self.x <= -BORDER_WIDTH + 20:
            self.dx *= -self.bounce
        elif self.y >= BORDER_HEIGHT - 20:
            self.dy *= -self.bounce
        elif self.y <= -BORDER_HEIGHT + 20:
            self.dy *= -self.bounce

    def reset(self):
        self.state = "inactive"

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.color(self.color)
            pen.shape(self.shape)
            pen.stamp()

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.cos(math.radians(self.heading)) * self.thrust

            self.x += self.dx
            self.y += self.dy

            self.border_chk()
            if self.health <= 0:
                self.state = self.reset()

class Enemy(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)
        self.max_health = 50
        self.health = self.max_health

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.shapesize(stretch_wid=1, stretch_len=1, outline=None)
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.setheading(self.heading)
            pen.stamp()

            # Draw health
            pen.goto(self.x - x_offset - 10.0, self.y - y_offset + 20.0)
            pen.width(3.0)
            pen.pendown()
            pen.setheading(0.0)
            try:
                if self.health / self.max_health < 0.3:
                    pen.color("red")
                elif self.health / self.max_health < 0.7:
                    pen.color("yellow")
                else:
                    pen.color("green")
                pen.fd(20.0 * (self.health / self.max_health))
                if self.health < self.max_health:
                    pen.color("grey")
                    pen.fd(20.0 * ((self.max_health - self.health) / self.max_health))
            except Exception as e:
                print(e)

        pen.penup()

class Powerup(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)
        
