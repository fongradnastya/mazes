import random
from collections import defaultdict, OrderedDict
from itertools import chain
from math import inf


def generate(width, height):
    # Проверим ограничения параметров на 0
    if (width < 1) or (height < 1):
        return None
    top_limit = 2 ** 32 - 1
    # Проверим ограничения по максимальному допустимому размеру
    if ((top_limit - 1) // 2 <= width) or ((top_limit - 1) // 2 <= height):
        return None

    # Ячейки будут представлять собой фрагменты 2x2 + 1 одно значение
    # сверху и слева для стен
    output_height = height * 2 + 1
    output_width = width * 2 + 1
    # Инициализируем лабиринт
    maze = [['█' for _ in range(output_width)] for _ in range(output_height)]
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


class IndexedQueue(OrderedDict):
    "Queue-like container with fast search"

    def push(self, item):
        self[item] = None

    def pop(self):
        return OrderedDict.popitem(self, last=False)[0]


def find_path(points, start, end=None):
    gr = create_dict(points)
    dist = defaultdict(lambda: inf)
    dist[start] = 0
    path = {start: (start, ())}
    m0 = set()
    m1, m1_urg = IndexedQueue.fromkeys([start]), IndexedQueue()
    m2 = set(chain.from_iterable(
        (v for v in from_u) for from_u in gr.values())) - {start}

    def relax(u, v):
        if dist[v] > dist[u] + 1:
            dist[v] = dist[u] + 1
            path[v] = (v, path[u])
            return True
        return False

    while m1 or m1_urg:
        u = m1_urg.pop() if m1_urg else m1.pop()
        for v in gr.get(u, ()):
            if v in m2:
                m1.push(v)
                m2.discard(v)
                relax(u, v)
            elif v in m1:
                relax(u, v)
            elif v in m0 and relax(u, v):
                m1_urg.push(v)
                m0.discard(v)
        m0.add(u)

    if end is None:
        return path
    elif end in path:
        restore_path = lambda tup: \
            (*restore_path(tup[1]), tup[0]) if tup else ()
        return restore_path(path[end])
    else:
        return ()


def create_dict(points):
    points_dict = defaultdict(list)
    for first, second in points:
        points_dict[first].append(second)
    return points_dict


if __name__ == '__main__':
    points = [('a', 'b'), ('b', 'c'), ('c', 'a'), ('c', 'd'), ('a', '5')]
    path = find_path(points, 'a', 'c')
    print(path)
