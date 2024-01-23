import cv2
import pygame
from pygame.locals import *
from cvzone.HandTrackingModule import HandDetector
from maze_list import maze1, maze2, maze3, maze4, maze5, maze6, maze7, maze8, maze9, maze10, maze11, maze12

pygame.init()

screen_width, screen_height = 750, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hand Tracking Maze Game")

black = (0, 0, 0)
white = (255, 255, 255)
player_size = 20

detector = HandDetector(detectionCon=0.6, maxHands=1)
cap = cv2.VideoCapture(0)

clock = pygame.time.Clock()
FPS = 30
smooth_factor = 0.1
start_color = (0, 0, 255)
player_color = (255, 0, 0)
finish_color = (0, 255, 0)
threshold_distance = 30

current_level = 1
max_levels = 12
maze = globals()[f'maze{current_level}']

# Начальные координаты игрока
player_x, player_y = 0, 0
target_player_x, target_player_y = player_x, player_y

def initialize_start_position():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 3:
                return j * 50 + 25, i * 50 + 25

# Инициализация начальных координат
player_x, player_y = initialize_start_position()
target_player_x, target_player_y = player_x, player_y

level_completed = False
victory_screen = False
start_time = pygame.time.get_ticks()
end_time = 0

font = pygame.font.Font(None, 36)

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            cv2.destroyAllWindows()
            exit()

    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, _ = detector.findHands(img)

    if hands:
        hand = hands[0]
        index_finger = hand["lmList"][8]
        thumb = hand["lmList"][4]
        distance = ((index_finger[0] - thumb[0]) ** 2 + (index_finger[1] - thumb[1]) ** 2) ** 0.5

        if distance < threshold_distance:
            x, y = index_finger[0], index_finger[1]
            target_x = int(x / cap.get(3) * screen_width)
            target_y = int(y / cap.get(4) * screen_height)
            target_player_x = target_x
            target_player_y = target_y

    prev_player_x, prev_player_y = player_x, player_y

    player_x += (target_player_x - player_x) * smooth_factor
    player_y += (target_player_y - player_y) * smooth_factor

    player_tile_x = int(player_x // 50)
    player_tile_y = int(player_y // 50)

    if (
        0 <= player_tile_y < len(maze) and
        0 <= player_tile_x < len(maze[0]) and
        maze[player_tile_y][player_tile_x] == 1
    ):
        player_x, player_y = prev_player_x, prev_player_y

    screen.fill(black)

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                wall_rect = pygame.Rect(j * 50, i * 50, 50, 50)
                pygame.draw.rect(screen, white, wall_rect)
            elif maze[i][j] == 2:
                finish_rect = pygame.Rect(j * 50, i * 50, 50, 50)
                pygame.draw.rect(screen, finish_color, finish_rect)
            elif maze[i][j] == 3:
                start_rect = pygame.Rect(j * 50, i * 50, 50, 50)
                pygame.draw.rect(screen, start_color, start_rect)

    pygame.draw.circle(screen, player_color, (int(player_x), int(player_y)), player_size)

    if (
        0 <= player_tile_y < len(maze) and
        0 <= player_tile_x < len(maze[0]) and
        maze[player_tile_y][player_tile_x] == 2 and
        not level_completed
    ):
        level_completed = True
        end_time = pygame.time.get_ticks()

    if level_completed:
        elapsed_time = (end_time - start_time) // 1000
        text_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 50, 300, 150)
        pygame.draw.rect(screen, (100, 100, 100), text_rect)
        win_text = font.render("Вы победили!", True, white)
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - 20))
        timer_text = font.render(f"Время: {elapsed_time} сек", True, white)
        screen.blit(timer_text, (screen_width // 2 - timer_text.get_width() // 2, screen_height // 2 + 20))
        next_level_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 70, 200, 50)
        pygame.draw.rect(screen, (150, 150, 150), next_level_button)
        next_level_text = font.render("Следующий уровень", True, white)
        screen.blit(next_level_text, (screen_width // 2 - next_level_text.get_width() // 2, screen_height // 2 + 90))
        victory_screen = True

    if victory_screen:
        pygame.display.update()

        # Обработка нажатия кнопки "следующий уровень"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if next_level_button.collidepoint(mouse_x, mouse_y):
            if current_level < max_levels:
                current_level += 1
                maze = globals()[f'maze{current_level}']  # Получаем следующую матрицу лабиринта
                player_x, player_y = initialize_start_position()
                target_player_x, target_player_y = player_x, player_y
                level_completed = False
                victory_screen = False
                start_time = pygame.time.get_ticks()
                end_time = 0
            else:
                # Если достигнут последний уровень, игра завершается
                pygame.quit()
                cv2.destroyAllWindows()
                exit()

        continue

    pygame.display.update()

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
