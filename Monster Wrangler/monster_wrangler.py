import pygame, random
from pygame import mixer

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

FPS = 60
clock = pygame.time.Clock()


class Game():
    def __init__(self, player, monster_group):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        # Set sounds and music
        self.next_level_sound = pygame.mixer.Sound('next_level.wav')
        pygame.mixer.music.load('next_level.wav')

        # Set game values

        # Set Font
        self.font = pygame.font.Font("Abrushow.ttf", 24)

        # Set Images
        blue_image = pygame.image.load('blue_monster.png')
        green_image = pygame.image.load('green_monster.png')
        yellow_image = pygame.image.load('yellow_monster.png')
        purple_image = pygame.image.load('purple_monster.png')

        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]
        # This list corresponds to the monster images order

        self.target_monster_type = random.randint(0, 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH // 2
        self.target_monster_rect.top = 30

    def update(self):
        # self.round_time += 1
        self.frame_count += 1

        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0

        self.check_collisions()

    def draw(self):
        # Set Colors
        WHITE = (255, 255, 255)
        BLUE = (20, 176, 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        colors = [BLUE, GREEN, PURPLE, YELLOW]

        catch_text = self.font.render("Current Catch: ", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH // 2
        catch_rect.top = 5

        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render("Round: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render("Round Time: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, 5)

        warp_text = self.font.render("Warps: " + str(self.player.warps), True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH - 10, 35)

        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warp_text, warp_rect)

        display_surface.blit(self.target_monster_image, self.target_monster_rect)
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (WINDOW_WIDTH // 2 - 32, 30, 64, 64), 2)
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200),4)

    def check_collisions(self):
        # Check for collision and an individual monster, we must test the type of the monster to see if it matches the type of our monster
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)

        if collided_monster:
            if collided_monster.type == self.target_monster_type:
                self.score += 100 * self.round_number
                collided_monster.remove(monster_group)

                if self.monster_group:
                    self.player.catch_sound.play()
                    self.choose_new_target()

                else:
                    self.player.reset()
                    self.start_new_round()

            else:
                self.player.die_sound.play()
                self.player.lives -= 1

                self.player.reset()

            if self.player.lives == 0:
                self.pause_game()
                self.reset_game()

    def start_new_round(self):
        self.score += int(10000 * self.round_number / (1 + self.round_time))
        self.round_number += 1
        self.round_time = 0
        self.frame_count = 0
        self.player.warps += 1

        for monster in self.monster_group:
            self.monster_group.remove(monster)

        for i in range(self.round_number):
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[0], 0))
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[1], 1))
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[2], 2))
            self.monster_group.add(
                Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164),
                        self.target_monster_images[3], 3))

        self.choose_new_target()
        pygame.mixer.music.play()

    def choose_new_target(self):
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image

    def pause_game(self):
        game_over_text = self.font.render("Game Over!", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        continue_text = self.font.render("Press any key to play again", True, (255, 255, 255))
        continue_rect = continue_text.get_rect()
        continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)

        display_surface.fill((0, 0, 0))

        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)


        pygame.display.update()

        pygame.time.delay(1000)

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    is_paused = False
                if event.type == pygame.KEYDOWN:
                    is_paused = False

    def reset_game(self):
        self.score = 0
        self.round_number = 0
        self.player.reset()
        for x in self.monster_group:
            self.monster_group.remove(x)
        self.start_new_round()
        self.player.lives = 5
        self.player.warps = 5


class Player(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()

        self.image = pygame.image.load('knight.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.monster_group = monster_group

        self.lives = 5
        self.warps = 3

        self.velocity = 8

        pygame.mixer.init()
        self.catch_sound = pygame.mixer.Sound('catch.wav')
        self.die_sound = pygame.mixer.Sound('die.wav')
        self.warp_sound = pygame.mixer.Sound('warp.wav')

        self.catch_sound.set_volume(.2)
        self.die_sound.set_volume(.2)

        self.in_game_area = False

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity

        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocity

        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.velocity

    def warp(self):
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()

            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.y = WINDOW_HEIGHT - 64


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, image, monster_type):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Monster_type is an int, 0:Blue 1:Green 2:Purple 3:Yellow
        self.type = monster_type

        self.dx = random.choice([1, -1])
        self.dy = random.choice([1, -1])

        self.velocity = random.randint(1,5)

    def update(self):
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.dx *= -1
        if self.rect.top < 100 or self.rect.bottom > WINDOW_HEIGHT - 100:
            self.dy *= -1


player_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()

player = Player()
player_group.add(player)
game = Game(player, monster_group)
game.start_new_round()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.warp()

    display_surface.fill((0, 0, 0))

    monster_group.draw(display_surface)
    player_group.draw(display_surface)

    monster_group.update()
    player_group.update()

    game.update()
    game.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
