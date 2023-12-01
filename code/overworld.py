import pygame as pg
from game_data import levels
from support import import_folder
from decoration import Sky
 

class Node(pg.sprite.Sprite):
    def __init__(self,pos,status,icon_speed,path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index =0
        self.image = self.frames[self.frame_index]
        self.image = pg.Surface((32,32))
        if status == 'available':
            #self.image.fill('Red')
            self.status = 'available'
        else:
            #self.image.fill('Grey')
            self.status = 'locked'
        self.rect = self.image.get_rect(center = (pos))

        self.detection_zone = pg.Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed,icon_speed)
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('Red',None,pg.BLEND_RGBA_MULT)
            self.image.blit(tint_surf,(0,0))
        
class Icon(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pg.Surface((20,20))
        #self.image.fill('Blue')
        self.image = pg.image.load("../graphics/overworld_graphics/stand.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.center = self.pos
        
class Overworld:
    def __init__(self,start_level,max_level,surface,create_level):
        #______________________________[setup]___________
        self.display_surf = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        #_____________________________[movement_logic]_____
        self.moving = False
        self.move_direction = pg.math.Vector2(0,0)
        self.speed = 8
        #_____________________________[sprites]__________
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky (20,'overworld')
       # self.clouds = Clouds(400,level_width,20)
        
    def setup_nodes(self):
        self.nodes = pg.sprite.Group()
        
        for index,node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'],'available',self.speed,node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'],'locked',self.speed,node_data['node_graphics'])
            self.nodes.add(node_sprite)
    def setup_icon(self):
        self.icon = pg.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)
        
    def draw_paths(self):
        if self.max_level > 0 :
            points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level]
            pg.draw.lines(self.display_surf,'LightBlue',False,points,6)
            
    def input(self):
        keys = pg.key.get_pressed()
        if not  self.moving:
            if keys[pg.K_RIGHT]and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pg.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pg.K_SPACE]:
                self.create_level(self.current_level)
                
    def get_movement_data(self,target):
        start = pg.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pg.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pg.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        return (end - start).normalize()
    
    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pg.math.Vector2(0,0)
        
    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()
        self.sky.draw(self.display_surf)
        #self.clouds.draw(self.display_surf)
        self.draw_paths()
        self.nodes.draw(self.display_surf)
        self.icon.draw(self.display_surf)
        
