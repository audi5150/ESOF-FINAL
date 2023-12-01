import pygame as pg
from support import import_csv_layout,import_cut_graphics
from settings import tile_size,sc_wid,sc_hei
from tiles import Tile,StaticTile,AnimatedTile,Coin
from player import Player
from enemy import Enemy
from game_data import levels
from decoration import Sky

class Level:
    def __init__(self,current_level,surface,create_overworld,change_coins,change_health):
        #__________________________[gen setup]______
        self.display_surf = surface
        self.world_shift = 0
        self.current_x = None
        #_____________________________[audio]_________
        self.coin_sound = pg.mixer.Sound('../audio/effects/smb_coin.wav')
        self.stomp_sound = pg.mixer.Sound('../audio/effects/smb_stomp.wav')
        #_____________________________________[overworld connection]________
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']
        #__________________________________________________[player_layout]_____
        player_layout = import_csv_layout(level_data['player'])
        self.player = pg.sprite.GroupSingle()
        self.goal = pg.sprite.GroupSingle()
        self.player_setup(player_layout,change_health)
        #_________________________________[user interface]_______________
        self.change_coins = change_coins
        #__[terrain_setup]____
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
        green_layout =import_csv_layout(level_data['green'])
        self.green_sprites = self.create_tile_group(green_layout,'green')
        #__[coin_layout]_____
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')
        #____[enemy]____
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprite = self.create_tile_group(enemy_layout,'enemies')
        #____[constraint]____
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')
        self.sky = Sky(13,'level')
      
        
    def create_tile_group(self,layout,type):
        sprite_group = pg.sprite.Group()
#____[rowindex is y position of tiles
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type == 'green':
                        green_tile_list = import_cut_graphics('../graphics/tilesets/00THIS_ONE.png')
                        tile_surf = green_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surf)
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/tilesets/00THIS_ONE.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type == 'coins':
                        sprite = Coin(tile_size,x,y,'../graphics/coins')
                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)
                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)
                  
                        
                    

                    sprite_group.add(sprite)
                
        return sprite_group
    def box_collision(self):
        box_collisions =pg.sprite.spritecollide(self.player.sprite,self.box_sprite,False)
        if box_collisions:
            for box in box_collisions:
                box_center = box.rect.centery
                box_bottom = box.rect.bottom
                player_top = self.player.sprite.rect.top
                if box_bottom > player_top> box_center and self.player.sprite.direction.y >=1:
                    self.animate()
                    
    def player_setup(self,layout,change_health):
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                pos = (x,y)
                if val == '0':
                  sprite = Player(pos,change_health)
                  self.player.add(sprite)
                if val == '1':
                    end_surf = pg.image.load("../graphics/tilesets/pend.png").convert_alpha()
                    sprite = StaticTile(tile_size,x,y,end_surf)
                    self.goal.add(sprite)
     
                    
                    
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprite.sprites():
            if pg.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()

    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        #_____[collision for left/right, place character on the surf
        #___[for other collisions, boxes etc add + and call the self.sprites
        collidable_sprites = self.terrain_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0 :
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
        
    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y =0
                    player.on_ground = True
                elif player.direction.y < 0 :
                    player.rect.top = sprite.rect.bottom
                    player.direction.y =0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y <0 or player.direction.y >0:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < sc_wid /4 and direction_x < 0:
            self.world_shift = 8
            player.speed =0
        elif player_x > sc_wid -(sc_wid /4) and direction_x >0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift =0
            player.speed = 8
    def check_death(self):
        if self.player.sprite.rect.top > sc_hei:
            self.create_overworld(self.current_level,0)

    def check_win(self):
        if pg.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.create_overworld(self.current_level,self.new_max_level)
    def check_coin_collisions(self):
        collided_coins = pg.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(1)
    def check_enemy_collisions(self):
        enemy_collisions =pg.sprite.spritecollide(self.player.sprite,self.enemy_sprite,False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >=1:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -15
                    enemy.kill()
            
                else:  
                    self.player.sprite.get_damage()

    def lvl_0(self):
        if self.current_level == levels[0]:
            Sky.lvl_0()

    def run(self):
        self.sky.draw(self.display_surf)
        
        #self.clouds.draw(self.display_surf,self.world_shift)
        self.green_sprites.update(self.world_shift)
        self.green_sprites.draw(self.display_surf)
        
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surf)
     
        
        self.enemy_sprite.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprite.draw(self.display_surf)
           

        
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surf)
        
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surf)
       

        self.player.update()
        self.player.draw(self.display_surf)
        self.check_death()
        self.check_win()
        self.horizontal_collision()
        self.vertical_collision()
        self.scroll_x()
        
        self.check_coin_collisions()
        self.check_enemy_collisions()
