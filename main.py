import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('space.jpg')

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)
# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# game over
ov = pygame.font.Font('freesansbold.ttf', 32)
# player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
n = 6
for i in range(n):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 760))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)
# bullets
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 3
bulletY_change = 10
bullet_state = "ready"


def game_over_text():
    over = font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over, (250, 250))


def show_score(x, y):
    sc = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(sc, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    dist = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if dist < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((100, 8, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # bullet movement
    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        bulletX = playerX
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    for i in range(n):
        # game over
        if playerY - enemyY[i] < 100 :
            for j in range(n):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        # collision
        col = is_collision(enemyX[i], enemyY[i], bulletX, bulletY )
        if col:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 760)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()


