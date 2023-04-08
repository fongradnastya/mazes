import random

from queue import PriorityQueue


def generate(width, height):
    # Проверим ограничения параметров на 0
    if (width < 1) or (height < 1):
        return None

    top_limit = 2 ** 32 - 1
    # Проверим ограничения по максимальному допустимому размеру
    if ((top_limit - 1) // 2 <= width) or ((top_limit - 1) // 2 <= height):
        return None

    # Инициализируем размер конечной матрицы maze
    # Ячейки будут представлять собой фрагменты 2x2 + 1 одно значение
    # сверху и слева для стен
    output_height = height * 2 + 1
    output_width = width * 2 + 1
    # Инициализируем лабиринт
    maze = [['█' for j in range(output_width)] for i in range(output_height)]
    for i in range(1, output_height, 2):
        for j in range(1, output_width, 2):
            # Если этот элемент в строке является ячейкой в левом верхнем
            # угле области 2x2 - то это пустая ячейка в лабиринте
            maze[i][j] = ' '
            if i + 2 == output_height and not j + 2 == output_width:
                maze[i][j + 1] = ' '
            elif j + 2 == output_width and not i + 2 == output_height:
                maze[i + 1][j] = ' '
            elif not (i + 2 == output_height or j + 2 == output_width):
                is_bottom = random.randint(0, 1)
                maze[i + 1][j] = ' ' if is_bottom else '█'
                maze[i][j + 1] = ' ' if not is_bottom else '█'
    return maze


def best_first_search(maze):
    # Задаем начальную и конечную точки лабиринта
    start = (1, 1)
    goal = (len(maze) - 2, len(maze[0]) - 2)

    # Создаем очередь с приоритетами и добавляем в нее начальную точку
    frontier = PriorityQueue()
    frontier.put(start, False)

    # Словарь для хранения путей
    came_from = {start: None}

    while not frontier.empty():
        # Получаем следующую точку из очереди с приоритетами
        current = frontier.get()

        # Если мы достигли цели, то выходим из цикла
        if current == goal:
            break

        # Получаем соседние точки
        for next_point in get_neighbors(current, maze):
            # Если мы еще не были в этой точке
            if next_point not in came_from:
                # Вычисляем приоритет для этой точки
                priority = heuristic(goal, next_point)
                # Добавляем эту точку в очередь с приоритетами
                frontier.put(next_point, priority)
                # Добавляем путь до этой точки в словарь came_from
                came_from[next_point] = current

    # Восстанавливаем путь до цели из словаря came_from
    return reconstruct_path(came_from, start, goal)


def get_neighbors(pos, maze):
    neighbors = []
    # Перебираем четыре направления: вверх, вниз, влево и вправо
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        # Считаем координаты соседней точки
        neighbor = (pos[0] + direction[0], pos[1] + direction[1])
        # Проверяем, что соседняя точка не является стеной лабиринта
        if maze[neighbor[0]][neighbor[1]] != '█':
            # Добавляем соседнюю точку в список соседей
            neighbors.append(neighbor)
    return neighbors


def heuristic(a, b):
    # Вычисляем эвристическую функцию как манхеттенское расстояние
    # между двумя точками
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    # Идем от цели к началу по словарю came_from
    while current != start:
        # Добавляем текущую точку в путь
        path.append(current)
        # Переходим к предыдущей точке по пути
        current = came_from[current]
    # Добавляем начальную точку в путь
    path.append(start)
    # Переворачиваем путь, чтобы он шел от начала к цели
    path.reverse()
    return path
