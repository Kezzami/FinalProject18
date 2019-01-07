'''
Created on Jan 7, 2019

@author: hyobo
'''
import pygame
pygame.init()

game_display = pygame.display.set_mode((500,500)) ##creating a window for the game
pygame.display.set_caption("Space Invaders") ##setting the window title

x = 250
y = 490
vel = 10

end_game = False
while end_game == False:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        if x != 0 and y != 350:
            x -= vel
            y -= vel
        
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        if x != 0 and y != 490:
            x -= vel
            y += vel
    
    elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        if x != 490 and y != 350:
            x += vel
            y -= vel
        
    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        if x != 490 and y != 490:
            x += vel
            y += vel
    
    elif keys[pygame.K_LEFT] and x != 0:
        x -= vel
        
    elif keys[pygame.K_RIGHT] and x != 490:
        x += vel
        
    elif keys[pygame.K_UP] and y != 350:
        y -= vel
        
    elif keys[pygame.K_DOWN] and y != 490:
        y += vel
        
    
    game_display.fill((0,0,0))
    pygame.draw.rect(game_display, (255,0,0), (x, y, 10, 10))
    pygame.display.update()
            

pygame.quit()