import pygame
import random
import os

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


# For drawing an image on another image.
def player_blitting(screen, player_img, player_x, player_y):
    screen.blit(player_img, (player_x, player_y))


def enemy_blitting(screen, enemy_img, enemy_x, enemy_y):
    screen.blit(enemy_img, (enemy_x, enemy_y))


def game_loop():
    # title and icon
    pygame.display.set_caption('God Killer')
    player, player_x, player_y = player_details()
    enemy, enemy_x, enemy_y = enemy_details()
    # Game loop
    enemyX_change = 7
    enemyYchange = 0
    running = True
    while running:
        playerx_change = 0

        screen = rendering_screen()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    playerx_change = -9
                if event.key == pygame.K_RIGHT:
                    playerx_change = 9
        player_x += playerx_change

        if player_x < 0:
            player_x = 0
        if player_x > 736:  # bcoz size of spaceship is 64 pixels
            player_x = 736

        if enemy_x >= 736 or enemy_x < 0:
            enemyX_change = -enemyX_change
            enemyYchange = 1  # diagonally come down on every turn
        enemy_x += enemyX_change
        enemy_y += enemyYchange
        player_blitting(screen, player, player_x, player_y)
        enemy_blitting(screen, enemy, enemy_x, enemy_y)
        pygame.display.update()  # to update the screen (needs to be there to implement any changes)


if __name__ == '__main__':
    game_loop()
