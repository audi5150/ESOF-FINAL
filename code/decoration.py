import pygame as pg
from settings import sc_wid,tile_size,vertical_tile_num
from support import import_folder
from random import choice,randint
from tiles import StaticTile


class Sky:
    def __init__(self,horizon,style = 'level'):
        #self.top = pg.image.load('../graphics/sky/blsktop.png').convert()
        #self.bottom = pg.image.load('../graphics/sky/bottom.png').convert()
        #self.mid = pg.image.load('../graphics/sky/blskymid.png').convert()
        self.lvl = pg.image.load('../graphics/sky/bg/bg.png').convert()
        self.horizon = horizon
        #self.top = pg.transform.scale(self.top,(sc_wid,tile_size))
        #self.bottom = pg.transform.scale(self.bottom,(sc_wid,tile_size))
        #self.mid = pg.transform.scale(self.mid,(sc_wid,tile_size))
        self.oworld = pg.image.load('../graphics/sky/bg/bg6.png').convert()
        self.lvl1 = pg.image.load('../graphics/sky/bg/bg5.png').convert()
        self.style = style
      
        """
        if self.style == 'overworld':
            star_surfaces = import_folder('../graphics/clouds/')
            self.stars = []
            for surface in [choice(star_surfaces)for image in range(30)]:
                x = randint(0,sc_wid)
                y = (self.horizon * tile_size) + randint(50,100)
                rect = surface.get_rect(midbottom = (x,y))
                self.stars.append((surface,rect))
        if self.style == 'level':
            star_surfaces = import_folder('../graphics/clouds/')
            self.stars = []
            for surface in [choice(star_surfaces)for image in range(15)]:
                x = randint(0,sc_wid)
                y = (self.horizon * tile_size) + randint(75,100)
                rect = surface.get_rect(midbottom = (x,y))
                self.stars.append((surface,rect))
            """

    def draw(self,surface):
        if self.style == 'overworld':
            self.image = self.oworld
        if self.style == 'level':
            self.image = self.lvl

        surface.blit(self.image,(0,0))
##        for row in range(vertical_tile_num):
##            y = row * tile_size
##            if row < self.horizon:
##                surface.blit(self.top,(0,y))
##            elif row == self.horizon:
##                surface.blit(self.mid,(0,y))
##            else:
##                surface.blit(self.bottom,(0,y))
##        if self.style == 'overworld':
##            for star in self.stars:
##                
##                surface.blit(star[0],star[1])
##        if self.style == 'level':
##            for star in self.stars:
##                surface.blit(star[0],star[1])
                
                
"""        
class Clouds:
    def __init__(self,horizon,level_width,cloud_num):
        cloud_surf_list = import_folder('../graphics/clouds/')
        min_x = -sc_wid
        max_x = level_width + sc_wid
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pg.sprite.Group()
        for cloud in range(cloud_num):
            cloud = choice(cloud_surf_list)
            x = randint(min_x,max_x)
            y = randint(min_y,max_y)
            sprite = StaticTile(0,x,y,cloud_surf)
            self.cloud_sprites.add(sprite)
    def draw(self,surface,shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
"""
