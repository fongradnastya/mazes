"""Основная программа"""

import os
import argparse

from typing import Any

from maze import generate, find_path
from graphic import start_visualization
from file_proc import read_from_text, \
    read_from_image


def check_args(args: Any) -> bool:
    """
    Проверка переданных программе аргументов
    @:param args: список аргументов командной строки
    """

    if args.width_height:
        if args.width_height[0] not in range(3, 201):
            print("Maze width should be between 3 and 200")
            return False
        if args.width_height[1] not in range(3, 201):
            print("Maze height should be between 3 and 200")
            return False

    if args.load_maze_text:
        if not os.path.exists(args.load_maze_text):
            print("This path is not exist")
            return False
        if not args.load_maze_text.endswith('.txt'):
            print("Wrong file type")
            return False

    if args.load_maze_image:
        if not os.path.exists(args.load_maze_image):
            print("This path is not exist")
            return False
        if not args.load_maze_image.endswith(('.png', '.jpg')):
            print("Wrong file type")
            return False

    if args.save_maze_image and \
            not args.save_maze_image.endswith(('.png', '.jpg')):
        print("Wrong file type")
        return False

    if args.save_maze_text and not args.save_maze_text.endswith(".txt"):
        print("Wrong file type")
        return False

    return True


def parse_args() -> None:
    """
    Обработка параметров командной строки
    """
    # Осуществляем разбор аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Generation and solution of mazes")

    # Метод add_mutually_exclusive_group() создает взаимоисключающую группу
    # параметров командной строки
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-wh', '--width_height', nargs=2, dest="width_height",
                       type=int, help='Ширина и высота лабиринта (от 3 до 200)')

    group.add_argument('-lmi', '--load-maze-image', dest="load_maze_image",
                       type=str,
                       help='Загрузка лабиринта из изображения')

    group.add_argument('-lmt', '--load-maze-text', dest="load_maze_text",
                       type=str,
                       help='Загрузка лабиринта из текста')

    parser.add_argument("-sol", "--solution", dest="solution",
                        action="store_true", help="Решение лабиринта")

    parser.add_argument("-smi", "--save-maze-image", dest="save_maze_image",
                        type=str, help="Выходной файл для сохранения лабиринта"
                                       "в виде изображения (jpg/png)")

    parser.add_argument("-smt", "--save-maze-text", dest="save_maze_text",
                        type=str, help="Выходной файл для сохранения лабиринта"
                                       "в виде текста (txt)")

    # В эту переменную попадает результат разбора аргументов командной строки.
    args = parser.parse_args()

    # Проверяем аргументы командной строки
    if check_args(args):
        maze = [[]]

        if args.width_height:
            maze = generate(args.width_height[0], args.width_height[1])

        elif args.load_maze_text:
            maze = read_from_text(args.load_maze_text)

        elif args.load_maze_image:
            maze = read_from_image(args.load_maze_image)

        if maze:
            if args.solution:
                try:
                    solution = find_path(maze)
                    print(solution)
                    start_visualization(maze, solution, args.save_maze_image,
                                        args.save_maze_text)
                except (IndexError, KeyError):
                    print("Runtime error")
            else:
                start_visualization(maze, img_path=args.save_maze_image,
                                    text_path=args.save_maze_text)
    else:
        print("Invalid arguments passed")


if __name__ == "__main__":
    parse_args()
