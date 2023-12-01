import pygame as pg

class UI:
    def __init__(self,surface):
        self.display_surf = surface
        self.health_bar = pg.image.load("../graphics/ui/heartbar.png").convert_alpha()
        #____[prob need to adjust these nums later]_____
        self.health_bar_topleft = (30,20)
        self.bar_max_width = 100
        self.bar_height = 4
        
        self.coin = pg.image.load("../graphics/ui/coin1.png").convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50,61))
        self.font = pg.font.Font('../graphics/ui/font1/Mario64.ttf',25)

    def show_health(self,current,full):
        self.display_surf.blit(self.health_bar,(20,10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pg.Rect((self.health_bar_topleft),(current_bar_width,self.bar_height))
        pg.draw.rect(self.display_surf,'Red',health_bar_rect)
    def show_coins(self,amount):
        self.display_surf.blit(self.coin,self.coin_rect)
        coin_amount_surface = self.font.render(str(amount),False,'Black')
        coin_amount_rect = coin_amount_surface.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surf.blit(coin_amount_surface,coin_amount_rect)        
