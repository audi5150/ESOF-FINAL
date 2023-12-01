import pygame as pg
from support import import_folder
from math import sin


class Player(pg.sprite.Sprite):
    def __init__(self,pos,change_health):
        super().__init__()
        self.import_char_assets()
        self.frame_index =0
        self.animation_speed = 0.15
        #self.status = 'walk'
        #self.image = self.animations['walk'][self.frame_index]
        #self.image = pg.image.load("stand.png").convert_alpha()
        self.image = self.animations['idle'][self.frame_index]
        self.image.set_colorkey('LightBlue')
        self.rect = self.image.get_rect(topleft = (pos))
#______________________________________________________[movement]______
        self.direction = pg.math.Vector2(0,0)
        self.speed =8
        self.gravity = 0.8
        self.jump_speed = -16
#_______________________________________[playerstatus]___________________
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
#______________________________________________[health management]_________
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 300
        self.hurt_time = 0
#_____________________________________________[sounds]__________
        self.jump_sound = pg.mixer.Sound('../audio/effects/smb_jump-small.wav')
        #self.hit_sound = pg.mixer.Sound('../audio/effects/hit.wav')
    def import_char_assets(self):
        char_path = '../graphics/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}
        for animation in self.animations.keys():
            full_path = char_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index =0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_img = pg.transform.flip(image,True,False)
            self.image = flipped_img
            self.image.set_colorkey('Black')
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
            
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

            
        
    def get_input(self):
        k = pg.key.get_pressed()
        if k[pg.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif k[pg.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x =0
        if k[pg.K_SPACE] and self.on_ground:
            self.jump()
            
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1 :
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
        return self.status
            
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()
    def get_damage(self):
        if not self.invincible:
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pg.time.get_ticks()
    def invincibility_timer(self):
        if self.invincible:
            current_time = pg.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
        
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.invincibility_timer()
        self.wave_value()
        
        

            
       
    
