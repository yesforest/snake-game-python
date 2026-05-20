import pygame
import random
import sys

# Pygame-i başlatmaq
pygame.init()
pygame.font.init()  # Yazılar üçün font sistemini başlatmaq

# Ekran ölçüləri və rənglər
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Python Project:Snake Game")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Oyun sürəti
clock = pygame.time.Clock()
SNAKE_SPEED = 2
BLOCK_SIZE = 20

# Fontlar
font_score = pygame.font.SysFont("Arial", 20)
font_gameover = pygame.font.SysFont("Arial", 40)

def show_score(score):
    value = font_score.render(f"Xal: {score}", True, WHITE)
    screen.blit(value, [10, 10])

def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        text1 = font_gameover.render("OYUN BİTDİ!", True, RED)
        text2 = font_score.render(f"Toplam Xalınız: {score}", True, WHITE)
        text3 = font_score.render("Yenidən başlamaq üçün R, Çıxmaq üçün Q basın", True, GRAY)
        
        screen.blit(text1, [WIDTH // 4, HEIGHT // 4])
        screen.blit(text2, [WIDTH // 4, HEIGHT // 2])
        screen.blit(text3, [WIDTH // 6, HEIGHT // 1.5])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start_game()  # Oyunu yenidən başladır
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def start_game():
    # İlanın başlanğıc bədəni (X koordinatları BLOCK_SIZE qədər fərqlənməlidir)
    snake_pos = [[100, 60], [80, 60], [60, 60]]
    direction = 'RIGHT'
    change_to = direction

    # Yeməyin ilk mövqeyi (Ekran sərhədləri daxilində tam bloklara oturtmaq)
    food_pos = [random.randrange(0, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
                random.randrange(0, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Klaviaturadan ox düymələrini tutmaq
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        # İlanın başının yeni koordinatlarını hesablamaq
        new_head = list(snake_pos[0])
        if direction == 'UP':
            new_head[1] -= BLOCK_SIZE
        if direction == 'DOWN':
            new_head[1] += BLOCK_SIZE
        if direction == 'LEFT':
            new_head[0] -= BLOCK_SIZE
        if direction == 'RIGHT':
            new_head[0] += BLOCK_SIZE

        # Yeni başı ilan bədəninin əvvəlinə əlavə edirik
        snake_pos.insert(0, new_head)

        # İlanın yeməyi yeməsi yoxlanılır
        if snake_pos[0][0] == food_pos[0] and snake_pos[0][1] == food_pos[1]:
            score += 10
            # Yeni yemək yaradırıq
            food_pos = [random.randrange(0, (WIDTH//BLOCK_SIZE)) * BLOCK_SIZE,
                        random.randrange(0, (HEIGHT//BLOCK_SIZE)) * BLOCK_SIZE]
        else:
            # Əgər yemək yeməyibsə, quyruğu silirik (beləcə ilan irəli hərəkət etmiş olur)
            snake_pos.pop()

        # Ekranı təmizləmək
        screen.fill(BLACK)

        # İlanı çəkmək
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

        # Yeməyi çəkmək
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

        # Xalı ekranda göstərmək
        show_score(score)

        # Divara dəymə yoxlanışı
        if snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT:
            running = False

        # Özünə dəymə yoxlanışı
        for block in snake_pos[1:]:
            if snake_pos[0] == block:
                running = False

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    # Oyun bitəndə Game Over ekranını göstər
    game_over_screen(score)

if __name__ == "__main__":
    start_game()