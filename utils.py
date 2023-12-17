# импортируем функции для расчетов и конвертации градусов в радианы из библиотеки math
from math import sqrt, atan2, cos, sin, degrees, radians

# функция расчета расстояния между объектами sprite и target
def get_distance(sprite_x, sprite_y, target_x, target_y):
    dx = target_x - sprite_x
    dy = target_y - sprite_y
    return sqrt(dx * dx + dy * dy)

# функция поворота спрайта sprite к объекту target
def turn_sprite_to_target(sprite, target_x, target_y):
    pointDirection = atan2(target_y - sprite.rect.centery, target_x - sprite.rect.centerx)
    sprite.direction = degrees(pointDirection)

# функция, возвращающая смещение спрайта sprite по осям X и Y, согласно его направления (sprite.direction) на расстояние  path
def move_sprite_by_direction(sprite, path):
    angle = radians(sprite.direction)
    move_x = cos(angle) * path
    move_y = sin(angle) * path
    return (move_x, move_y)