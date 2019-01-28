'''
Created on Jan 7, 2019

@author: hyobo
'''
import pygame
from optparse import Option
pygame.init()
pygame.font.init() ##Initialize text
game_display = pygame.display.set_mode((1000,700)) ##creating the game window
pygame.display.set_caption("Space Invaders") ##naming the game window

player_ship = pygame.image.load("resources/images/player.png")  ##loading up the image of the player ship
player_ship = pygame.transform.scale(player_ship, (50, 50)) ##resizing the image of the player ship to be 50 pixels by 50 pixels
bg = pygame.image.load("resources/images/background.png")
bg = pygame.transform.scale(bg, (1000,700))
enemy_ship = pygame.image.load("resources/images/alien.png")
enemy_ship = pygame.transform.scale(enemy_ship, (50, 50))
explosion = pygame.image.load("resources/images/explosion.png")
explosion = pygame.transform.scale(explosion, (50,50))

class character(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        
    def draw(self, win):
        ##draws the character onto the game display
        win.blit(player_ship, (self.x,self.y))
            
class projectile(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y 
        self.width = width 
        self.height = height 
        self.vel = vel
        
        
    def draw(self, win):
        pygame.draw.rect(win, (255,255,255), (self.x, self.y, self.width, self.height))
        
class enemy_alien(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y 
        self.width = width 
        self.height = height 
        self.vel = vel
        self.has_shot = False
        
    def draw(self, win):
        win.blit(enemy_ship, (self.x, self.y))

    def hit(self, win):
        ##Draws an explosion to demonstrate that the enemy has been hit 
        win.blit(explosion, (self.x, self.y))
        pygame.display.update()
        pygame.time.delay(50)
         

def update_display():
    #clears the screen and redraws every object for every frame
    game_display.blit(bg, (0,0))
    player.draw(game_display)
    for bullet in bullets:
        bullet.draw(game_display)
    for bullet in enemy_bullets:
        bullet.draw(game_display)
    for enemy in enemies:
        enemy.draw(game_display)
    pygame.draw.line(game_display, (255,0,0), (0, game_display.get_height() - player.height * 2), (game_display.get_width(), game_display.get_height() - player.height * 2)) ##sets the point where aliens can't cross or its game over
    ##Displaying the level the player is on 
    game_font = pygame.font.Font('resources/fonts/INVASION2000.ttf', 40)
    level_display = game_font.render(f'Wave: {wave_count}', False, (255,255,255))  
    game_display.blit(level_display, (game_display.get_width() - 250, 0))       ##display the wave count in the upper right corner of the screen
    pygame.display.update()
    
    

def enemy_group():
    ##Creates a group of 10 enemies side by side
    for enemy_ship in range(10):
        enemies.append(enemy_alien(60 * (enemy_ship + 1), 200, 60, 60, vel))

##Start Menu
game_start = False
main_font = pygame.font.Font('resources/fonts/INVASION2000.ttf', 95) ##initialize the font for the main text as a ttf file in the fonts folder of this game
sub_font = pygame.font.Font('resources/fonts/INVASION2000.ttf', 60) ##initialize font for the subtext
option_font = pygame.font.Font('resources/fonts/INVASION2000.ttf', 40)

while game_start == False: ##While the player hasn't pressed anything to start the game 
    text = main_font.render('SPACE INVADERS', False, (255,255,255))  ##creating the main text
    subtext = sub_font.render('Choose your game mode', False, (255,255,255)) ##creating the sub text
    option1 = option_font.render('Retro', False, (255,255,255))
    option2 = option_font.render('Smooth', False, (255,255,255))
    game_display.blit(bg, (0,0)) ##filling the screen with the background
    game_display.blit(text, (30, 40)) ##drawing the main text onto the screen
    game_display.blit(subtext, (80, 600))
    pygame.draw.rect(game_display, (0,255,127), (100, 300, 200, 100))  ##button for option 1 (retro)
    pygame.draw.rect(game_display, (0, 191, 255), (700, 300, 200, 100)) ##button for option 2 (smooth)
    game_display.blit(option1, (130, 320))  ##Adding text to the two buttons
    game_display.blit(option2, (715, 320))
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  ##if the player presses the close button
            pygame.quit()              ##exit the program

    mouse = pygame.mouse.get_pos()
    if 100 < mouse[0] < 100 + 200 and 300 < mouse[1] < 300 + 100: ##if the mouse is within the bounds of the first button
        pygame.draw.rect(game_display, (0, 128, 0), (100, 300, 200, 100)) ##highlight the button
        game_display.blit(option1, (130, 320)) 
        pygame.display.update()      
        if pygame.mouse.get_pressed()[0]:
            game_start = True
            vel = 30    ##change how fast the game moves based on their choice
            bullet_vel = 40
            delay = 100
                
    if 700 < mouse[0] < 700 + 200 and 300 < mouse[1] < 300 + 100:
        pygame.draw.rect(game_display, (0,0,255), (700, 300, 200, 100))
        game_display.blit(option2, (715, 320))
        pygame.display.update()
        if pygame.mouse.get_pressed()[0]:
            game_start = True
            vel = 10    ##change the speed of the game based on their choice
            bullet_vel = 15
            delay = 10
            
        
#Main Loop
try_again = True
while try_again == True:     ##loops the game over until the player doesn't want to play anymore
    #Game Loop
    far_right = game_display.get_width() - player_ship.get_width() ##setting the farthest point right the player can go
    bullets = []  #3empty list to hold all the player projectile objects on the screen
    enemy_bullets = []  ##holds the enemy projectile objects
    enemies = []  ##holds the enemy objects
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000) ##set a check to perform a function every 1 second
    wave_count = 0 ##setting the current level/wave the player is on
    player = character(game_display.get_width() / 2, game_display.get_height() - player_ship.get_height(),player_ship.get_width(), player_ship.get_height(), vel)
    #creates a player ship at the middle-bottom of the screen

    end_game = False
    while end_game == False:
        pygame.time.delay(delay)  ##the game updates its frames by a delay chosen by the player (retro vs smooth)
        
        if len(enemies) == 0:    ##if all the enemies have been killed, spawn more
            enemy_group()
            wave_count += 1
        
        for enemy in enemies:  ##for every enemy currently alive 
            if enemy.x < game_display.get_width() - enemy_ship.get_width():    ##if the enemy hasn't reached the end of the screen
                enemy.x += enemy.vel                                           ##move the enemy along by a set velocity 
                
            else:
                enemy.y += enemy_ship.get_height()    ##if the enemy reaches the end of the screen, they go one level lower 
                enemy.x = 60                        
                
            if enemy.y >= player.y - player.height: ##If the enemy passes the line, then its game over
                end_game = True
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game = True
                try_again = False
                
            if event.type == pygame.USEREVENT + 1:  ##for every 1 second
                for enemy in enemies:
                    if enemy.has_shot == True:
                        enemy.has_shot = False   ##if the enemy has already shot, do nothing and move onto the next enemy
                        
                    elif enemy.has_shot == False:
                        enemy.has_shot = True
                        enemy_bullets.append(projectile(enemy.x + enemy_ship.get_width(), enemy.y, 10, 20, bullet_vel))
                        break
        
        for bullet in bullets:  ##for every bullet shot by the user still on the screen
            if bullet.y > 0:  #if the bullet hasnt reached the top of the screen
                bullet.y -= bullet.vel    #move the bullet up
            else:
                bullets.pop(bullets.index(bullet))    ##if the bullet is at the top, remove it from the list of existing bullets
        
            for enemy in enemies:
                if bullet.y < enemy.y + enemy.height and bullet.y + bullet.height > enemy.y: ##if the bullet touches the bottom of the enemy's hitbox
                    if bullet.x > enemy.x and bullet.x + bullet.width < enemy.x + enemy.width:
                        enemy.hit(game_display)  ##make the explosion effect
                        bullets.pop(bullets.index(bullet))  ##remove the bullet so that it doesn't hit other enemies
                        enemies.pop(enemies.index(enemy)) ##remove the hit enemy from the list of currently alive enemies
                        
        for bullet in enemy_bullets: ##for every bullet shot by the enemy
            if bullet.y < game_display.get_height(): ##if the bullet hasn't reached the bottom of the screen
                bullet.y += bullet.vel               ##move the bullet down
            else:
                enemy_bullets.pop(enemy_bullets.index(bullet))   ##if the bullet has reached the end of the screen, removew it from the list
                
            if bullet.y < player.y + player.height and bullet.y + bullet.height > player.y:   ##if the bullet is within the player's frame
                if bullet.x > player.x and bullet.x + bullet.width < player.x + player.width:
                    end_game = True 
        
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_SPACE]:  ##if the space key is pressed
            if len(bullets) < 1:
                bullets.append(projectile(player.x + player_ship.get_width() / 2, player.y, 10, 20, bullet_vel)) #creates a bullet object centered on the player and puts it in the list of bullets 

        elif keys[pygame.K_LEFT] and player.x != 0:  ##if the player moves left and isn't at the end of the screen
            player.x -= player.vel
            
        elif keys[pygame.K_RIGHT] and player.x != far_right:
            player.x += player.vel
        ##allowing player-inputted movement and setting boundaries 
        
        update_display()

    ##Game Over Screen
    if event.type != pygame.QUIT:   ##If the player closes the window out, don't show the game over screen
        text = main_font.render('GAME OVER', False, (255,255,255))
        try_again_text = option_font.render('Press any button to try again', False, (255,255,255))
        game_display.blit(bg, (0,0))
        game_display.blit(text, (200, 300)) ##display the text in white
        game_display.blit(try_again_text, (160, 600))
        pygame.display.update()
        pygame.time.delay(1500) ##set a delay so the player doesn't accidently restart the game
        try_again = False ##makes it so that the game won't restart automatically
        while try_again == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: ##if the user presses any key
                    try_again = True    ##repeat the whole game loop
                                        ##if the player doesn't do anything, nothing happens

                elif event.type == pygame.QUIT:
                    pygame.quit()