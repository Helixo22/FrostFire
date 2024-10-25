import pygame
import math
import random
import json
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frostfire")


WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)


bg_image = pygame.image.load("bg.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (100, 100))

bomb_image = pygame.image.load("bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (60, 60))

xp_texture = pygame.image.load("xp.png")
xp_texture = pygame.transform.scale(xp_texture, (70, 70))


player_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 80, 80)

bullets = []
recoil_speed = 0
recoil_direction = 0
recoil_duration = 0
player_speed = 5
player_velocity = [0, 0]
gravity = 0.2


max_clip_size = 10
bullets_in_clip = max_clip_size
reload_time = 1
last_reload_time = pygame.time.get_ticks()


lives = 3
invulnerable = False
invulnerability_time = 2000
last_hit_time = 0


record_file = 'highscore.json'
try:
    with open(record_file, 'r') as file:
        highscore = json.load(file).get('highscore', 0)
except FileNotFoundError:
    highscore = 0

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 10, 20)
        self.direction = direction
        self.speed = 10

    def update(self):
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

    def draw(self):

        pygame.draw.ellipse(screen, YELLOW, self.rect)

def calculate_angle(player_rect, target_pos):
    dx = target_pos[0] - player_rect.centerx
    dy = target_pos[1] - player_rect.centery
    return math.atan2(dy, dx)

def draw_arrow(player_pos, target_pos):
    angle = calculate_angle(player_pos, target_pos)
    length = 50
    end_pos = (player_pos.centerx + int(length * math.cos(angle)),
               player_pos.centery + int(length * math.sin(angle)))
    pygame.draw.line(screen, WHITE, player_pos.center, end_pos, 5)
    arrowhead_angle1 = angle + math.pi / 6
    arrowhead_angle2 = angle - math.pi / 6
    pygame.draw.line(screen, WHITE, end_pos, (end_pos[0] - 10 * math.cos(arrowhead_angle1), end_pos[1] - 10 * math.sin(arrowhead_angle1)), 3)
    pygame.draw.line(screen, WHITE, end_pos, (end_pos[0] - 10 * math.cos(arrowhead_angle2), end_pos[1] - 10 * math.sin(arrowhead_angle2)), 3)

class Ball:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = 0
        self.radius = random.randint(20, 50)
        self.is_purple = random.choice([True, False])
        self.speed = random.randint(5, 10)
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

    def draw(self):
        if self.is_purple:

            screen.blit(xp_texture, self.rect)
        else:

            screen.blit(bomb_image, self.rect)

    def is_dangerous(self):
        return not self.is_purple

def check_collision(ball, bullet):
    return ball.rect.colliderect(bullet.rect)

def check_player_collision(ball, player_rect):
    return ball.rect.colliderect(player_rect)

def draw_button(text, position, width, height):
    font = pygame.font.SysFont(None, 36)
    button_rect = pygame.Rect(position[0], position[1], width, height)
    pygame.draw.rect(screen, WHITE, button_rect)
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (position[0] + (width - text_surface.get_width()) // 2, position[1] + (height - text_surface.get_height()) // 2))
    return button_rect

def save_highscore(score):
    with open(record_file, 'w') as file:
        json.dump({'highscore': score}, file)

def draw_clip_bar():
    """Disegna una barra di caricamento che mostra i colpi rimasti (in verticale)."""
    bar_height = 100
    bar_width = 10
    bar_x = player_rect.x + player_rect.width + 10
    bar_y = player_rect.y


    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))


    fill_height = int((bullets_in_clip / max_clip_size) * bar_height)
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y + (bar_height - fill_height), bar_width, fill_height))

balls = []
ball_spawn_time = 0

running = True
clock = pygame.time.Clock()
score = 0
player_alive = True

while running:

    screen.blit(bg_image, (0, 0))

    if pygame.time.get_ticks() - ball_spawn_time > 1000 and len(balls) < 5:
        balls.append(Ball())
        ball_spawn_time = pygame.time.get_ticks()

    for ball in balls[:]:
        ball.update()
        ball.draw()
        if ball.y > HEIGHT:
            balls.remove(ball)


        if check_player_collision(ball, player_rect) and not invulnerable:
            if ball.is_dangerous():

                lives -= 1
                invulnerable = True
                last_hit_time = pygame.time.get_ticks()
                if lives <= 0:
                    player_alive = False
            else:
                score += 1
                balls.remove(ball)


    if invulnerable and pygame.time.get_ticks() - last_hit_time > invulnerability_time:
        invulnerable = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if player_alive and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and bullets_in_clip > 0:
                angle = calculate_angle(player_rect, pygame.mouse.get_pos())
                bullets.append(Bullet(player_rect.centerx, player_rect.centery, angle))
                recoil_direction = angle + math.pi
                recoil_speed = 12
                recoil_duration = 6
                bullets_in_clip -= 1


        if not player_alive and event.type == pygame.MOUSEBUTTONDOWN:
            if retry_button.collidepoint(event.pos):

                player_rect.center = (WIDTH // 2, HEIGHT // 2)
                balls.clear()
                bullets.clear()
                score = 0
                bullets_in_clip = max_clip_size
                lives = 3
                invulnerable = False
                player_alive = True


    if pygame.time.get_ticks() - last_reload_time >= reload_time * 1000 and bullets_in_clip < max_clip_size:
        bullets_in_clip += 1
        last_reload_time = pygame.time.get_ticks()

    if recoil_duration > 0:
        player_velocity[0] = int(recoil_speed * math.cos(recoil_direction) * 0.6)
        player_velocity[1] = int(recoil_speed * math.sin(recoil_direction) * 0.6)
        recoil_duration -= 1
    else:

        player_velocity[1] += gravity


    player_rect.x += player_velocity[0]
    player_rect.y += player_velocity[1]


    if player_rect.left < 0:
        player_rect.right = WIDTH
    elif player_rect.right > WIDTH:
        player_rect.left = 0
    if player_rect.top < 0:
        player_rect.bottom = HEIGHT
    elif player_rect.bottom > HEIGHT:
        player_rect.top = 0

    draw_arrow(player_rect, pygame.mouse.get_pos())

    for bullet in bullets[:]:
        bullet.update()
        bullet.draw()

        for ball in balls[:]:
            if check_collision(ball, bullet):
                if not ball.is_dangerous():
                    score += 1
                balls.remove(ball)
                bullets.remove(bullet)
                break

        if bullet.rect.x < 0 or bullet.rect.x > WIDTH or bullet.rect.y < 0 or bullet.rect.y > HEIGHT:
            bullets.remove(bullet)

    if player_alive:

        screen.blit(player_image, player_rect.topleft)
    else:
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))


        if score > highscore:
            highscore = score
            save_highscore(highscore)


        retry_button = draw_button("Retry", (WIDTH // 2 - 50, HEIGHT // 2 + 50), 100, 50)


    font = pygame.font.SysFont(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 150, 10))

    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}  Highscore: {highscore}", True, WHITE)
    screen.blit(score_text, (10, 10))


    draw_clip_bar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
