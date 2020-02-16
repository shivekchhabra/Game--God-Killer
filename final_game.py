import pygame
import random
import os
import time
import math

# Initialise pygame
pygame.init()


def rendering_screen():
    # Create the screen
    screen = pygame.display.set_mode((800, 600))
    # screen.fill((0, 25, 0))  # screen color
    background = pygame.image.load('background.png')
    screen.blit(background, (0, 0))
    return screen


def player_details():
    player = pygame.image.load('player.png')
    player_x = 370
    player_y = 480
    return player, player_x, player_y


def enemy_details():
    path = os.getcwd()
    enemies = os.listdir(path + '/enemies')
    enemy_choice = random.choice(enemies)
    enemy = pygame.image.load(path + '/enemies/' + enemy_choice)
    enemy_x = random.randint(0, 736)
    enemy_y = random.randint(20, 100)
    return enemy, enemy_x, enemy_y


def check_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 50:
        return True
    else:
        return False


# ready - not firing
# fire - firing
def bullet_details():
    bullet = pygame.image.load('scythe.png')
    bullet_x = 0
    bullet_y = 480  # same as our player
    return bullet, bullet_x, bullet_y


# For drawing an image on another image.
def player_blitting(screen, player_img, player_x, player_y):
    screen.blit(player_img, (player_x, player_y))


def enemy_blitting(screen, enemy_img, enemy_x, enemy_y):
    screen.blit(enemy_img, (enemy_x, enemy_y))


def bullet_blitting(screen, bullet_img, bullet_x, bullet_y):
    bullet_state = 'fire'
    screen.blit(bullet_img, (bullet_x + 16, bullet_y + 10))
    return bullet_state


def show_score(screen, font, score_val, x, y):
    score = font.render("Score: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over(screen, font, x, y):
    text = font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(text, (x, y))


def game_loop():
    # title and icon
    score = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    score_x = 10
    score_y = 10
    pygame.display.set_caption('God Killer')
    player, player_x, player_y = player_details()
    enemy, enemy_x, enemy_y = enemy_details()
    bullet, bullet_x, bullet_y = bullet_details()
    # Game loop
    bullet_state = 'ready'
    enemyX_change = 10
    bulletY_change = 40
    enemyYchange = 0
    running = True
    while running:
        playerx_change = 0

        screen = rendering_screen()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                print('Score= ', score)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    playerx_change = -40
                if event.key == pygame.K_RIGHT:
                    playerx_change = 40
                if event.key == pygame.K_SPACE:
                    if bullet_state == 'ready':
                        temp_x = player_x
                        bullet_state = bullet_blitting(screen, bullet, temp_x, bullet_y)
        player_x += playerx_change

        if player_x < 0:
            player_x = 0
        if player_x > 736:  # bcoz size of spaceship is 64 pixels
            player_x = 736

        if enemy_x >= 736 or enemy_x < 0:
            enemyX_change = -enemyX_change
            enemyYchange = 3  # diagonally come down on every turn
        enemy_x += enemyX_change
        enemy_y += enemyYchange

        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = 'ready'
        if bullet_state == 'fire':
            bullet_state = bullet_blitting(screen, bullet, temp_x, bullet_y)
            bullet_y -= bulletY_change

        # Checking collision... gotta send player_x value (could have stored in bullet_x)
        collision = check_collision(enemy_x, enemy_y, player_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = 'ready'
            score += 1
            if score % 5 == 0:
                bulletY_change += 10
            enemy, enemy_x, enemy_y = enemy_details()
            enemyX_change += score

        player_blitting(screen, player, player_x, player_y)
        enemy_blitting(screen, enemy, enemy_x, enemy_y)
        show_score(screen, font, score, score_x, score_y)
        if enemy_y >= 400 or enemy_y == player_y:
            game_over(screen, over_font, 200, 250)
            time.sleep(1)
            running = False
            print('Game over, Your score is: ', score)
        pygame.display.update()  # to update the screen (needs to be there to implement any changes)


if __name__ == '__main__':
    game_loop()
