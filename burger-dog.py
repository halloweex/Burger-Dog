import random

import pygame
from random import randint

# initialize pygame
pygame.init()

# set display surface
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 3
NORMAL_VELOCITY = 5
BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = .5
BUFFER_DISTANCE = 100

score = 0
burger_points = 0
burger_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = NORMAL_VELOCITY

boost_level = STARTING_BOOST_LEVEL

burger_velocity = STARTING_BURGER_VELOCITY

# Set colors
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
ORANGE = (246, 170, 54)
ORANGE_2 = pygame.Color('orange')

# Set fonts
font = pygame.font.Font('WashYourHand.ttf', 32)

# Set text
points_text = font.render("Burger Points: " + str(burger_points), True, ORANGE)
points_rect = points_text.get_rect()
points_rect.topleft = (10, 10)

score_text = font.render("Score: " + str(score), True, ORANGE_2)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 50)

title_text = font.render("Burger Dog", True, ORANGE)
title_rect = title_text.get_rect()
title_rect.center = (WINDOW_WIDTH // 2, 20)

eaten_text = font.render("Burger Eaten: " + str(burger_eaten), True, ORANGE)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = (WINDOW_WIDTH // 2)
eaten_rect.centery = 60

lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH - 10, 50)

game_over_text = font.render("FINAL SCORE: " + str(score), True, ORANGE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

continue_text = font.render("Press any key to play again", True, ORANGE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Set sounds and musics
bark_sound = pygame.mixer.Sound('sounds/bark_sound.wav')
miss_sound = pygame.mixer.Sound('sounds/miss_sound.wav')
pygame.mixer.music.load("sounds/bd_background_music.wav")

# Set images
dog_left = pygame.image.load("img/dog_left.png")
dog_right = pygame.image.load("img/dog_right.png")

player_image = dog_left
player_rect = player_image.get_rect()
player_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 64)

burger_image = pygame.image.load("img/burger.png")
burger_rect = burger_image.get_rect()
burger_rect.topleft = (randint(0, WINDOW_WIDTH - 32), -BUFFER_DISTANCE)

# the main game loop
pygame.mixer.music.play()
pygame.mixer.music.set_volume(.1)
running = True
while running:
    # check to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_image = dog_left
    if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += player_velocity
        player_image = dog_right
    if keys[pygame.K_UP] and player_rect.top > 100:
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity

    # Engage Boost
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = NORMAL_VELOCITY

    # Move the burger and update burger points
    burger_rect.y += burger_velocity
    burger_points = int(burger_velocity * (WINDOW_HEIGHT - burger_rect.y + 100))

    # Player missed the burger
    if burger_rect.y > WINDOW_HEIGHT:
        player_lives -= 1
        miss_sound.play()

        burger_rect.topleft = (random.randint(0, WINDOW_HEIGHT - 32), -BUFFER_DISTANCE)
        burger_velocity = STARTING_BURGER_VELOCITY

        player_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 64)
        boost_level = STARTING_BOOST_LEVEL

    # Collision
    if player_rect.colliderect(burger_rect):
        score += burger_points
        burger_eaten += 1
        bark_sound.play()

        burger_rect.topleft = (random.randint(0, WINDOW_HEIGHT - 32), -BUFFER_DISTANCE)
        burger_velocity += BURGER_ACCELERATION

        boost_level += 25
        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL

    # Update the HUD
    points_text = font.render("Burger Points: " + str(burger_points), True, ORANGE)
    score_text = font.render("Score: " + str(score), True, ORANGE_2)
    eaten_text = font.render("Burger Eaten: " + str(burger_eaten), True, ORANGE)
    lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
    boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)

    # Check for game over
    if player_lives == 0:
        game_over_text = font.render("Final Score: " + str(score), True, ORANGE)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until the player presses a key, then reset the game
        pygame.mixer.music.stop()
        is_pause = True
        while is_pause:
            for event in pygame.event.get():
                # The player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    burger_eaten = 0
                    player_lives = PLAYER_STARTING_LIVES
                    burger_velocity = STARTING_BURGER_VELOCITY
                    boost_level = STARTING_BOOST_LEVEL

                    pygame.mixer.music.play()
                    is_pause = False
                # The player wants to quit
                if event.type == pygame.QUIT:
                    running = False
                    is_pause = False

    # Fill the screen
    screen.fill(BLACK)

    # Blit the HUD
    screen.blit(points_text, points_rect)
    screen.blit(score_text, score_rect)
    screen.blit(title_text, title_rect)
    screen.blit(eaten_text, eaten_rect)
    screen.blit(lives_text, lives_rect)
    screen.blit(boost_text, boost_rect)
    pygame.draw.line(screen, WHITE, (0, 100), (800, 100), 5)

    # Blit assets
    screen.blit(burger_image, burger_rect)
    screen.blit(player_image, player_rect)

    # Update screen and set FPS
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
