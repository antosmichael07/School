import pygame as pg
from entities.entity import Entity
from settings import PLAYER_SPEED, WIDTH, HEIGHT

class Player(Entity):
    def __init__(self, game, pos, size, image):
        super().__init__(game, pos, size, image)
        self.speed = PLAYER_SPEED
        self.image_left = pg.transform.flip(self.image, True, False)
        self.image_right = self.image
    
    def update(self, dt):
        keys = pg.key.get_pressed()
        vel = pg.Vector2(0, 0)
        
        if keys[pg.K_LEFT]:
            vel.x = -1
            self.image = self.image_left
        if keys[pg.K_RIGHT]:
            vel.x = 1
            self.image = self.image_right
        if keys[pg.K_UP]:
            vel.y = -1
        if keys[pg.K_DOWN]:
            vel.y = 1
        
        if vel.length() > 0:
            vel = vel.normalize()
        
        self.pos += vel * self.speed * dt
        self.rect.center = self.pos
        
        self.rect.clamp_ip(pg.Rect(0, 0, WIDTH, HEIGHT))
        self.pos = pg.Vector2(self.rect.center)
