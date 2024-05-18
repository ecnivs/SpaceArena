from sprite import Sprite
import random
from settings import WIDTH, RADAR
import os
import platform
import winsound
import turtle

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

class Particle(Sprite):
    def __init__(self, x, y, shape = "triangle", color = "red"):
        Sprite.__init__(self, x, y, shape, color)
        self.dx = random.randint(-6, 6)
        self.dy = random.randint(-6, 6)
        self.frame = random.randint(10, 20)
        self.color = random.choice(["red", "orange", "yellow"])
        self.shape = "triangle"
        self.state = "inactive"
        
    def render(self, pen, x_offset = 0, y_offset = 0):
        self.frame -= 1
        self.dx *= 0.85
        self.dy *= 0.85
        if self.frame <= 0:
            self.frame = random.randint(10, 20)
            self.state = "inactive"
        pen.shapesize(stretch_wid=0.05, stretch_len=0.05, outline=None) 
        pen.goto(self.x - x_offset, self.y - y_offset)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()   

class Exhaust():
    def __init__(self, number_of_particles):
        self.particles = []
        for _ in range(number_of_particles):
            self.particles.append(Particle(0,0))
            
    def explode(self, x, y, dx_offset, dy_offset):
        for particle in self.particles:
            if particle.state == "inactive":
                particle.color = random.choice(["red", "orange", "yellow"])
                particle.x = x
                particle.y = y
                particle.dx = random.randint(-1, 1)
                particle.dy = random.randint(-1, 1)
                particle.dx += dx_offset * 2
                particle.dy += dy_offset * 2
                particle.state = "active"
                
    def render(self, pen, x_offset = 0, y_offset = 0):
        for particle in self.particles:
            if particle.state == "active":
                particle.update()
                pen.width(2)
                particle.render(pen, x_offset, y_offset)

class Explosion():
    def __init__(self, number_of_particles):
        self.particles = []
        for _ in range(number_of_particles):
            self.particles.append(Particle(0,0))
            
    def explode(self, x, y, dx_offset = 0, dy_offset = 0):
        for particle in self.particles:
            if particle.state == "inactive":
                particle.x = x
                particle.y = y
                particle.dx = random.randint(-12, 12)
                particle.dy = random.randint(-12, 12)
                particle.dx += dx_offset * 2
                particle.dy += dy_offset * 2
                particle.state = "active"
                
    def render(self, pen, x_offset = 0, y_offset = 0):
        for particle in self.particles:
            if particle.state == "active":
                particle.update()
                particle.render(pen, x_offset, y_offset)

# If on Windows, import winsound or, better yet, switch to Linux!
if platform.system() == "Windows":
    try:
        import winsound
    except:
        print ("Winsound module not available.")
        
def play_sound(sound_file, time = 0):
    # Windows
    if platform.system() == 'Windows':
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    # Linux
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    # Mac
    else:
        os.system("afplay {}&".format(sound_file))

    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time * 1000))   
