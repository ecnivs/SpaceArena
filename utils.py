from sprite import Sprite
import random
from settings import WIDTH, RADAR

class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.left = self.x - (WIDTH / 2)
        self.right = self.x + (WIDTH / 2)
        self.radar = RADAR

    def update(self, x, y):
        self.x = x
        self.y = y
        self.left = self.x - (WIDTH / 2)
        self.right = self.x + (WIDTH / 2)


class Star(Sprite):
    def __init__(self, x, y, shape="circle", color="yellow"):
        Sprite.__init__(self, x, y, shape, color)
        self.distance = random.randint(2, 6)
        self.color = random.choice(["white", "yellow", "orange", "red"])
        self.width = 0.5 / self.distance

    def render(self, pen, x_offset=0, y_offset=0):
        pen.shapesize(
            stretch_wid=0.5 / self.distance,
            stretch_len=0.5 / self.distance,
            outline=None,
        )
        pen.goto(self.x - x_offset / self.distance, self.y - y_offset / self.distance)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.setheading(self.heading)
        pen.stamp()
