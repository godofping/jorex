#missing animation. menu. input name. database. keyboard
import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import argparse
import os
import random


pygame.HWSURFACE
#this set the start up position of the game
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150,50)

#capture video from webcam.
device = cv2.VideoCapture(0)


#set the width and height of the camera
device.set(3, 1280.)#width
device.set(4, 720.)#height

#define variables
WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
FPS = 60
score = 0
multiplier = 1
name = ""

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Thesis 1: Fruit razor")
screen = pygame.display.set_mode([WINDOWWIDTH,WINDOWHEIGHT],pygame.FULLSCREEN)


xlocation = random.randint(40,700)
counter = 0
pointerx = 0
pointery = 0
gotTime = False
endGame = True
life = 5
speed = 20
starttime = 0
endtime = 0
isentername = 0

# define colors
RED = pygame.Color(255,0,0)
BLUE = pygame.Color(0,0,255)
WHITE = pygame.Color(255,255,255)
BLACK = pygame.Color(0,0,0)
GREEN = pygame.Color(0, 255, 0)

screenstatus = 0

lasttimeout = 0


# set up assets folders
game_folder = os.path.dirname(__file__) #D:\Python
# concats the two folder
img_folder = os.path.join(game_folder,"img") #D:\Python\img

snd_folder = os.path.join(game_folder,'snd') #D:\Python\snd


#screen classes Player

