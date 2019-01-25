'''
Created on Jan 7, 2019

@author: hyobo
'''
import pygame
pygame.init()

game_display = pygame.display.set_mode((1000,700)) ##creating the game window
pygame.display.set_caption("Space Invaders") ##naming the game window

player_ship = pygame.image.load("images/player.png")  ##loading up the image of the player ship
player_ship = pygame.transform.scale(player_ship, (50, 50)) ##resizing the image of the player ship to be 50 pixels by 50 pixels
bg = pygame.image.load("images/background.png")
bg = pygame.transform.scale(bg, (1000,700))
enemy_ship = pygame.image.load("images/alien.png")
enemy_ship = pygame.transform.scale(enemy_ship, (50, 50))
explosion = pygame.image.load("images/explosion.png")
explosion = pygame.transform.scale(explosion, (50,50))

print(player_ship.get_height())
print(game_display.get_height())

class character(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 30
        
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
        
class enemy_alien(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y 
        self.width = width 
        self.height = height 
        self.vel = 10
        
    def draw(self, win):
        win.blit(enemy_ship, (self.x, self.y))

    def hit(self, win):
        win.blit(explosion, (self.x, self.y))
        pygame.display.update()
        pygame.time.delay(50)
         

def update_display():
    #clears the screen and redraws the player every frame
    game_display.blit(bg, (0,0))
    player.draw(game_display)
    for bullet in bullets:
        bullet.draw(game_display)
    for enemy in enemies:
        enemy.draw(game_display)
    pygame.display.update()
    
    

def enemy_group():
    for enemy_ship in range(10):
        enemies.append(enemy_alien(60 * (enemy_ship + 1), 200, 60, 60))
        
    

player = character(game_display.get_width() / 2, game_display.get_height() - player_ship.get_height(),50,50)
#creates a player ship at the middle-bottom of the screen


#Main Loop
far_right = game_display.get_width() - player_ship.get_width() ##setting the farthest point right the player can go
bullets = []
enemies = []

end_game = False
while end_game == False:
    pygame.time.delay(100)
    
    if len(enemies) == 0:    ##if all the enemies have been killed, spawn more
        enemy_group()
    
    for enemy in enemies:  ##for every enemy currently alive 
        if enemy.x < game_display.get_width() - enemy_ship.get_width():    ##if the enemy hasn't reached the end of the screen
            enemy.x += enemy.vel                                           ##move the enemy along by a set velocity 
            
        else:
            enemy.y += enemy_ship.get_height()    ##if the enemy reaches the end of the screen, they go one level lower 
            enemy.x = 60
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True
    
    for bullet in bullets:  ##for every bullet still on the screen

        if bullet.y > 0:  #if the bullet hasnt reached the top of the screen
            bullet.y -= bullet.vel    #move the bullet up
        else:
            bullets.pop(bullets.index(bullet))    ##if the bullet is at the top, make it disappear 
    
        for enemy in enemies:
            if bullet.y < enemy.y + enemy.height and bullet.y + bullet.height > enemy.y: ##if the bullet touches the bottom of the enemy's hitbox
                if bullet.x > enemy.x and bullet.x + bullet.width < enemy.x + enemy.width:
                    enemy.hit(game_display)  ##make the explosion effect
                    bullets.pop(bullets.index(bullet))  ##remove the bullet so that it doesn't hit other enemies
                    enemies.pop(enemies.index(enemy)) ##remove the hit enemy from the list of currently alive enemies
                    
        
    keys = pygame.key.get_pressed()
    
    
    if keys[pygame.K_SPACE]:
        if len(bullets) < 1:
            bullets.append(projectile(player.x + player_ship.get_width() / 2, player.y, 10, 20)) #creates a 10x20 bullet centered on the ship 

    elif keys[pygame.K_LEFT] and player.x != 0:
        player.x -= player.vel
        
    elif keys[pygame.K_RIGHT] and player.x != far_right:
        player.x += player.vel
    ##allowing player-inputted movement and setting boundaries 
    
    update_display()
    
    
    