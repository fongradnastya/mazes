# Генерация и решение лабиринта

Учебная работа по алгоритмам и структурам данных

## Описание программы

Данная программа генерирует лабиринт с помощью алгоритма двоичного дерева. 
А также определяет кратчайший путь от его начальной до конечной клетки 
на основе алгоритма Левита.

<p align="center">
  <img src="maze_image/maze.png" alt="maze" width="700"/>
</p>
<p align="center">
  <img src="maze_image/purple.png" alt="maze" width="700"/>
</p>

## Запуск программы

Генерация и решение лабиринта с заданным числом ячеек:

```cmd
python main.py -wh 20 10 -sol 
```
Считывание лабиринта из текстового файла:
```cmd
python main.py -lmt maze_text/array.txt -sol
```
Считывание лабиринта из изображения:
```cmd
python main.py -lmi maze_image/n_maze.png  
```
Сохранение лабиринта в виде изображения
```cmd
python main.py -wh 10 10 -smi maze_image/n_maze.png  
```
Сохранение лабиринта в текстовом виде
```cmd
python main.py -wh 10 10 -smt maze_text/n_maze.txt -sol 
```