class GameOver(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class QuitGame(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class AboutScreen(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class HelpScreen(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class MainMenu(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class ScoreMenu(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class DoYouWantToAgainPlayBackground(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()

        self.rect.left, self.rect.top = location

#button classes


#interactive buttons

class YesButtonQuit(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "yes-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.5) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 400
        self.rect.y = 490

class NoButtonQuit(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "no-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.5) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 690
        self.rect.y = 490

class YesButtonQuitTry(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "yes-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.5) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 234
        self.rect.y = 301

class NoButtonQuitTry(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "no-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.5) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 906
        self.rect.y = 301

class BackButtonScore(pygame.sprite.Sprite):
    #sprite of the back button
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "back-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.5) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 16
        self.rect.y = 152

class BackButtonAbout(pygame.sprite.Sprite):
    #sprite of the back button
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "back-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.3) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 16
        self.rect.y = 152

class BackButtonHelp(pygame.sprite.Sprite):
    #sprite of the back button
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "back-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.3) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 16
        self.rect.y = 152



class PlayButton(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "play-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.3) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 513
        self.rect.y = 290


class ScoreButton(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "score-button.png")).convert_alpha()

        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.3) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 513
        self.rect.y = 380

class HelpButton(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "help-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.3) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 513
        self.rect.y = 460

class AboutButton(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "about-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.3) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 513
        self.rect.y = 560

class ExitButton(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "exit-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.3) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 1032
        self.rect.y = 14

#progress bar

class Time1(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Time2(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Time3(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Time4(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Time5(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Time6(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Time7(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Time8(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Time9(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Time10(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location



#heart classes

class Heart1(pygame.sprite.Sprite):
    #sprite of the heart1
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Heart2(pygame.sprite.Sprite):
    #sprite of the heart2
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Heart3(pygame.sprite.Sprite):
    #sprite of the heart3
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Heart4(pygame.sprite.Sprite):
    #sprite of the heart4
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
class Heart5(pygame.sprite.Sprite):
    #sprite of the heart5
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class MainGameFrame(pygame.sprite.Sprite):
    #sprite of the background in game proper
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Player(pygame.sprite.Sprite):
    #sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "sword.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.5) / 2)
        self.mask = pygame.mask.from_surface(self.image)


#normal fruits


class Pomelo(pygame.sprite.Sprite):
    #sprite for the Pomelo
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

       
        self.image = pygame.image.load(os.path.join(img_folder, "pomelo.png")).convert_alpha()
        self.image_orig = pygame.image.load(os.path.join(img_folder, "pomelo.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 1) / 2)
        self.rect.x = random.randrange(60, WINDOWWIDTH - (self.rect.width+59))
        self.rect.y = random.randrange(0, 20)
        self.speedy = random.randrange(8, 15)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        
    
    def rotate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update =  now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy

        #when this fruit reaches the bottom. kill this
        if self.rect.top > WINDOWHEIGHT - 20:
            global life
            life -= 1
            self.kill()
          
class Mangosteen(pygame.sprite.Sprite):
    #sprite for the mangosteen
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

       
        self.image = pygame.image.load(os.path.join(img_folder, "mangosteen.png")).convert_alpha()
        self.image_orig = pygame.image.load(os.path.join(img_folder, "mangosteen.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 1) / 2)
        self.rect.x = random.randrange(60, WINDOWWIDTH - (self.rect.width+59))
        self.rect.y = random.randrange(0, 20)
        self.speedy = random.randrange(8, 15)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        
    
    def rotate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update =  now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy

        #when this fruit reaches the bottom. kill this
        if self.rect.top > WINDOWHEIGHT - 20:
            global life
            life -= 1
            self.kill()     

class Papaya(pygame.sprite.Sprite):
    #sprite for the Papaya
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

       
        self.image = pygame.image.load(os.path.join(img_folder, "papaya.png")).convert_alpha()
        self.image_orig = pygame.image.load(os.path.join(img_folder, "papaya.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 1) / 2)
        self.rect.x = random.randrange(60, WINDOWWIDTH - (self.rect.width+59))
        self.rect.y = random.randrange(0, 20)
        self.speedy = random.randrange(8, 15)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        
    
    def rotate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update =  now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy

        #when this fruit reaches the bottom. kill this
        if self.rect.top > WINDOWHEIGHT - 20:
            global life
            life -= 1
            self.kill()               

class Atis(pygame.sprite.Sprite):
    #sprite for the Atis
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

       
        self.image = pygame.image.load(os.path.join(img_folder, "atis.png")).convert_alpha()
        self.image_orig = pygame.image.load(os.path.join(img_folder, "atis.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 1) / 2)
        self.rect.x = random.randrange(60, WINDOWWIDTH - (self.rect.width+59))
        self.rect.y = random.randrange(0, 20)
        self.speedy = random.randrange(8, 15)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        
    
    def rotate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update =  now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy

        #when this fruit reaches the bottom. kill this
        if self.rect.top > WINDOWHEIGHT - 20:
            global life
            life -= 1
            self.kill()
          


#special fruits

class Mango(pygame.sprite.Sprite):
    #sprite for the Mango
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

       
        self.image = pygame.image.load(os.path.join(img_folder, "mangonm3.png")).convert_alpha()
        self.image_orig = pygame.image.load(os.path.join(img_folder, "mangonm3.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 1) / 2)
        self.rect.x = random.randrange(60, WINDOWWIDTH - (self.rect.width+59))
        self.rect.y = random.randrange(0, 20)
        self.speedy = random.randrange(8, 15)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        
    
    def rotate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update =  now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy

        #when this fruit reaches the bottom. kill this
        if self.rect.top > WINDOWHEIGHT - 20:
            self.kill()
          
class Durian(pygame.sprite.Sprite):
    #sprite for the Durian
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
       
        self.image = pygame.image.load(os.path.join(img_folder, "duriannm0.png")).convert_alpha()
        self.image_orig = pygame.image.load(os.path.join(img_folder, "duriannm0.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 1) / 2)
        self.rect.x = random.randrange(60, WINDOWWIDTH - (self.rect.width+59))
        self.rect.y = random.randrange(0, 20)
        self.speedy = random.randrange(8, 15)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        
    
    def rotate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update =  now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy

        #when this fruit reaches the bottom. kill this
        if self.rect.top > WINDOWHEIGHT - 20:
            self.kill()
                  
class Bomb(pygame.sprite.Sprite):
    #sprite for the Bomb
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

       
        self.image = pygame.image.load(os.path.join(img_folder, "bomb.png")).convert_alpha()
        self.image_orig = pygame.image.load(os.path.join(img_folder, "bomb.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 1) / 2)
        self.rect.x = random.randrange(60, WINDOWWIDTH - (self.rect.width+59))
        self.rect.y = random.randrange(0, 20)
        self.speedy = random.randrange(8, 15)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        
    
    def rotate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update =  now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy



        #when this bomb reaches the bottom. kill this
        if self.rect.top > WINDOWHEIGHT - 20:
            self.kill()
          
                  
            
#animation classes       
class atisSlice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = atis_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(atis_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = atis_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#animation classes       
class atisx2Slice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = atisx2_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(atisx2_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = atisx2_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class durianSlice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = durian_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(durian_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = durian_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class durianx2Slice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = durianx2_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(durianx2_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = durianx2_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class mangoSlice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = mango_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(mango_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = mango_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class mangox2Slice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = mangox2_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(mangox2_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = mangox2_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class mangosteenSlice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = mangosteen_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(mangosteen_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = mangosteen_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class mangosteenx2Slice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = mangosteenx2_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(mangosteenx2_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = mangosteenx2_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class papayaSlice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = papaya_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(papaya_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = papaya_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class papayax2Slice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = papayax2_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(papayax2_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = papayax2_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class pomeloSlice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pomelo_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(pomelo_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = pomelo_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class pomelox2Slice(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pomelox2_slice_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(pomelox2_slice_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = pomelox2_slice_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#game over menu
#keyboard classes
class SubmitButton(pygame.sprite.Sprite):
    #sprite of the Game over
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "submit-button.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.5) / 2)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 414
        self.rect.y = 503



#keyboard classes


 
#load all sounds
slice_sound = pygame.mixer.Sound(os.path.join(snd_folder, "slice.wav"))
bomb_sound = pygame.mixer.Sound(os.path.join(snd_folder, "bomb.wav"))
pygame.mixer.music.load(os.path.join(snd_folder, "background.wav"))
pygame.mixer.music.set_volume(0.2)



#load all sprites      
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
all_sprites.update()

#call Time function
Time1 = Time1(os.path.join(img_folder, "1.png"), [50,65])
Time2 = Time2(os.path.join(img_folder, "2.png"), [50,65])
Time3 = Time3(os.path.join(img_folder, "3.png"), [50,65])
Time4 = Time4(os.path.join(img_folder, "4.png"), [50,65])
Time5 = Time5(os.path.join(img_folder, "5.png"), [50,65])
Time6 = Time6(os.path.join(img_folder, "6.png"), [50,65])
Time7 = Time7(os.path.join(img_folder, "7.png"), [50,65])
Time8 = Time8(os.path.join(img_folder, "8.png"), [50,65])
Time9 = Time9(os.path.join(img_folder, "9.png"), [50,65])
Time10 = Time10(os.path.join(img_folder, "10.png"), [50,65])


#call Heart1 function
Heart1 = Heart1(os.path.join(img_folder, "heart.png"), [100,15])
Heart2 = Heart2(os.path.join(img_folder, "heart.png"), [130,15])
Heart3 = Heart3(os.path.join(img_folder, "heart.png"), [160,15])
Heart4 = Heart4(os.path.join(img_folder, "heart.png"), [190,15])
Heart5 = Heart5(os.path.join(img_folder, "heart.png"), [220,15])

#screen
GameOver = GameOver(os.path.join(img_folder, "gameover.png"), [0,0])
MainMenu = MainMenu(os.path.join(img_folder, "main-menu-background.png"), [0,0])
MainGameFrame = MainGameFrame(os.path.join(img_folder, "frame.png"), [0,0])
QuitGame = QuitGame(os.path.join(img_folder, "quit-background.png"), [0,0])
ScoreMenu = ScoreMenu(os.path.join(img_folder, "score-background.png"), [0,0])
AboutScreen = AboutScreen(os.path.join(img_folder, "about-background.png"), [0,0])
HelpScreen = HelpScreen(os.path.join(img_folder, "help-background.png"), [0,0])
DoYouWantToAgainPlayBackground = DoYouWantToAgainPlayBackground(os.path.join(img_folder, "youwanttoplayagain-background.png"), [0,0])


#import images use for atis slicing animation
atis_slice_animation = {}
atis_slice_animation['nm'] = []
for i in range(4):
    filename = 'atis-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    atis_slice_animation['nm'].append(img)

#import images use for atis slicing animation
atisx2_slice_animation = {}
atisx2_slice_animation['nm'] = []
for i in range(4):
    filename = 'atisx2-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    atisx2_slice_animation['nm'].append(img)

#import images use for durian slicing animation
durian_slice_animation = {}
durian_slice_animation['nm'] = []
for i in range(4):
    filename = 'durian-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    durian_slice_animation['nm'].append(img)

#import images use for mango slicing animation
mango_slice_animation = {}
mango_slice_animation['nm'] = []
for i in range(4):
    filename = 'mango-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    mango_slice_animation['nm'].append(img)

#import images use for mango slicing animation
mangox2_slice_animation = {}
mangox2_slice_animation['nm'] = []
for i in range(4):
    filename = 'mangox2-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    mangox2_slice_animation['nm'].append(img)


#import images use for mangosteen slicing animation
mangosteen_slice_animation = {}
mangosteen_slice_animation['nm'] = []
for i in range(4):
    filename = 'mangosteen-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    mangosteen_slice_animation['nm'].append(img)


#import images use for mangosteen slicing animation
mangosteenx2_slice_animation = {}
mangosteenx2_slice_animation['nm'] = []
for i in range(4):
    filename = 'mangosteenx2-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    mangosteenx2_slice_animation['nm'].append(img)

#import images use for papaya slicing animation
papaya_slice_animation = {}
papaya_slice_animation['nm'] = []
for i in range(4):
    filename = 'papaya-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    papaya_slice_animation['nm'].append(img)

#import images use for papaya slicing animation
papayax2_slice_animation = {}
papayax2_slice_animation['nm'] = []
for i in range(4):
    filename = 'papayax2-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    papayax2_slice_animation['nm'].append(img)

#import images use for pomelo slicing animation
pomelo_slice_animation = {}
pomelo_slice_animation['nm'] = []
for i in range(4):
    filename = 'pomelo-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    pomelo_slice_animation['nm'].append(img)

#import images use for pomelo slicing animation
pomelox2_slice_animation = {}
pomelox2_slice_animation['nm'] = []
for i in range(4):
    filename = 'pomelox2-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    pomelox2_slice_animation['nm'].append(img)


#import images use for durian drop animation
durian_drop_animation = {}
durian_drop_animation['nm'] = []
for i in range(4):
    filename = 'duriannm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    durian_drop_animation['nm'].append(img)

#import images use for mango drop animation
mango_drop_animation = {}
mango_drop_animation['nm'] = []
for i in range(4):
    if multiplier == 1:
        filename = 'mango-slashnm{}.png'.format(i)
    if multiplier == 2:
        filename = 'mangox2-slashnm{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert_alpha()
    mango_drop_animation['nm'].append(img)






pomeloes = pygame.sprite.Group() 
mangosteens = pygame.sprite.Group() 
papayas = pygame.sprite.Group() 
mangoes = pygame.sprite.Group() 
durians = pygame.sprite.Group() 
bombs = pygame.sprite.Group()
atises = pygame.sprite.Group() 
all_sprites = pygame.sprite.Group()
yesButtonQuits = pygame.sprite.Group()
noButtonQuits = pygame.sprite.Group()
PlayButtons = pygame.sprite.Group()
HelpButtons = pygame.sprite.Group()
ScoreButtons = pygame.sprite.Group()
AboutButtons = pygame.sprite.Group()
ExitButtons = pygame.sprite.Group()



    
#FPS controller
fpsController = pygame.time.Clock()

pygame.mixer.music.play(loops=-1)
pygame.mixer.music.pause()


#game loop
try:
    while endGame:
    #codes for the keyboard
        #process input events
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    sys.exit(0)



    #START CODE FOR THE BALL DETECTION
       
        
        #keep loop running at the right FPS
        fpsController.tick(FPS)

        #get the frame from the camera
        ret, frame = device.read()
       

#          65 28 45

# 93 150 126

        
        
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #create threshold
        #this is the color for orange
 
        lower_range = np.array([42, 70, 110])
        upper_range = np.array([79,255,255])

        
        #Command for just threshold image
        mask = cv2.inRange(hsv, lower_range, upper_range)


       

        #Create Contours for all green objects
        _, contours, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        maximumArea = 0
        bestContour = None
        for contour in contours:
            currentArea = cv2.contourArea(contour)
            if currentArea > maximumArea:
                bestContour = contour
                maximumArea = currentArea
            
        #Create a bounding box around the biggest green object
        if bestContour is not None:
            (x,y),radius = cv2.minEnclosingCircle(bestContour)
            center = (int(x),int(y))
            radius = int(radius)

            mouse_x, mouse_y = (abs(center[0] - 1280),center[1])
            circlecoor = 'x: %s y: %s'%(abs(center[0] - 1280),center[1])
            
            #print("The value of x: %s and the value of y: %s" %(x,y))
            pointerx = circlecoor
            pointery = radius

            #the cursor
            player.rect.center = (abs(center[0] - 1280),center[1])
            
        else:
            player.rect.x = (WINDOWWIDTH)

    #END CODE FOR THE BALL DETECTION


#############################################################################################################
        #check what is the screenstatus and display



        all_sprites.draw(screen)
        all_sprites.update()

        if screenstatus == 0: #0 for main menu
        #main  menu

            counter = 0
            currenttime = 0
            speed = 25

            name = ""
            isentername = 0
            screen.blit(MainMenu.image, MainMenu.rect)

            pomeloes = pygame.sprite.Group() 
            mangosteens = pygame.sprite.Group() 
            papayas = pygame.sprite.Group() 
            mangoes = pygame.sprite.Group() 
            durians = pygame.sprite.Group() 
            bombs = pygame.sprite.Group()
            atises = pygame.sprite.Group() 
            all_sprites = pygame.sprite.Group()
            yesButtonQuits = pygame.sprite.Group()
            noButtonQuits = pygame.sprite.Group()
            PlayButtons = pygame.sprite.Group()
            HelpButtons = pygame.sprite.Group()
            ScoreButtons = pygame.sprite.Group()
            AboutButtons = pygame.sprite.Group()
            ExitButtons = pygame.sprite.Group()


            playButton = PlayButton()
            all_sprites.add(playButton)
            PlayButtons.add(playButton)

            scoreButton = ScoreButton()
            all_sprites.add(scoreButton)
            ScoreButtons.add(scoreButton)

            helpButton = HelpButton()
            all_sprites.add(helpButton)
            HelpButtons.add(helpButton)

            aboutButton = AboutButton()
            all_sprites.add(aboutButton)
            AboutButtons.add(aboutButton)

            exitButton = ExitButton()
            all_sprites.add(exitButton)
            ExitButtons.add(exitButton)

            slices = pygame.sprite.spritecollide(player, PlayButtons, False, pygame.sprite.collide_circle)
            for slice in slices:
                screenstatus = 1
                lasttimeout = currenttime
               

                pomeloes = pygame.sprite.Group() 
                mangosteens = pygame.sprite.Group() 
                papayas = pygame.sprite.Group() 
                mangoes = pygame.sprite.Group() 
                durians = pygame.sprite.Group() 
                bombs = pygame.sprite.Group()
                atises = pygame.sprite.Group() 
                all_sprites = pygame.sprite.Group()
                yesButtonQuits = pygame.sprite.Group()
                noButtonQuits = pygame.sprite.Group()
                PlayButtons = pygame.sprite.Group()
                HelpButtons = pygame.sprite.Group()
                ScoreButtons = pygame.sprite.Group()
                AboutButtons = pygame.sprite.Group()
                ExitButtons = pygame.sprite.Group()
             


            slices = pygame.sprite.spritecollide(player, ScoreButtons, False, pygame.sprite.collide_circle)
            for slice in slices:
                screenstatus = 2

            slices = pygame.sprite.spritecollide(player, HelpButtons, False, pygame.sprite.collide_circle)
            for slice in slices:
                screenstatus = 3

            slices = pygame.sprite.spritecollide(player, AboutButtons, False, pygame.sprite.collide_circle)
            for slice in slices:
                screenstatus = 6

            slices = pygame.sprite.spritecollide(player, ExitButtons, False, pygame.sprite.collide_circle)
            for slice in slices:
                screenstatus = 4
          



            all_sprites.draw(screen)
            all_sprites.update()

        if screenstatus == 1: #1 for main game
        #start code for main game
            #start music
            currenttime = int(pygame.time.get_ticks()/1000) - lasttimeout
            pygame.mixer.music.unpause()



            #codes for the durian x2 effect. 
            if currenttime >= starttime and currenttime <= endtime:
                multiplier = 2
            else:
                multiplier = 1
                starttime = 0
                endtime = 0



            
            counter = counter + 1

            #adjust the drop speed of the fruits

            if currenttime >= 1:
                speed = 27
            if currenttime >= 15:
                speed = 24
            if currenttime >= 45:
                speed = 20
            if currenttime >= 80:
                speed = 18
           


            #draw and render
            if (life > 0) and (counter % speed == 0):
                #when game is not yet over, drop fruits

                #randomize number from 1 to 4
                randomNumber = random.randrange(1, 5)
                #randomNumber = 4
            
                if randomNumber == 1:
                    papaya = Papaya()
                    papayas.add(papaya)
                    all_sprites.add(papaya)

                if randomNumber == 2:
                    mangosteen = Mangosteen()
                    all_sprites.add(mangosteen)
                    mangosteens.add(mangosteen)

                if randomNumber == 3:
                    pomelo = Pomelo()
                    all_sprites.add(pomelo)
                    pomeloes.add(pomelo) 

                if randomNumber == 4:
                    atis = Atis()
                    all_sprites.add(atis)
                    atises.add(atis)

                #30 percent chance to drop the bomb in every second
                #randomize number from 1 to 10
                randomDropBombChance = random.randrange(1, 11)

                if randomDropBombChance == 1 or randomDropBombChance == 2 or randomDropBombChance == 3:
                    bomb = Bomb()
                    all_sprites.add(bomb)
                    bombs.add(bomb)

                #20 percent chance to drop the mango in every second
                #randomize number from 1 to 10
                randomDropMangoChance = random.randrange(1, 11)

                if randomDropMangoChance == 1 or randomDropMangoChance == 2:
                    mango = Mango()
                    all_sprites.add(mango)
                    mangoes.add(mango)

                #1 percent chance to drop the durian in every second if it is not activated
                #randomize number from 1 to 10 
                randomDropDurianChance = random.randrange(1, 11)

                if randomDropDurianChance == 1 and (starttime == 0 and endtime == 0):
                    durian = Durian()
                    all_sprites.add(durian)
                    durians.add(durian) 

            
            #check if the fruits are sliced

            slices = pygame.sprite.spritecollide(player, papayas, True, pygame.sprite.collide_circle)

            for slice in slices:
                if (life > 0):
                    slice_sound.play()
                    score += (1 * multiplier)
                    if multiplier == 1:
                        slicepapaya = papayaSlice(slice.rect.center, 'nm')
                    if multiplier == 2:
                        slicepapaya = papayax2Slice(slice.rect.center, 'nm')
                    all_sprites.add(slicepapaya)

            slices = pygame.sprite.spritecollide(player, mangosteens, True, pygame.sprite.collide_circle)
            for slice in slices:
                if (life > 0):
                    slice_sound.play()
                    score += (1 * multiplier)
                    if multiplier == 1:
                        slicemangosteen = mangosteenSlice(slice.rect.center, 'nm')
                    if multiplier == 2:
                        slicemangosteen = mangosteenx2Slice(slice.rect.center, 'nm')
                    all_sprites.add(slicemangosteen)


            slices = pygame.sprite.spritecollide(player, pomeloes, True, pygame.sprite.collide_circle)
            for slice in slices:
                if (life > 0):
                    slice_sound.play()
                    score += (1 * multiplier)
                    if multiplier == 1:
                        slicepomelo= pomeloSlice(slice.rect.center, 'nm')
                    if multiplier == 2:
                        slicepomelo= pomelox2Slice(slice.rect.center, 'nm')
                    all_sprites.add(slicepomelo)

            slices = pygame.sprite.spritecollide(player, atises, True, pygame.sprite.collide_circle)
            for slice in slices:
                if (life > 0):
                    slice_sound.play()
                    score += (1 * multiplier)
                    if multiplier == 1:
                        sliceatis = atisSlice(slice.rect.center, 'nm')
                    if multiplier == 2:
                        sliceatis = atisx2Slice(slice.rect.center, 'nm')
                    all_sprites.add(sliceatis)

            slices = pygame.sprite.spritecollide(player, durians, True, pygame.sprite.collide_circle)
            for slice in slices:
                if (life > 0):
                    slice_sound.play()
                    starttime = currenttime
                    endtime = currenttime + 10
                    slicedurian = durianSlice(slice.rect.center, 'nm')
                    all_sprites.add(slicedurian)

            slices = pygame.sprite.spritecollide(player, mangoes, True, pygame.sprite.collide_circle)
            for slice in slices:
                if (life > 0):
                    slice_sound.play()
                    score += (5 * multiplier)
                    if multiplier == 1:
                        slicemango = mangoSlice(slice.rect.center, 'nm')
                    if multiplier == 2:
                        slicemango = mangox2Slice(slice.rect.center, 'nm')
                    all_sprites.add(slicemango)


            slices = pygame.sprite.spritecollide(player, bombs, True, pygame.sprite.collide_circle)
            
            for slice in slices:
                if (life > 0):
                    bomb_sound.play()
                    pygame.mixer.music.pause()
                    life = 0
                 
             
         


            #set the font style and size
            myFont = pygame.font.SysFont('Agent Orange', 25)
            myFont2 = pygame.font.SysFont('Agent Orange', 35)
            myFont3 = pygame.font.SysFont('Agent Orange', 37)



            if life == 0:
                screenstatus = 5
                lasttimeout = currenttime

           
            #background image
            screen.blit(MainGameFrame.image, MainGameFrame.rect)

            

            if life > 0:
                #life label
                GOsurf = myFont.render('Life', True, WHITE)
                GOrect = GOsurf.get_rect()
                GOrect.midtop = (60, 15)
                screen.blit(GOsurf,GOrect)

                # #time label
                # GOsurf = myFont2.render('%s'%currenttime, True, WHITE)
                # GOrect = GOsurf.get_rect()
                # GOrect.midtop = (640, 10)
                # screen.blit(GOsurf,GOrect)

                #score label
                GOsurf = myFont.render('Score: ', True, WHITE)
                GOrect = GOsurf.get_rect()
                GOrect.midtop = (1060, 15)
                screen.blit(GOsurf,GOrect)

                GOsurf = myFont3.render('%s'%score, True, GREEN)
                GOrect = GOsurf.get_rect()
                GOrect.midtop = (1210, 10)
                screen.blit(GOsurf,GOrect)


                


                 #Bonus multiplier label label
                if multiplier == 2:
              

                    if endtime - currenttime == 10:
                        screen.blit(Time10.image, Time10.rect)
                    if endtime - currenttime == 9:
                        screen.blit(Time9.image, Time9.rect)
                    if endtime - currenttime == 8:
                        screen.blit(Time8.image, Time8.rect)
                    if endtime - currenttime == 7:
                        screen.blit(Time7.image, Time7.rect)
                    if endtime - currenttime == 6:
                        screen.blit(Time6.image, Time6.rect)
                    if endtime - currenttime == 5:
                        screen.blit(Time5.image, Time5.rect)
                    if endtime - currenttime == 4:
                        screen.blit(Time4.image, Time4.rect)
                    if endtime - currenttime == 3:
                        screen.blit(Time3.image, Time3.rect)
                    if endtime - currenttime == 2:
                        screen.blit(Time2.image, Time2.rect)
                    if endtime - currenttime == 1:
                        screen.blit(Time1.image, Time1.rect)

            



            #heart image

            if life == 5:
                screen.blit(Heart5.image, Heart5.rect)
            if life >= 4:
                screen.blit(Heart4.image, Heart4.rect)
            if life >= 3:
                screen.blit(Heart3.image, Heart3.rect)
            if life >= 2:
                screen.blit(Heart2.image, Heart2.rect)
            if life >= 1:
                screen.blit(Heart1.image, Heart1.rect)
            #end code for main game

        if screenstatus == 2: #2 for score screen
        #codes
            screen.blit(ScoreMenu.image, ScoreMenu.rect)

            pomeloes = pygame.sprite.Group() 
            mangosteens = pygame.sprite.Group() 
            papayas = pygame.sprite.Group() 
            mangoes = pygame.sprite.Group() 
            durians = pygame.sprite.Group() 
            bombs = pygame.sprite.Group()
            atises = pygame.sprite.Group() 
            all_sprites = pygame.sprite.Group()
            yesButtonQuits = pygame.sprite.Group()
            noButtonQuits = pygame.sprite.Group()
            PlayButtons = pygame.sprite.Group()
            HelpButtons = pygame.sprite.Group()
            ScoreButtons = pygame.sprite.Group()
            AboutButtons = pygame.sprite.Group()
            ExitButtons = pygame.sprite.Group()

            

            ExitButtons = pygame.sprite.Group()
            BackButtonScores = pygame.sprite.Group()


   
            backButtonScore = BackButtonScore()
            all_sprites.add(backButtonScore)
            BackButtonScores.add(backButtonScore)



            SubmitButtons = pygame.sprite.Group()
            DeleteButtons = pygame.sprite.Group()

            slices = pygame.sprite.spritecollide(player, BackButtonScores, False, pygame.sprite.collide_circle)
            for slice in slices:
                screenstatus = 0


            scoresfrom = []
            with open("scores.txt") as f:
                for line in f:
                    namex, scorex = line.split(',')
                    scorex = int(scorex)
                    scoresfrom.append((namex, scorex))

            scoresfrom.sort(key=lambda s: s[1])

            length = len(scoresfrom)

            if length >= 4:
                first = scoresfrom[length-1]
                second = scoresfrom[length-2]
                third = scoresfrom[length-3]

            if length == 3:
                first = scoresfrom[length-1]
                second = scoresfrom[length-2]
                third = ""

            if length == 2:
                first = scoresfrom[length-1]
                second = ""
                third = ""

            if length == 1 or line == "":
                first = ""
                second = ""
                third = ""

            print(first)
            print(second)
            print(third)



            scoreFontStyle = pygame.font.SysFont('Agent Orange', 25)
            GOsurf = scoreFontStyle.render("Top Three Highest Scores", True, WHITE)
            GOrect = GOsurf.get_rect()
            GOrect.midtop = (619, 175)
            screen.blit(GOsurf,GOrect)

            scoreFontStyle = pygame.font.SysFont('Agent Orange', 25)
            GOsurf = scoreFontStyle.render("%s %s" %(first[0], first[1]), True, WHITE)
            GOrect = GOsurf.get_rect()
            GOrect.midtop = (619, 245)
            screen.blit(GOsurf,GOrect)


            scoreFontStyle = pygame.font.SysFont('Agent Orange', 25)
            GOsurf = scoreFontStyle.render("%s %s" %(second[0], second[1]), True, WHITE)
            GOrect = GOsurf.get_rect()
            GOrect.midtop = (619, 346)
            screen.blit(GOsurf,GOrect)

            scoreFontStyle = pygame.font.SysFont('Agent Orange', 25)
            GOsurf = scoreFontStyle.render("%s %s" %(third[0], third[1]), True, WHITE)
            GOrect = GOsurf.get_rect()
            GOrect.midtop = (619, 447)
            screen.blit(GOsurf,GOrect)
         

            
                

            all_sprites.draw(screen)
            all_sprites.update()

        if screenstatus == 3: #6 for about
        #codes
            screen.blit(HelpScreen.image, HelpScreen.rect)

            pomeloes = pygame.sprite.Group() 
            mangosteens = pygame.sprite.Group() 
            papayas = pygame.sprite.Group() 
            mangoes = pygame.sprite.Group() 
            durians = pygame.sprite.Group() 
            bombs = pygame.sprite.Group()
            atises = pygame.sprite.Group() 
            all_sprites = pygame.sprite.Group()
            yesButtonQuits = pygame.sprite.Group()
            noButtonQuits = pygame.sprite.Group()
            PlayButtons = pygame.sprite.Group()
            HelpButtons = pygame.sprite.Group()
            ScoreButtons = pygame.sprite.Group()
            AboutButtons = pygame.sprite.Group()
            ExitButtons = pygame.sprite.Group()
            backButtonHelps = pygame.sprite.Group()
   

            helpButtonAbout = BackButtonHelp()
            all_sprites.add(helpButtonAbout)
            backButtonHelps.add(helpButtonAbout)

            slices = pygame.sprite.spritecollide(player, backButtonHelps, False, pygame.sprite.collide_circle)
            for slice in slices:
                screenstatus = 0

            
            all_sprites.draw(screen)
            all_sprites.update()

            
        if screenstatus == 4: #quit Game
            screen.blit(QuitGame.image, QuitGame.rect)

            pomeloes = pygame.sprite.Group() 
            mangosteens = pygame.sprite.Group() 
            papayas = pygame.sprite.Group() 
            mangoes = pygame.sprite.Group() 
            durians = pygame.sprite.Group() 
            bombs = pygame.sprite.Group()
            atises = pygame.sprite.Group() 
            all_sprites = pygame.sprite.Group()
            yesButtonQuits = pygame.sprite.Group()
            noButtonQuits = pygame.sprite.Group()
            PlayButtons = pygame.sprite.Group()
            HelpButtons = pygame.sprite.Group()
            ScoreButtons = pygame.sprite.Group()
            AboutButtons = pygame.sprite.Group()
            ExitButtons = pygame.sprite.Group()
   
            yesButtonQuit = YesButtonQuit()
            all_sprites.add(yesButtonQuit)
            yesButtonQuits.add(yesButtonQuit)

            noButtonQuit = NoButtonQuit()
            all_sprites.add(noButtonQuit)
            noButtonQuits.add(noButtonQuit)

            slices = pygame.sprite.spritecollide(player, yesButtonQuits, False, pygame.sprite.collide_circle)
            for slice in slices:
                endGame = False

            slices = pygame.sprite.spritecollide(player, noButtonQuits, False, pygame.sprite.collide_circle)
            for slice in slices:
                screenstatus = 0


            
            all_sprites.draw(screen)
            all_sprites.update()
           

        if screenstatus == 5: #5 for game over
        #gameover

            counter = 0
            currenttime = 0
            speed = 25

            if isentername == 1:
                with open("scores.txt", "a") as text_file:
                    text_file.write("%s, %s\n" % (name, score))
                screenstatus = 7
                

            pomeloes = pygame.sprite.Group() 
            mangosteens = pygame.sprite.Group() 
            papayas = pygame.sprite.Group() 
            mangoes = pygame.sprite.Group() 
            durians = pygame.sprite.Group() 
            bombs = pygame.sprite.Group()
            atises = pygame.sprite.Group() 
            all_sprites = pygame.sprite.Group()
            yesButtonQuits = pygame.sprite.Group()
            noButtonQuits = pygame.sprite.Group()
            PlayButtons = pygame.sprite.Group()
            HelpButtons = pygame.sprite.Group()
            ScoreButtons = pygame.sprite.Group()
            AboutButtons = pygame.sprite.Group()
            ExitButtons = pygame.sprite.Group()

            




            SubmitButtons = pygame.sprite.Group()
        

            screen.blit(GameOver.image, GameOver.rect)
            
            starttime = 0
            endtime = 0
            pygame.mixer.music.pause()

            if name != "":
                submitButton = SubmitButton()
                all_sprites.add(submitButton)
                SubmitButtons.add(submitButton)

        

            #codes for the keyboard
            #process input events
            for event in pygame.event.get():
                if event.type == KEYUP:
                    
                    if len(name) < 10:
                        if event.key == K_a:
                            name += 'A'
                        if event.key == K_b:
                            name += 'B'
                        if event.key == K_c:
                            name += 'C'
                        if event.key == K_d:
                            name += 'D'
                        if event.key == K_e:
                            name += 'E'
                        if event.key == K_f:
                            name += 'F'
                        if event.key == K_g:
                            name += 'G'
                        if event.key == K_h:
                            name += 'H'
                        if event.key == K_i:
                            name += 'I'
                        if event.key == K_j:
                            name += 'J'
                        if event.key == K_k:
                            name += 'K'
                        if event.key == K_l:
                            name += 'L'
                        if event.key == K_m:
                            name += 'M'
                        if event.key == K_n:
                            name += 'N'
                        if event.key == K_o:
                            name += 'O'
                        if event.key == K_p:
                            name += 'P'
                        if event.key == K_q:
                            name += 'Q'
                        if event.key == K_r:
                            name += 'R'
                        if event.key == K_s:
                            name += 'S'
                        if event.key == K_t:
                            name += 'T'
                        if event.key == K_u:
                            name += 'U'
                        if event.key == K_v:
                            name += 'V'
                        if event.key == K_w:
                            name += 'W'
                        if event.key == K_x:
                            name += 'X'
                        if event.key == K_y:
                            name += 'Y'
                        if event.key == K_z:
                            name += 'Z'
                        if event.key == K_SPACE:
                            name += ' '


                    if event.key == K_BACKSPACE:
                        name = name[:-1]

              

            
                

            slices = pygame.sprite.spritecollide(player, SubmitButtons, True, pygame.sprite.collide_circle)
            for slice in slices:
                with open("scores.txt", "a") as text_file:
                    text_file.write("%s, %s\n" % (name, score))
                    screenstatus = 7
                    isentername = 1
          

            if gotTime == False:
                finalTime = currenttime
                gotTime = True

            #display game over
            myFont1 = pygame.font.SysFont('Agent Orange', 40)
            myFontScoreandTime = pygame.font.SysFont('Agent Orange', 55)
            
            #display score

            GOsurf = myFont1.render('SCORE:', True, BLACK)
            GOrect = GOsurf.get_rect()
            GOrect.midtop = (395, 250)
            screen.blit(GOsurf,GOrect)


            GOsurf = myFontScoreandTime.render('%s'%score, True, GREEN)
            GOrect = GOsurf.get_rect()
            GOrect.midtop = (590, 240)
            screen.blit(GOsurf,GOrect)

            #display name
            
            GOsurf = myFont1.render('%s'%name, True, RED)
            GOrect = GOsurf.get_rect()
            GOrect.midtop = (490, 410)
            screen.blit(GOsurf,GOrect)

            #display sprites
            all_sprites.draw(screen)
            all_sprites.update()

        if screenstatus == 6: #6 for about
        #codes
            screen.blit(AboutScreen.image, AboutScreen.rect)

            pomeloes = pygame.sprite.Group() 
            mangosteens = pygame.sprite.Group() 
            papayas = pygame.sprite.Group() 
            mangoes = pygame.sprite.Group() 
            durians = pygame.sprite.Group() 
            bombs = pygame.sprite.Group()
            atises = pygame.sprite.Group() 
            all_sprites = pygame.sprite.Group()
            yesButtonQuits = pygame.sprite.Group()
            noButtonQuits = pygame.sprite.Group()
            PlayButtons = pygame.sprite.Group()
            HelpButtons = pygame.sprite.Group()
            ScoreButtons = pygame.sprite.Group()
            AboutButtons = pygame.sprite.Group()
            ExitButtons = pygame.sprite.Group()
            backButtonAbouts = pygame.sprite.Group()
   

            backButtonAbout = BackButtonAbout()
            all_sprites.add(backButtonAbout)
            backButtonAbouts.add(backButtonAbout)

            slices = pygame.sprite.spritecollide(player, backButtonAbouts, False, pygame.sprite.collide_circle)
            for slice in slices:
                screenstatus = 0

            
            all_sprites.draw(screen)
            all_sprites.update()

        if screenstatus == 7: #7 for do you want to play again
        #codes

            counter = 0
            currenttime = 0
            speed = 25
            

            screen.blit(DoYouWantToAgainPlayBackground.image, DoYouWantToAgainPlayBackground.rect)

            pomeloes = pygame.sprite.Group() 
            mangosteens = pygame.sprite.Group() 
            papayas = pygame.sprite.Group() 
            mangoes = pygame.sprite.Group() 
            durians = pygame.sprite.Group() 
            bombs = pygame.sprite.Group()
            atises = pygame.sprite.Group() 
            all_sprites = pygame.sprite.Group()
            YesButtonQuitTrys = pygame.sprite.Group()
            noButtonQuitsTrys = pygame.sprite.Group()
            PlayButtons = pygame.sprite.Group()
            HelpButtons = pygame.sprite.Group()
            ScoreButtons = pygame.sprite.Group()
            AboutButtons = pygame.sprite.Group()
            ExitButtons = pygame.sprite.Group()
            noButtonQuitTrys = pygame.sprite.Group()
            YesButtonQuitTrys = pygame.sprite.Group()

            noButtonQuitTry = NoButtonQuitTry()
            all_sprites.add(noButtonQuitTry)
            noButtonQuitTrys.add(noButtonQuitTry)

            yesButtonQuitTry = YesButtonQuitTry()
            all_sprites.add(yesButtonQuitTry)
            YesButtonQuitTrys.add(yesButtonQuitTry)

            slices = pygame.sprite.spritecollide(player, YesButtonQuitTrys, False, pygame.sprite.collide_circle)
            for slice in slices:
                pomeloes = pygame.sprite.Group() 
                mangosteens = pygame.sprite.Group() 
                papayas = pygame.sprite.Group() 
                mangoes = pygame.sprite.Group() 
                durians = pygame.sprite.Group() 
                bombs = pygame.sprite.Group()
                atises = pygame.sprite.Group() 
                all_sprites = pygame.sprite.Group()
                YesButtonQuitTrys = pygame.sprite.Group()
                noButtonQuitsTrys = pygame.sprite.Group()
                PlayButtons = pygame.sprite.Group()
                HelpButtons = pygame.sprite.Group()
                ScoreButtons = pygame.sprite.Group()
                AboutButtons = pygame.sprite.Group()
                ExitButtons = pygame.sprite.Group()
                noButtonQuitTrys = pygame.sprite.Group()
                YesButtonQuitTrys = pygame.sprite.Group()
                score = 0
                life = 5

                lasttimeout = currenttime
                screenstatus = 1
                

            slices = pygame.sprite.spritecollide(player, noButtonQuitTrys, False, pygame.sprite.collide_circle)
            for slice in slices:
                pomeloes = pygame.sprite.Group() 
                mangosteens = pygame.sprite.Group() 
                papayas = pygame.sprite.Group() 
                mangoes = pygame.sprite.Group() 
                durians = pygame.sprite.Group() 
                bombs = pygame.sprite.Group()
                atises = pygame.sprite.Group() 
                all_sprites = pygame.sprite.Group()
                YesButtonQuitTrys = pygame.sprite.Group()
                noButtonQuitsTrys = pygame.sprite.Group()
                PlayButtons = pygame.sprite.Group()
                HelpButtons = pygame.sprite.Group()
                ScoreButtons = pygame.sprite.Group()
                AboutButtons = pygame.sprite.Group()
                ExitButtons = pygame.sprite.Group()
                noButtonQuitTrys = pygame.sprite.Group()
                YesButtonQuitTrys = pygame.sprite.Group()
                screenstatus = 0
                score = 0
                name = ""
                life = 5

            
            all_sprites.draw(screen)
            all_sprites.update()



##########################################################################################

        #display sword
        screen.blit(player.image, player.rect)


    #START CODE FOR THE DISPLAY OF SPRITES AND WEBCAM
        pygame.display.flip()

         #this flips the webcam like a mirror
        frame = np.rot90(frame,1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0,0))
            
except (KeyboardInterrupt, SystemExit):
    pygame.quit()
    
# When everything done, release the capture
device.release()
cv2.destroyAllWindows()


