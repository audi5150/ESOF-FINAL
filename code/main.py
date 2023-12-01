import pygame as pg
import sys
from settings import *
from level import Level
from game_data import levels
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0
#__________________________[audio]_______

        self.level_bg_music = pg.mixer.Sound('../audio/ground_theme.mp3')
        self.overworld_bg_music = pg.mixer.Sound('../audio/overworld_theme.mp3')
        self.overworld_bg_music.set_volume(0.05)
        #self.game_over_sound = pg.mixer.Sound('../audio/effects/smb_gameover.wav')
#_____________________________________[overworld creation]__________
        self.overworld = Overworld(0,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1)
#______[ui]___
        self.ui = UI(screen)
        
        
    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)
    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops= -1)
        self.level_bg_music.stop()
    def change_coins(self,amount):
        self.coins += amount
    def change_health(self,amount):
        self.current_health += amount
    def check_game_over(self):
        if self.current_health <=0:
            self.level_bg_music.stop()
            self.overworld_bg_music.play()
            self.current_health =100
            self.coins =0
            self.max_level=0
            self.overworld = Overworld(0,self.max_level,screen,self.create_level)
            self.status = 'overworld'
          
            
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health,self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

pg.init()
 
#bg = pg.image.load('../graphics/sky/bg.png').convert_alpha()
screen = pg.display.set_mode((sc_wid,sc_hei))
clock = pg.time.Clock()
game = Game()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
    screen.fill('LightBlue')
    game.run()
  
    pg.display.update()
    clock.tick(60)
 
