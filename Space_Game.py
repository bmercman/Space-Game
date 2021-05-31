# import libraries
import pygame as pg
from pygame import mixer
import sys
import random
import math
pg.font.init()

# Basics
pg.init()
clock = pg.time.Clock()

# Game Screen
screen_width = 1600
screen_height = 900
screen = pg.display.set_mode((screen_width, screen_height))

# Background
bkg = pg.image.load("Assets/background.png").convert()

# Background Music
mixer.music.load("Assets/Quarantine.wav")
mixer.music.play(-1)

class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.sprites = []
        self.sprites.append(pg.image.load("Assets/Player_ship.png"))
        self.sprites.append(pg.image.load("Assets/Player_ship_2.png"))
        self.sprites.append(pg.image.load("Assets/Player_ship_3.png"))
        self.sprites.append(pg.image.load("Assets/Player_ship_4.png"))
        self.sprites.append(pg.image.load("Assets/Player_ship_5.png"))
        self.sprites.append(pg.image.load("Assets/Player_ship_4.png"))
        self.sprites.append(pg.image.load("Assets/Player_ship_3.png"))
        self.sprites.append(pg.image.load("Assets/Player_ship_2.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center = (800, 700))

    def update(self, pos_x, pos_y):
        # animate sprite
        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        # change sprite position
        self.rect.center = (pos_x, pos_y)

    def create_bullet(self, pos_x, pos_y):
        return Bullet(pos_x, pos_y)


class Bullet(pg.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pg.image.load("Assets/blast.png")
        self.rect = self.image.get_rect(center = (pos_x, pos_y))

    def update(self):
        self.rect.y += -4
        # destroy off screen bullets
        if self.rect.y <= -1:
            self.kill()


class Alien(pg.sprite.Sprite):

    def __init__(self, rand_x, rand_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pg.image.load("Assets/Alien_1.png"))
        self.sprites.append(pg.image.load("Assets/Alien_2.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [rand_x, rand_y]


    def update(self, vel):
        # animate sprite
        self.current_sprite += 0.05

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        # move aleins
        self.rect.y += vel
        # destroy off screen aliens
        if self.rect.y >= 950:
            self.kill()

    # returns x-coordinate
    def get_x(self):
        return self.rect.x

    # returns y-coordinate
    def get_y(self):
        return self.rect.y

def main():

    # Background
    bkg_y = 0

    # Player
    player_x = 800
    player_y = 700

    player = Player()
    player_group = pg.sprite.Group()
    player_group.add(player)

    # Bullet
    bullet_group = pg.sprite.Group()

    # Alien
    enemies = []
    wave_length = 0
    vel = 1
    alien_group = pg.sprite.Group()

    # Player score variables
    run = True
    lives = 1
    score = 0
    wave = 0
    lost = False
    lost_count = 0
    main_font = pg.font.SysFont("comicsans", 50)
    lost_font = pg.font.SysFont("comicsans", 80)


    # Game loop
    while run:

        # FPS - game run speed
        clock.tick(120)

        # adds enemies to enemies list
        if len(enemies) == 0:
            wave += 1
            if wave_length == 8:
                vel = 1.5
            if wave_length <= 8:
                wave_length += 2
            for i in range(wave_length):
                enemy = Alien(random.randint(50, 1550), random.randint(-1500, -100))
                enemies.append(enemy)

        # catches events
        for event in pg.event.get():
            # if game is quit, quit program
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # space bar shoots bullet & ESC exits game
            if event.type == pg.KEYDOWN:
                # space shoots bullet
                if event.key == pg.K_SPACE:
                    bullet_group.add(player.create_bullet(player_x, player_y))
                    bullet_sound = mixer.Sound("Assets/laser.wav")
                    bullet_sound.play()
                # ESC exits game
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

        # if key pressed, check which key
        userInput = pg.key.get_pressed()

        # up arrow
        if userInput[pg.K_UP] and player_y >= 50:
            player_y += -4.0
        # down arrow
        if userInput[pg.K_DOWN] and player_y <= 850:
            player_y += 4.0
        # left arrow
        if userInput[pg.K_LEFT] and player_x >= 50:
            player_x += -10.0
        # right arrow
        if userInput[pg.K_RIGHT] and player_x <= 1550:
            player_x += 10.0

        # end game
        if lives <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > 120 * 5:
                run = False
            else:
                continue

        # Draws Screen
        pg.display.flip()
        # parallax background
        rel_y = bkg_y % bkg.get_rect().height
        screen.blit(bkg, (0, rel_y - bkg.get_rect().height))
        # appends new background to create loop when end of image reached
        if rel_y < screen_height:
            screen.blit(bkg, (0, rel_y))
        # moves background, changes y coordinate
        bkg_y += 2
        # Draw Player Sprite & bullet
        bullet_group.draw(screen)
        player_group.draw(screen)
        # Draw Alien enemies
        for enemy in enemies:
            alien_group.add(enemy)
            alien_group.draw(screen)
            # check to see if alien hit bullet
            if pg.sprite.spritecollide(enemy, bullet_group, True):
                enemy.kill()
                enemies.remove(enemy)
                score += 100
                if score % 5000 == 0:
                    lives += 1
            # checks to see if alien hit player
            if pg.sprite.spritecollide(enemy, player_group, False):
                enemy.kill()
                enemies.remove(enemy)
                lives -= 1
            # removes life & enemy if enemy gets to bottom
            if enemy.get_y() >= 900:
                lives -= 1
                enemies.remove(enemy)
        # Draw text
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        wave_label = main_font.render(f"Wave: {wave}", 1, (255, 255, 255))
        screen.blit(score_label, (10, 10))
        screen.blit(lives_label, (10, 50))
        screen.blit(wave_label, (1600 - wave_label.get_width() - 10, 10))
        # Game Ends
        if lives <= 0:
            lost_label = lost_font.render("GAME OVER", 1, (255, 0, 0))
            screen.blit(lost_label, (screen_width / 2 - lost_label.get_width() / 2, 450))
        # player movement & bullet movement
        player_group.update(player_x, player_y)
        bullet_group.update()
        # alien movement
        alien_group.update(vel)
        # update background
        pg.display.update()

def main_menu():

    run = True
    title_font = pg.font.SysFont("comicsans", 70)
    sub_font = pg.font.SysFont("comicsans", 30)

    while run:
        # catches events
        for event in pg.event.get():
            # if game is quit, quit program
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # space bar starts game & ESC exits game
            if event.type == pg.KEYDOWN:
                # start game
                if event.key == pg.K_SPACE:
                    main()
                # ESC exits game
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

        # Draw screen
        pg.display.flip()
        screen.blit(bkg, (0, 0))
        # Label
        title_label = title_font.render("Everything Not Saved Will Be Lost", 1, (252, 3, 169))
        sub_label = sub_font.render("Press SPACE to begin...", 1, (255, 255, 255))
        screen.blit(title_label, (screen_width / 2 - title_label.get_width() / 2, 450))
        screen.blit(sub_label, (screen_width / 2 - sub_label.get_width() / 2, 700))

main_menu()