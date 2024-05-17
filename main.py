# SpaceArena - The ultimate Python turtle graphics game
# by Vince Swu

import turtle
from settings import BORDER_HEIGHT, WIDTH, HEIGHT, BORDER_WIDTH
from sprite import *
from player import *
from utils import Camera, Star
from penconf import *
import random

# secreen setup
wn = turtle.Screen()
wn.setup(WIDTH+220, HEIGHT+220)
wn.title("Space Arena")
wn.bgcolor("black")
wn.tracer(0)

# sprite lists
sprites = []
background_sprites = []

# game class
class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame = 0
        self.level = 2

    def start_level(self):
        sprites.clear()

        for _ in range(self.level):
            x = random.randint(-self.width//2, self.width//2)
            y = random.randint(-self.height//2, self.height//2)
            sprites.append(Enemy(x, y, "square", "red", players[0], players[-1]))

        for _ in range(self.level):
            x = random.randint(-self.width//2, self.width//2)
            y = random.randint(-self.height//2, self.height//2)
            sprites.append(Powerup(x, y, "circle", "green"))
    
    def render_border(self, pen, x_offset, y_offset):
        pen.color("white")
        pen.width(3)
        pen.penup()
        left = -self.width - x_offset
        right = self.width - x_offset
        top = self.height - y_offset
        bottom = -self.height - y_offset

        pen.goto(left, top)
        pen.pendown()
        pen.goto(right, top)
        pen.goto(right, bottom)
        pen.goto(left, bottom)
        pen.goto(left, top)
        pen.penup()

    def render_info(self, pen, active_enemies):
        pen.color("#202020")
        pen.penup()
        pen.goto(400, 0)
        pen.shape("square")
        pen.setheading(90)
        pen.shapesize(10, 32, None)
        pen.stamp()
        
        pen.color("white")
        pen.width(3)
        pen.goto(300, 400)
        pen.pendown()
        pen.goto(300, -400)
        
        pen.penup()
        pen.color("white")
        character_pen.scale = 1.0
        character_pen.draw_string(pen, "SPACE ARENA", 400, 270)
        character_pen.draw_string(pen, "ENEMIES {}".format(active_enemies), 400, 240)
        character_pen.draw_string(pen, "LEVEL {}".format(game.level), 400, 210)
        if PLAYERS > 1:
            character_pen.draw_string(pen, "1P LIVES {}".format(player.lives), 400, 180)
            character_pen.draw_string(pen, "1P SCORE {}".format(player1.score), 400, 150)
            character_pen.draw_string(pen, "2P LIVES {}".format(player.lives), 400, 120)
            character_pen.draw_string(pen, "2P SCORE {}".format(player2.score), 400, 90)
        else:
            character_pen.draw_string(pen, "LIVES {}".format(player1.lives), 400, 180)
            character_pen.draw_string(pen, "SCORE {}".format(player1.score), 400, 150)
        
    def start(self):
        self.state = "playing"

class Radar():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, pen):
        pen.color("white")
        pen.setheading(90)
        pen.goto(self.x + self.width / 2.0, self.y)
        pen.pendown()
        pen.fillcolor("black")
        pen.begin_fill()
        pen.circle(self.width / 2.0)
        pen.end_fill()
        pen.penup()

        # draw sprites
        for sprite in sprites:
            if sprite.state == "active":
                radar_x = self.x + (sprite.x - camera.x) * (self.width/ game.width)
                radar_y = self.y + (sprite.y - camera.y) * (self.height/ game.height)
                pen.goto(radar_x, radar_y)
                pen.color(sprite.color)
                pen.setheading(sprite.heading)
                pen.shape(sprite.shape)
                pen.shapesize(0.4, 0.4, None)              
                distance = ((camera.x-sprite.x)**2 + (camera.y - sprite.y)**2)**0.5
                if distance < camera.radar:
                    pen.stamp()

        # draw sprites
        for player in players:
            if player.state == "active":
                radar_x = self.x + (player.x - camera.x) * (self.width/ game.width)
                radar_y = self.y + (player.y - camera.y) * (self.height/ game.height)
                pen.goto(radar_x, radar_y)
                pen.color(player.color)
                pen.setheading(player.heading)
                pen.shape(player.shape)
                pen.shapesize(0.4, 0.4, None)              
                distance = ((camera.x-player.x)**2 + (camera.y - player.y)**2)**0.5
                if distance > camera.radar:
                    pen.shape("circle")
                pen.stamp()
                pen.shape(player.shape)

        # draw sprites
        for missile in missiles1:
            if missile.state == "active":
                radar_x = self.x + (missile.x - camera.x) * (self.width/ game.width)
                radar_y = self.y + (missile.y - camera.y) * (self.height/ game.height)
                pen.goto(radar_x, radar_y)
                pen.color(missile.color)
                pen.setheading(missile.heading)
                pen.shape(missile.shape)
                pen.shapesize(0.1, 0.1, None)              
                distance = ((camera.x-missile.x)**2 + (camera.y - missile.y)**2)**0.5
                if distance < camera.radar:
                    pen.stamp()

        # draw sprites
        for missile in missiles2:
            if missile.state == "active":
                radar_x = self.x + (missile.x - camera.x) * (self.width/ game.width)
                radar_y = self.y + (missile.y - camera.y) * (self.height/ game.height)
                pen.goto(radar_x, radar_y)
                pen.color(missile.color)
                pen.setheading(missile.heading)
                pen.shape(missile.shape)
                pen.shapesize(0.1, 0.1, None)              
                distance = ((camera.x-missile.x)**2 + (camera.y - missile.y)**2)**0.5
                if distance < camera.radar:
                    pen.stamp()

# set up the game
game = Game(BORDER_WIDTH, BORDER_HEIGHT)
radar = Radar(400, -200, 200, 200)
character_pen = CharacterPen("white",3.0)

# stars
stars = []
for _ in range(80):
    x = random.randint(int(-game.width), int(game.width))
    y = random.randint(int(-game.height), int(game.height))
    stars.append(Star(x, y))
for star in stars:
    background_sprites.append(star)

# players
players.append(player1)
if PLAYERS > 1:
    players.append(player2)

# add sprites to list
missiles1.append(missile1)
missiles2.append(missile2)

# set up the camera
camera = Camera(0, 0)

# set up the level
game.start_level()

# listen for keystrokes
wn.listen()

# player1 controls
wn.onkeypress(player1.rotate_left, "a")
wn.onkeypress(player1.rotate_right, "d")
wn.onkeypress(player1.accelerate, "w")
wn.onkeypress(player1.reverse, "s")
wn.onkeypress(player1.rotate_left, "A")
wn.onkeypress(player1.rotate_right, "D")
wn.onkeypress(player1.accelerate, "W")
wn.onkeypress(player1.reverse, "S")

wn.onkeypress(player1.brake, "e")
wn.onkeypress(player1.brake, "E")
wn.onkeypress(player1.fire, "space")

wn.onkeyrelease(player1.stop_rotation, "a")
wn.onkeyrelease(player1.stop_rotation, "d")
wn.onkeyrelease(player1.decelerate, "w")
wn.onkeyrelease(player1.decelerate, "s")
wn.onkeyrelease(player1.stop_rotation, "A")
wn.onkeyrelease(player1.stop_rotation, "D")
wn.onkeyrelease(player1.decelerate, "W")
wn.onkeyrelease(player1.decelerate, "S")

# player2 controls
wn.onkeypress(player2.rotate_left, "Left")
wn.onkeypress(player2.rotate_right, "Right")
wn.onkeypress(player2.accelerate, "Up")
wn.onkeypress(player2.reverse, "Down")

wn.onkeypress(player2.brake, "Shift_L")
wn.onkeypress(player2.fire, "Return")

wn.onkeyrelease(player2.stop_rotation, "Left")
wn.onkeyrelease(player2.stop_rotation, "Right")
wn.onkeyrelease(player2.decelerate, "Up")
wn.onkeyrelease(player2.decelerate, "Down")

while True:
    # render borders
    game.render_border(pen, camera.x - 100, camera.y)

    # camera update
    mid_x = (players[0].x + players[-1].x) / 2
    mid_y = (players[0].y + players[-1].y) / 2
    camera.update(mid_x, mid_y)

    # render stars
    for sprite in background_sprites:
        sprite.update()
        if Sprite.is_on_screen(sprite, WIDTH, HEIGHT, player1.x, player1.y):
            sprite.render(pen, camera.x + 100, camera.y)
        elif Sprite.is_on_screen(sprite, WIDTH, HEIGHT, player2.x, player2.y):
            sprite.render(pen, camera.x + 100, camera.y)

    for player in players:
        player.render(pen, camera.x - 100, camera.y)
        Player.update(player)
        player.cam_chk(camera.left, camera.right)

    for missile in missiles1:
        Missile.update(missile)
        missile.render(pen, camera.x - 100, camera.y)

    for missile in missiles2:
        Missile.update(missile)
        missile.render(pen, camera.x - 100, camera.y)

    for sprite in sprites:
        sprite.update()
        sprite.render(pen, camera.x - 100, camera.y)

    # check for collisions
    for sprite in sprites:
        if isinstance(sprite, Enemy) and sprite.state == "active":
            if players[0].is_collision(sprite):
                players[0].collide(sprite)

            if len(players) > 1:
                if players[-1].is_collision(sprite):
                    players[-1].collide(sprite)

            if missile1.state == "active" and missile1.is_collision(sprite):
                sprite.health -= player1.damage
                missile1.reset()

            if missile2.state == "active" and missile2.is_collision(sprite):
                sprite.health -= player2.damage
                missile2.reset()

        if isinstance(sprite, Powerup):
            if players[0].is_collision(sprite) and sprite.state == "active":
                sprite.reset()
                players[0].health = players[0].max_health
                players[0].score += 50

            if len(players) > 1:
                if players[-1].is_collision(sprite) and sprite.state == "active":
                    sprite.reset()
                    players[-1].health = players[-1].max_health
                    players[-1].score += 50

            if missile1.state == "active" and missile1.is_collision(sprite):
                sprite.reset()
                missile1.reset()

            if missile2.state == "active" and missile2.is_collision(sprite):
                sprite.reset()
                missile2.reset()
    
    # player collision
    if len(players) > 1:
        if players[0].is_collision(players[-1]):
            players[0].collide(players[-1])

    # missile to player collision
    if player1.is_collision(missile2) and missile2.state == "active":
        player1.health -= (player2.damage//2)
        missile2.reset()
    if player2.is_collision(missile1) and missile1.state == "active":
        player2.health -= (player1.damage//2)
        missile1.reset()
    
    # remove players if inactive
    if len(players) > 1:
        if players[0].state == "inactive":
            players.pop(0)
    if len(players) > 1:
        if players[-1].state == "inactive":
            players.pop(-1)
    
    # check for end of start
    end_level = True
    for sprite in sprites:
        if isinstance(sprite, Enemy) and sprite.state == "active":
            end_level = False
    if end_level:
        game.level +=1
        game.start_level()

    # render stats
    game.render_info(pen, 0)
    radar.render(pen)
    
    # update the screen
    wn.update()

    # clear the screen
    pen.clear()
