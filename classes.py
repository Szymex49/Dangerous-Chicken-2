"""A module with classes designed for creating objects in game.
List of objects:
 - main hero
 - enemy
 - missile
 - explosion
"""

import pygame as pg
from pygame.locals import *
from tools import *
import os
import math


class Hero(pg.sprite.Sprite):
    """A character who is controlled by the player."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(load_image('hero.jpg'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, screen_height/2)
        self.x_velocity = 0
        self.y_velocity = 0
        self.life = 3

    def update(self):
        """Update the position of the hero."""
        self.rect.move_ip((self.x_velocity, self.y_velocity))
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height


class Enemy(pg.sprite.Sprite):
    """An enemy who moves towards the player."""

    def __init__(self, starting_position:tuple, velocity:int, lifes:int):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(load_image('enemy.jpg'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = starting_position
        self.x_velocity = 0
        self.y_velocity = 0
        self.velocity = velocity
        self.lifes = lifes
    
    def update(self, hero_coords:tuple):
        """Update the position of the enemy"""
        x_dist = hero_coords[0] - self.rect.center[0]
        y_dist = hero_coords[1] - self.rect.center[1]
        dist = math.sqrt(x_dist**2 + y_dist**2)
        try:
            self.x_velocity = (self.velocity * x_dist) / dist
            self.y_velocity = (self.velocity * y_dist) / dist 
        except ZeroDivisionError:
            pass
        self.rect.move_ip((self.x_velocity, self.y_velocity))


class Missile(pg.sprite.Sprite):
    """A missile which moves towards the aim."""

    def __init__(self, start_position:tuple, aim:tuple, velocity:int):
        pg.sprite.Sprite.__init__(self)
        self.velocity = velocity
        self.aim = aim

        x_dist = self.aim[0] - start_position[0]
        y_dist = self.aim[1] - start_position[1]
        dist = math.sqrt(x_dist**2 + y_dist**2)
        self.x_velocity = (self.velocity * x_dist) / dist
        self.y_velocity = (self.velocity * y_dist) / dist

        # Find an angle of rotation
        if y_dist <= 0:
            angle = 180 * math.acos((x_dist / dist)) / math.pi
        else:
            angle = 180 * math.acos(-x_dist / dist) / math.pi + 180

        self.image = pg.transform.rotate(pg.transform.scale(load_image('rocket.png'), (80, 40)), angle)
        self.rect = self.image.get_rect()
        self.rect.center = start_position
        
    def update(self):
        """Update the position of the missile"""
        self.rect.move_ip((self.x_velocity, self.y_velocity))


class Explosion(pg.sprite.Sprite):
    """An animation of explosion displayed when an enemy is destroyed."""

    def __init__(self, position:tuple):
        pg.sprite.Sprite.__init__(self)
        self.position = position
        self.images = [pg.transform.scale(load_image('explosion\\' + image), (150, 150)) for image in os.listdir('files\explosion')]
        self.image_number = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = position
    
    def update(self):
        """Display next frame."""
        self.image_number += 1
        self.image = self.images[self.image_number]
        if self.image_number + 1 >= len(self.images):
            self.kill()