from typing import Any
from pygame import *
from pygame import display
from pygame import sprite
window = display.set_mode((400, 500))
display.set_caption("CS:GO TESAK EDITION")

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self,pl_image, pl_x, pl_y, size_x, size_y, pl_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pl_image),(size_x, size_y))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update (self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 680:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5 :
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 14, 20, -15)
        bullets.add(bullet)
from random import *
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(0, 400)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("asteroid.png", randint(0, 450), -40, 50,50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()
finish = False
background = transform.scale(image.load("galaxy.jpg"),(400, 500))
ship = Player("rocket.png", 100, 400, 80, 100, 10)
import sys

font.init()
mainfont = font.SysFont("comicsansms", 30)

win = mainfont.render("YOU WIN!",  True, (255,255,255))
lose = mainfont.render("YOU LOSE!",  True, (255,0,0))
score = 0
lost = 0
fire_sound = mixer.Sound('fire.ogg')
max_lost = 3
#хелоу
rel_time = False
num_fire = 0
from time import time as timer
while True:
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                    #fire_sound.play()

                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish: #
        window.blit(background, (0,0))
        text_rakh = mainfont.render("Рахунок: "+ str(score), True, (255,255,255))
        text_skip = mainfont.render("Пропущені: "+ str(lost), True, (255,255,255))
        window.blit(text_rakh, (10,10))
        window.blit(text_skip, (10,50))

        ship.update()
        monsters.update()
        bullets.update()


        ship.draw()
        bullets.draw(window)
        monsters.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = mainfont.render("Wait...reload!",  True, (255,255,255))
                window.blit(reload, (180, 450))
            else:
                num_fire = 0
                rel_time = False
                



        collides = sprite.groupcollide(monsters, bullets,  True, True)
        for c in collides:
            score +=1
            monster = Enemy("asteroid.png", randint(0, 450), -40, 50,50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost > max_lost:
            finish = True
            window.blit(lose,(200, 200))
        if score >= 10:
            finish = True
            window.blit(win,(200, 200))


    display.update()
    time.delay(50)








