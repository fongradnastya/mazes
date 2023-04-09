import pygame as pg
from file_proc import *

# Задаем цвета
WALL = (134, 28, 176)
BACKGROUND = (217, 135, 250)
PATH = (252, 219, 3)

WHITE = (225, 225, 225)
BLACK = (0, 0, 0)


def print_maze(maze):
    # Проверяем указатель на None
    if maze is None:
        return
    # Построчно считываем и выводим в консоль
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end='')
        print()


def visualize_maze(screen, maze, scale):
    # Проверяем указатель на None
    if maze is None:
        return
    # Рисуем лабиринт
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '█':
                pg.draw.rect(screen, BLACK,
                             (j * scale, i * scale, scale, scale))
            else:
                pg.draw.rect(screen, WHITE, (j * scale, i * scale, scale,
                                                  scale))
    # Обновляем экран
    pg.display.flip()


def draw_solution(screen, solution, scale):
    # Проверяем указатель на None
    if solution is None:
        return
    prev = None
    # Рисуем решение лабиринта
    for point in solution:
        pg.draw.rect(screen, PATH,
                     (point[1] * scale, point[0] * scale, scale, scale))
        if prev:
            pg.draw.rect(screen, PATH,
                         (prev[1] * scale, prev[0] * scale, scale, scale))
        imp = pg.image.load("bird.png").convert_alpha()
        imp = pg.transform.scale(imp, (scale, scale / 1.3))
        screen.blit(imp, (point[1] * scale, point[0] * scale + (scale / 8)))
        # Обновляем экран
        pg.display.flip()
        pg.time.wait(100)
        prev = point


def print_solution(solution):
    print("Maze solution: ", end="")
    solution_str = map(str, solution)
    solution_str = " -> ".join(solution_str)
    print(solution_str)


def visualization_init(maze: [[]], solution: [()] = None,
                       img_path: str = None, text_path: str = None):
    # Инициализируем Pygame
    pg.init()
    pg.display.set_caption('Maze solution')
    width = len(maze[0])
    height = len(maze)
    scale = 900 // height if height >= width else 900 // width
    # Создаем окно
    screen = pg.display.set_mode((width * scale, height * scale))
    visualize_maze(screen, maze, scale)
    if solution:
        print_solution(solution)
        draw_solution(screen, solution, scale)
    if img_path:
        save_img(screen, img_path)
    if text_path:
        save_txt(maze, text_path)
    # Ожидаем закрытия окна
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    # Выходим из Pygame
    pg.quit()
