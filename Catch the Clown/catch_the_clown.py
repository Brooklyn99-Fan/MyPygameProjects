import pygame, random

pygame.init()

WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Clown")

running = True

# Set FPS and Clock
FPS = 60
clock = pygame.time.Clock()

# Set Game Values
PLAYER_STARTING_LIVES = 10
CLOWN_STARTING_VELOCITY = 3
CLOWN_ACCELERATION = .5

player_lives = PLAYER_STARTING_LIVES
score = 0

clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])

# clown2_dx = random.choice([-1,1])
# clown2_dy = random.choice([-1,1])

# Set Colours
BLUE = (1, 175, 209)
YELLOW = (248, 231, 28)
WHITE = (255, 255, 255)

font = pygame.font.Font('Fonts/Franxurter.ttf', 32)

title_text = font.render("Catch the Clown", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (50, 30)

score_text = font.render("Score: " + str(score), True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH - 50, 10)

lives_text = font.render('Lives: ' + str(player_lives), True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 50, 50)

game_over_text = font.render("Game Over", True, BLUE, YELLOW)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("Press any key to continue", True, YELLOW, BLUE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

# Sounds and Music
hit_sound = pygame.mixer.Sound('Sounds/click_sound.wav')
miss_sound = pygame.mixer.Sound('Sounds/miss_sound.wav')

pygame.mixer.music.load('Sounds/ctc_background_music.wav')

# Images
background_image = pygame.image.load('Images/background.png')
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

clown_image = pygame.image.load('Images/clown.png')
clown_rect = clown_image.get_rect()
clown_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# clown_image2 = pygame.image.load('Images/clown.png')
# clown_rect2 = clown_image2.get_rect()
# clown_rect2.center = (WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) + 80 )

pygame.mixer.music.play(-1, 0.0)
hit_sound.set_volume(.1)
miss_sound.set_volume(.2)

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            if clown_rect.collidepoint(mouse_x, mouse_y):
                hit_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                previous_dx = clown_dx
                previous_dy = clown_dy

                while previous_dx == clown_dx and previous_dy == clown_dy:
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

            else:
                miss_sound.play()
                player_lives -= 1

    display_surface.blit(background_image, background_rect)
    display_surface.blit(clown_image, clown_rect)
    # display_surface.blit(clown_image2, clown_rect2)

    # Move the clown
    clown_rect.x += clown_dx * clown_velocity
    clown_rect.y += clown_dy * clown_velocity

    # clown_rect2.x += clown2_dx * clown_velocity
    # clown_rect2.y += clown2_dy * clown_velocity

    if clown_rect.left <= 0 or clown_rect.right >= WINDOW_WIDTH:
        clown_dx *= -1

    if clown_rect.top <= 90 or clown_rect.bottom >= WINDOW_HEIGHT:
        clown_dy *= -1

    score_text = font.render("Score: " + str(score), True, YELLOW)
    lives_text = font.render('Lives: ' + str(player_lives), True, YELLOW)

    # if clown_rect2.left <= 0 or clown_rect2.right >= WINDOW_WIDTH:
    #     clown2_dx *= -1
    #
    # if clown_rect2.top <= 0 or clown_rect2.bottom >= WINDOW_HEIGHT:
    #     clown2_dy *= -1
    #
    # if clown_rect2.colliderect(clown_rect):
    #     clown_dx *= -1
    #     clown_dy *= -1
    #     clown2_dx *= -1
    #     clown2_dy *= -1

    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(score_text, score_rect)

    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        is_paused = True
        pygame.mixer.music.stop()

        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES

                    clown_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                    clown_velocity = CLOWN_STARTING_VELOCITY

                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

                    pygame.mixer.music.play(-1,0.0)

                    is_paused = False
                    break

                if event.type == pygame.QUIT:
                    running = False
                    is_paused = False
                    break

    pygame.draw.line(display_surface, WHITE, (0, 90), (WINDOW_WIDTH, 90))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
