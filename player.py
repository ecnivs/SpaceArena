import math
from settings import ACCELERATION, DAMAGE,MAX_FUEL, MAX_HEALTH, LIVES, MAX_THRUST, REGEN, ROTATION_SPEED
from sprite import Sprite

# lists
players = []
missiles1 = []
missiles2 = []

class Player(Sprite):
    def __init__(self, x, y, shape, color, missiles):
        Sprite.__init__(self, x, y, shape, color)
        self.lives = LIVES
        self.heading = 90
        self.da = 0
        self.rotation = ROTATION_SPEED
        self.thrust = 0.0
        self.max_thrust = MAX_THRUST
        self.acceleration = ACCELERATION
        self.max_health = MAX_HEALTH
        self.health = self.max_health
        self.damage = DAMAGE
        self.width = 20
        self.height = 20
        self.regen = REGEN
        self.missiles = missiles

    def accelerate(self):
        self.thrust += self.acceleration

        # max speed
        if self.thrust >= self.max_thrust:
            self.thrust = self.max_thrust

    def decelerate(self):
        self.thrust = 0

    def brake(self):
        self.thrust = 0
        self.dx /= 1.2
        self.dy /= 1.2

    def reverse(self):
        self.thrust -= self.acceleration

    def rotate_left(self):
        self.da = self.rotation

    def rotate_right(self):
        self.da = -self.rotation

    def stop_rotation(self):
        self.da = 0
    
    # prevent players from leaving the camera
    def cam_chk(self, camera_left, camera_right):
        if self.x > camera_right - 20:
            self.dx *= -1
        elif self.x < camera_left + 20:
            self.dx *= -1

    def fire(self):

        directions = [0, 5, -5]

        for missile in self.missiles:
            if missile.state == "ready":
                missile.x = self.x
                missile.y = self.y
                missile.heading = self.heading + directions[0]
                missile.dx = math.cos(math.radians(missile.heading)) * missile.thrust
                missile.dy = math.sin(math.radians(missile.heading)) * missile.thrust
                missile.dx += self.dx
                missile.dy += self.dy
                missile.state = "active"
                
                # recoil
                self.dx -= missile.dx * 0.02
                self.dy -= missile.dy * 0.02

                directions.pop(0)

                if len(directions) == 0:
                    break

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

            self.x += self.dx
            self.y += self.dy

            self.border_chk()

            if self.health <= 0:
                self.reset()
            if self.lives < 1:
                self.state = "inactive"
            
            # regen
            if self.health < self.max_health:
                self.health += self.regen

    def reset(self):
        self.health = self.max_health
        self.dx = 0
        self.dy = 0
        self.lives -= 1

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.shapesize(stretch_wid=1, stretch_len=1, outline=None)
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.setheading(self.heading)
            pen.stamp()
            self.render_health(pen, x_offset, y_offset)

        pen.penup()

class Missile(Sprite):
    def __init__(self, x, y, shape="circle", color="yellow"):
        Sprite.__init__(self, x, y, shape, color)
        self.state = "ready"
        self.thrust = 4.0
        self.max_fuel = MAX_FUEL
        self.fuel = self.max_fuel
        self.height = 4.0
        self.width = 4.0

    def update(self):
        self.heading += self.da
        self.heading %= 360.0

        self.x += self.dx
        self.y += self.dy

        self.border_chk()

        self.fuel -= (self.thrust)
        if self.fuel < 0:
            self.state = "ready"
            self.fuel = self.max_fuel

    def reset(self):
        self.state = "ready"
        self.fuel = self.max_fuel

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.shapesize(stretch_wid=0.2, stretch_len=0.2, outline=None)
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.setheading(self.heading)
            pen.stamp()
            pen.shapesize(stretch_wid=1, stretch_len=1, outline=None)

# register missiles
missile1 = Missile(0,0, "circle", "yellow")
missile2 = Missile(0,0, "circle", "yellow")

# register players
player1 = Player(-100, 0, "turtle", "blue", missiles1)
player2 = Player(100, 0, "turtle", "red", missiles2)
