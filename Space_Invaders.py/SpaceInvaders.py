'''
Created on Jan 7, 2019

@author: hself.yobo
'''
import pygame
pygame.init()

game_display = pygame.display.set_mode((1000,700)) ##creating the game window
pygame.display.set_caption("Space Invaders") ##naming the game window

player_ship = pygame.image.load("images/player.png")  ##loading up the image of the player ship
player_ship = pygame.transform.scale(player_ship, (50, 50)) ##resizing the image of the player ship to be 50 pixels by 50 pixels
bg = pygame.image.load("images/background.png")
bg = pygame.transform.scale(bg, (1000,700))

print(player_ship.get_height())
print(game_display.get_height())

class character(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        
    def draw(self, win):
        ##draws the character onto the game display
        win.blit(player_ship, (self.x,self.y))
            
class projectile(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y 
        self.width = width 
        self.height = height 
        self.vel = 40
        
    def draw(self, win):
        pygame.draw.rect(win, (255,255,255), (self.x, self.y, self.width, self.height))

def update_display():
    #clears the screen and redraws the player every frame
    game_display.blit(bg, (0,0))
    player.draw(game_display)
    for bullet in bullets:
        bullet.draw(game_display)
    pygame.display.update()
    
    
player = character(game_display.get_width() / 2, game_display.get_height() - player_ship.get_height(),50,50)
#creates a player ship at the middle-bottom of the screen


#Main Loop
far_up = 500 ##setting the y boundary for the player, the farthest point up they can go in the window
far_right = game_display.get_width() - player_ship.get_width() ##setting the farthest point right the player can go
low_down = game_display.get_height() - player_ship.get_height() ##setting the farthest point downward the player can go
bullets = []

end_game = False
while end_game == False:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True
    
    for bullet in bullets:
        if bullet.y > 0:
            bullet.y -= bullet.vel    
        else:
            bullets.pop(bullets.index(bullet))    
    
    keys = pygame.key.get_pressed()
    
    
    if keys[pygame.K_SPACE]:
        if len(bullets) < 1:
            bullets.append(projectile(player.x + player_ship.get_width() / 2, player.y, 10, 20)) #creates a 10x20 bullet centered on the ship 
    
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]: ##if the player moves diagonally and isn't at a boundary, move a specified amount
        if player.x != 0 and player.y != far_up:
            player.x -= player.vel
            player.y -= player.vel
        
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        if player.x != 0 and player.y != low_down:
            player.x -= player.vel
            player.y += player.vel
    
    elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        if player.x != far_right and player.y != far_up:
            player.x += player.vel
            player.y -= player.vel
        
    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        if player.x != far_right and player.y != low_down:
            player.x += player.vel
            player.y += player.vel
    
    elif keys[pygame.K_LEFT] and player.x != 0:
        player.x -= player.vel
        
    elif keys[pygame.K_RIGHT] and player.x != far_right:
        player.x += player.vel
        
    elif keys[pygame.K_UP] and player.y != far_up:
        player.y -= player.vel
        
    elif keys[pygame.K_DOWN] and player.y != low_down:
        player.y += player.vel
    ##allowing player-inputted movement and setting boundaries 
    
    update_display()
    
    
    