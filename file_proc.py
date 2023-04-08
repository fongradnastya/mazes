from PIL import Image


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
        for i in range(width):
            for j in range(height):
                if img.getpixel((i, j)) == (255, 255, 255):
                    diagonal = ((i ** 2 + j ** 2) ** 0.5)
                    square_size = int(diagonal / (2 ** 0.5))
                    return square_size


def read_from_image(path_to_file: str):
    with Image.open(path_to_file) as img:
        maze = []

        square_size = calculate_square_size(path_to_file)

        for i in range(0, img.size[1], square_size):
            row = []
            for j in range(0, img.size[0], square_size):
                square = img.crop((j, i, j + square_size, i + square_size))

                if (0, 0, 0) in [color[1] for color in square.getcolors()]:
                    row.append('█')
                else:
                    row.append('')
            maze.append(row)

    return maze
