import random

import pygame

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

# Set fps and clock
FPS = 60
clock = pygame.time.Clock()

# Set colors
WHITE = (255, 255, 255)
ORANGE = (246, 170, 54)
BLACK = (0, 0, 0)

# Game Values
BURGER_STARTING_POINTS = 0
score = 0
burgers_eaten = 0
is_boosted = False

PLAYER_STARTING_LIVES = 3
BOOST_AMOUNT = 100

PLAYER_VELOCITY = 7
PLAYER_BOOST_VELOCITY = 3

BURGER_STARTING_VELOCITY = 3
BURGER_ACCELERATION = .25

burger_points = BURGER_STARTING_POINTS
player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_VELOCITY
boost_level = BOOST_AMOUNT

burger_velocity = BURGER_STARTING_VELOCITY

# Set text
font = pygame.font.Font("WashYourHand.ttf", 32)

burger_points_text = font.render("Burger Points: " + str(burger_points), True, ORANGE)
burger_points_rect = burger_points_text.get_rect()
burger_points_rect.topleft = (10, 10)

score_text = font.render("Score: " + str(score), True, ORANGE)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 50)

title_text = font.render("Burger Dog", True, ORANGE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH // 2
title_rect.y = 10

lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

burgers_eaten_text = font.render("Burgers Eaten: " + str(burgers_eaten), True, ORANGE)
burgers_eaten_rect = burgers_eaten_text.get_rect()
burgers_eaten_rect.centerx = WINDOW_WIDTH // 2
burgers_eaten_rect.y = 50

boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH - 10, 50)

game_over_text = font.render("FINAL SCORE: " + str(score), True, ORANGE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("Press any key to play again", True, ORANGE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

# Set images
player_image_right = pygame.image.load('dog_right.png')
player_image_left = pygame.image.load('dog_left.png')
player_image = player_image_left
player_rect = player_image.get_rect()
player_rect.centerx = WINDOW_WIDTH // 2
player_rect.bottom = WINDOW_HEIGHT
player_direction = "Left"

burger_image = pygame.image.load("burger.png")
burger_rect = burger_image.get_rect()
BUFFER_DISTANCE = 100
burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -BUFFER_DISTANCE)

# Set Sounds
bark_sound = pygame.mixer.Sound("bark_sound.wav")
miss_sound = pygame.mixer.Sound("miss_sound.wav")
pygame.mixer.music.load("bd_background_music.wav")
bark_sound.set_volume(.2)

running = True
pygame.mixer.music.play(-1, 0, 0)

while running:
    display_surface.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(FPS)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_direction = "Left"
        player_rect.x -= player_velocity
    if keys[pygame.K_RIGHT]:
        player_direction = "Right"
        player_rect.x += player_velocity
    if keys[pygame.K_DOWN]:
        player_rect.y += player_velocity
    if keys[pygame.K_UP]:
        player_rect.y -= player_velocity

    player_normal_velocity = player_velocity

    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity += PLAYER_BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = PLAYER_VELOCITY

    if player_rect.left <= 0:
        player_rect.left = 0
    if player_rect.right >= WINDOW_WIDTH:
        player_rect.right = WINDOW_WIDTH
    if player_rect.top <= 0:
        player_rect.top = 0
    if player_rect.bottom >= WINDOW_HEIGHT:
        player_rect.bottom = WINDOW_HEIGHT

    burger_points = int(burger_velocity*(WINDOW_HEIGHT - burger_rect.y))
    burger_rect.y += burger_velocity
    burger_points -= 3

    if burger_rect.colliderect(player_rect):
        score += burger_points
        bark_sound.play()
        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -BUFFER_DISTANCE)
        boost_level = BOOST_AMOUNT
        burger_velocity += BURGER_ACCELERATION
        burgers_eaten += 1


    if burger_rect.y > WINDOW_HEIGHT:
        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -BUFFER_DISTANCE)
        miss_sound.play()
        player_lives -= 1
        burger_velocity = BURGER_STARTING_VELOCITY
        player_rect.center = (WINDOW_WIDTH // 2,WINDOW_HEIGHT)
        boost_level = BOOST_AMOUNT

    burger_points_text = font.render("Burger Points: " + str(burger_points), True, ORANGE)
    score_text = font.render("Score: " + str(score), True, ORANGE)
    lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
    burgers_eaten_text = font.render("Burgers Eaten: " + str(burgers_eaten), True, ORANGE)
    boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)

    display_surface.blit(burger_points_text, burger_points_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(burgers_eaten_text, burgers_eaten_rect)
    display_surface.blit(boost_text, boost_rect)

    if player_direction == "Left":
        display_surface.blit(player_image_left, player_rect)
    if player_direction == "Right":
        display_surface.blit(player_image_right, player_rect)



    display_surface.blit(burger_image, burger_rect)

    pygame.draw.line(display_surface, WHITE, (0, 100), (WINDOW_WIDTH, 100), 3)
    pygame.display.update()

    if player_lives == 0:
        is_paused = True
        pygame.mixer.music.stop()
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    is_paused = False
                    break
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    burger_velocity = BURGER_STARTING_VELOCITY
                    burgers_eaten = 0
                    burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -BUFFER_DISTANCE)
                    pygame.mixer.music.play(-1,0.0)
                    is_paused = False
                    break

pygame.quit()
