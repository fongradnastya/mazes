import random
from collections import defaultdict, OrderedDict
from itertools import chain
from math import inf


def generate(width, height):
    """
    Генерирует лабиринт при помощи метода двоичного дерева
    @:param width: ширина генерируемого лабиринта
    @:param height: высота генерируемого лабиринта
    @:return: созданный лабиринт
    """
    if (width < 1) or (height < 1):
        return None
    top_limit = 2 ** 32 - 1
    # Проверим ограничения по максимальному допустимому размеру
    if ((top_limit - 1) // 2 <= width) or ((top_limit - 1) // 2 <= height):
        return None
    # Ячейки будут представлять собой фрагменты 2x2 + 1 одно значение
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
    """
    Получает список всех ячеек, в которые можно перейти из данной
    @:param pos: позиция текущей ячейки
    @:param maze: лабиринт для поиска
    @:return: список соседних ячеек
    """
    neighbors = []
    # Перебираем четыре направления: вверх, вниз, влево и вправо
    for direction in [(0, 1), (1, 0)]:
        # Считаем координаты соседней точки
        neighbor = (pos[0] + direction[0], pos[1] + direction[1])
        # Проверяем, что соседняя точка не является стеной лабиринта
        if maze[neighbor[0]][neighbor[1]] != '█':
            # Добавляем соседнюю точку в список соседей
            neighbors.append(neighbor)
    return neighbors


class IndexedQueue(OrderedDict):
    """
    Класс очереди, построенной на основе списков
    """

    def push(self, item):
        """
        Добавление элемента в конец очереди
        """
        self[item] = None

    def pop(self):
        """
        Удаление элемента из очереди
        """
        return OrderedDict.popitem(self, last=False)[0]


def find_path(maze):
    """
    Вычисляет кратчайший путь при помощи алгоритма Левита
    @:param maze: лабиринт для поиска пути
    @:return: последовательность вершин из кратчайшего пути
    """
    start = (1, 1)
    end = (len(maze) - 2, len(maze[0]) - 2)
    gr = create_dict(maze, len(maze[0]), len(maze))
    dist = defaultdict(lambda: inf)
    dist[start] = 0
    path = {start: (start, ())}
    m0 = set()
    m1, m1_urg = IndexedQueue.fromkeys([start]), IndexedQueue()
    m2 = set(chain.from_iterable(
        (v for v in from_u) for from_u in gr.values())) - {start}

    def relax(first_el, second_el):
        if dist[second_el] > dist[first_el] + 1:
            dist[second_el] = dist[first_el] + 1
            path[second_el] = (second_el, path[first_el])
            return True
        return False

    while m1 or m1_urg:
        first_el = m1_urg.pop() if m1_urg else m1.pop()
        for second_el in gr.get(first_el, ()):
            if second_el in m2:
                m1.push(second_el)
                m2.discard(second_el)
                relax(first_el, second_el)
            elif second_el in m1:
                relax(first_el, second_el)
            elif second_el in m0 and relax(first_el, second_el):
                m1_urg.push(second_el)
                m0.discard(second_el)
        m0.add(first_el)

    if end is None:
        return path
    elif end in path:
        restore_path = lambda tup: \
            (*restore_path(tup[1]), tup[0]) if tup else ()
        return restore_path(path[end])
    else:
        return ()


def create_dict(maze, width, height):
    """
    Создаёт словарь смежных друг с другом вершин
    @:param maze: лабиринт в виде двухмерного списка
    @:param width: ширина лабиринта
    @:param height: высота лабиринта
    @:return: словарь смежных ячеек лабиринта
    """
    points_dict = defaultdict(list)
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            neighbors = get_neighbors((i, j), maze)
            for neighbor in neighbors:
                points_dict[(i, j)].append(neighbor)
    return points_dict
