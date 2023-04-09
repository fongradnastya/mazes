import pygame as pg
from PIL import Image

WALL = (134, 28, 176)
BACKGROUND = (217, 135, 250)


def read_from_text(path_to_file: str):
    maze = []
    with open(path_to_file, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                maze.append(list(line.strip()))
    return maze


def calculate_square_size(path_to_file: str):
    with Image.open(path_to_file) as img:
        width, height = img.size
        print(img.getpixel((0, 0)))
        print(img.getpixel((1, 1)))
        print(img.getpixel((0, 1)))
        for i in range(width):
            for j in range(height):
                if img.getpixel((i, j)) == BACKGROUND:
                    diagonal = ((i ** 2 + (j + 1) ** 2) ** 0.5)
                    square_size = int(diagonal / (2 ** 0.5))
                    return square_size


def read_from_image(path_to_file: str):
    with Image.open(path_to_file) as img:
        maze = []
        square_size = calculate_square_size(path_to_file)
        if not square_size:
            print("This image is incorrect")
            return None
        for i in range(0, img.size[1], square_size):
            row = []
            for j in range(0, img.size[0], square_size):
                square = img.crop((j, i, j + square_size, i + square_size))
                colors = [color[1] for color in square.getcolors()]
                print(colors)
                if WALL in colors:
                    row.append('█')
                else:
                    row.append(' ')
            maze.append(row)
    return maze


def save_img(screen, img_path):
    print(f"Изображение лабиринта сохранено в файл {img_path}")
    pg.image.save(screen, img_path)


def save_txt(maze, text_path):
    with open(text_path, "w", encoding="utf-8") as file:
        for row in maze:
            file.write(''.join(row) + "\r\n")
    print(f"Лабиринт в текстовом формате сохранён в файл {text_path}")
