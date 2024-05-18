import math
from settings import BORDER_WIDTH, BORDER_HEIGHT, BOUNCE, ENEMY_REGEN, ENEMY_SPEED, MAX_HEALTH, PLAYERS
import random

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

    @staticmethod
    def is_collision(sprite, other, threshold):
        d = math.sqrt((sprite.x-other.x)**2 + (sprite.y-other.y)**2)
        if d < threshold:
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

    def collide(self, other):
        # swapping momentum
        temp_dx = self.dx
        temp_dy = self.dy

        self.dx = other.dx
        self.dy = other.dy
        
        other.dx = temp_dx
        other.dy = temp_dy
        
        # collision damage
        self.health -= (self.max_health/5)
        other.health -= (other.max_health/10)

        # 25% chance to change stance on collision
        if isinstance(other, Enemy):
            if (random.randrange(1,100)) > 75:
                other.stance = random.choice(["agressive", "passive", "idle"])
                if other.stance == "agressive":
                    other.color = "red"
                elif other.stance == "passive":
                    other.color = "orange"
                elif other.stance == "idle":
                    other.color = "yellow"


    def border_chk(self):
        # bounce off borders
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

    def render_health(self, pen, x_offset, y_offset):
        # draw health
        if self.state == "active":
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
                if self.health != self.max_health:
                    pen.color("grey")
                    pen.fd(20.0 * ((self.max_health - self.health) / self.max_health))
            except Exception as e:
                print(e)

        pen.penup()

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
    def __init__(self, x, y, shape, color, target1, target2):
        Sprite.__init__(self, x, y, shape, color)
        self.dx = 0
        self.dy = 0
        self.target = random.choice([target1, target2])
        self.target1 = target1
        self.target2 = target2
        self.regen = ENEMY_REGEN
        self.speed = ENEMY_SPEED
        self.max_health = 50
        self.health = self.max_health
        self.max_dx = 3.0
        self.max_dy = 3.0 
        self.stance = random.choice(["agressive", "passive", "idle"])

        if self.stance == "agressive":
            self.color = "red"
            self.sensor_range = random.randint(100, 200)
        elif self.stance == "passive":
            self.color = "orange"
            self.sensor_range = random.randint(100, 200)
        elif self.stance == "idle":
            self.color = "yellow"
            self.sensor_range = random.randint(200, 400)

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

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360

            self.border_chk()
            if self.health <= 0:
                self.state = self.reset()

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust
        
            self.x += self.dx
            self.y += self.dy    

            # check distance to players
            tar_dist1 = ((self.target1.x - self.x)**2 + (self.target1.y - self.y)**2)**0.5
            tar_dist2 = ((self.target2.x - self.x)**2 + (self.target2.y - self.y)**2)**0.5
            
            # choose closer player as target
            if tar_dist1 > tar_dist2:
                self.target = self.target2
            else:
                self.target = self.target1
            
            # Change movement based on type
            if self.stance == "agressive":
                if Sprite.is_collision(self.target, self, self.sensor_range):
                    if self.x < self.target.x:
                        self.dx += self.speed
                    else: 
                        self.dx -= self.speed

                    if self.y < self.target.y:
                        self.dy += self.speed
                    else: 
                        self.dy -= self.speed
                
            elif self.stance == "idle":
                if self.dx != 0 or self.dy != 0:
                    self.dx /= 1.002
                    self.dy /= 1.002
                
                if Sprite.is_collision(self.target, self, self.sensor_range):
                    self.stance = "agressive"
                    self.color = "red"
                
            elif self.stance == "passive":
                if Sprite.is_collision(self.target, self, self.sensor_range):
                    if self.x > self.target.x:
                        self.dx += (self.speed - (self.speed/5))
                    else: 
                        self.dx -= (self.speed -(self.speed/5))

                    if self.y > self.target.y:
                        self.dy += (self.speed - (self.speed/5))
                    else: 
                        self.dy -= (self.speed - (self.speed/5))
                elif self.dx != 0 or self.dy != 0:
                    self.dx /= 1.002
                    self.dy /= 1.002
            
            # Check max velocity
            if self.dx > self.max_dx:
                self.dx = self.max_dx
            elif self.dx < -self.max_dx:
                self.dx = -self.max_dx
                
            if self.dy > self.max_dy:
                self.dy = self.max_dy
            elif self.dy < -self.max_dy:
                self.dy = -self.max_dy   

            # regen
            if self.health < self.max_health:
                self.health += self.regen

class Powerup(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)
        
