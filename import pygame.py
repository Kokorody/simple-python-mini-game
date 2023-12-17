import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Plane Shooting Game with Timer, Score-based Difficulty, and Enemy Bullets")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

player_width, player_height = 50, 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 5
player_shoot_cooldown = 0.5  
last_shoot_time = pygame.time.get_ticks()

try:
    player_image = pygame.image.load("f22.png")
    player_image = pygame.transform.scale(player_image, (player_width, player_height))
except pygame.error as e:
    print(f"Error loading player image: {e}")
    pygame.quit()
    sys.exit()

enemy_width, enemy_height = 50, 50
enemy_speed = 3
max_enemy_speed = 10
score_to_max_speed = 2000
enemies = []

try:
    enemy_image = pygame.image.load("mig29.png")
    enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))
except pygame.error as e:
    print(f"Error loading enemy image: {e}")
    pygame.quit()
    sys.exit()

bullet_width, bullet_height = 5, 15
bullet_speed = 7
player_bullets = []
enemy_bullets = []

try:
    background_image = pygame.image.load("sky.jpg")
    background_image = pygame.transform.scale(background_image, (width, height))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    pygame.quit()
    sys.exit()

start_time = 30  
current_time = start_time
timer_last_updated = pygame.time.get_ticks()  

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

score = 0

def update_timer():
    global current_time, timer_last_updated

    now = pygame.time.get_ticks()

    if now - timer_last_updated >= 1000:
        current_time -= 1
        timer_last_updated = now

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < height - player_height:
        player_y += player_speed

    if keys[pygame.K_SPACE]:
        now = pygame.time.get_ticks()
        if now - last_shoot_time > player_shoot_cooldown * 1000:
            bullet_x = player_x + player_width // 2 - bullet_width // 2
            bullet_y = player_y
            player_bullets.append([bullet_x, bullet_y])
            last_shoot_time = now

    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > height:
            enemies.remove(enemy)
            score += 1

    for bullet in player_bullets:
        for enemy in enemies:
            if (
                bullet[0] < enemy[0] + enemy_width
                and bullet[0] + bullet_width > enemy[0]
                and bullet[1] < enemy[1] + enemy_height
                and bullet[1] + bullet_height > enemy[1]
            ):
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                current_time += 2

    for bullet in player_bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            player_bullets.remove(bullet)

    if random.randint(0, 100) < 2:
        enemy_x = random.randint(0, width - enemy_width)
        enemies.append([enemy_x, 0])

    update_timer()

    if current_time <= 0:
        print("Game Over! Your final score:", score)
        pygame.quit()
        sys.exit()

    enemy_speed = min(max_enemy_speed, 3 + score // score_to_max_speed)

    for enemy in enemies:
        if random.randint(0, 100) < 2:
            enemy_bullet_x = enemy[0] + enemy_width // 2 - bullet_width // 2
            enemy_bullet_y = enemy[1] + enemy_height
            enemy_bullets.append([enemy_bullet_x, enemy_bullet_y])

    for bullet in enemy_bullets:
        bullet[1] += bullet_speed
        if bullet[1] > height:
            enemy_bullets.remove(bullet)

    for bullet in enemy_bullets:
        if (
            bullet[0] < player_x + player_width
            and bullet[0] + bullet_width > player_x
            and bullet[1] < player_y + player_height
            and bullet[1] + bullet_height > player_y
        ):
            print("Game Over! Your final score:", score)
            pygame.quit()
            sys.exit()

    screen.fill(black)

    screen.blit(background_image, (0, 0))

    screen.blit(player_image, (player_x, player_y))

    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))

    for bullet in player_bullets:
        pygame.draw.rect(screen, white, [bullet[0], bullet[1], bullet_width, bullet_height])

    for bullet in enemy_bullets:
        pygame.draw.rect(screen, green, [bullet[0], bullet[1], bullet_width, bullet_height])

    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    timer_text = font.render(f"Time: {current_time}", True, white)
    screen.blit(timer_text, (width - 150, 10))

    pygame.display.flip()

#  frame rate (higher than 60 fps may broke the game XD)
    clock.tick(60)
 