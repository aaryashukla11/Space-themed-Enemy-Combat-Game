import math
import random

import pygame
from pygame import mixer
pygame.init()

#create the screen
screen=pygame.display.set_mode((800,600))

#sound
mixer.music.load("images\\background.wav")
mixer.music.play(-1)

#caption and icon
pygame.display.set_caption("My Space Game")
icon=pygame.image.load("images\\ufo.png")
pygame.display.set_icon(icon)

background=pygame.image.load("images\\backgr.png")

#player
playerimg=pygame.image.load("images\\player.png")
playerX=370
playerY=480
player_change=0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images\\enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)




bulletimg=pygame.image.load("images\\bullet.png")
bulletX=370
bulletY=480
bullet_changeX=0
bullet_changeY=20
bullet_state="ready"

#score
score_value=0
font=pygame.font.Font("freesansbold.ttf",32)

#textX=10
#textY=10

#Gameover
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score=font.render("Score :" + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerimg,(x,y))#here blits means draw

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def bullet(x,y):
    screen.blit(bulletimg,(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletimg,(x+15,y+10))

def iscollision(enemyX,enemyY,bulletX, bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX, 2)+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

#gameloop
running=True
while running:
    screen.fill((193,118,171))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                player_change=-1
            if event.key == pygame.K_RIGHT:
                player_change=1
            if event.key==pygame.K_SPACE:
                if bullet_state=='ready':
                    bulletSound=mixer.Sound("images\laser.wav");
                    bulletSound.play()
                    bulletX=playerX
                    fire_bullet(playerX,bulletY)

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                player_change=0

    if playerX<=0:
        playerX=0
    if playerX>=740:
        playerX=740
    playerX = playerX + player_change

    #enemymovement
    for i in range(num_of_enemies):
        #game over
        if enemyY[i] >440:
            for j in range(num_of_enemies):
                enemyY[j] =2000
            game_over_text()
            show_score(playerX+250,bulletY+50)
            break
        enemyX[i] = enemyX[i] + enemyX_change[i]

        if enemyX[i] <=0:

             enemyX_change[i] =2
             enemyY[i]+=enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] =-2
            enemyY[i] += enemyY_change[i]

        #collision
        if iscollision(enemyX[i],enemyY[i],bulletX,bulletY):
            explosionSound=mixer.Sound("images\\explosion.wav")
            explosionSound.play()
            bulletY=480
            bullet_state="ready"
            score_value+=1
            enemyX[i]=random.randint(0,736)
            enemyY[i]=random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)


    #bullett movement
    if bulletY<=0:
        bulletY=480
        bullet_state='ready'

    if bullet_state=="fire":
        fire_bullet(playerX,bulletY)
        bulletY-=bullet_changeY


    bullet(playerX + 10, playerY + 10)
    player(playerX,playerY)
    pygame.display.update()


