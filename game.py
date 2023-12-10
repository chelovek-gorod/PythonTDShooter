# главный файл игры - с него производим запуск (ctrl + F5)

import sys # модуль правильного выхода из игры

# импортируем константы, pygame (PG), спрайты и функцию инициализации
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from init import PG, SPRITES, init_src

from player import Player

# создаем игровое окно (заданной в константах ширины и высоты)
SCREEN = PG.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# создаем счетчик обновления экрана
CLOCK = PG.time.Clock()

# инициализируем (загружаем) игровые ресурсы
init_src()

# создаем игрока
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# счетчик кадров
frame = 0

# ПРОВЕРКА АНИМАЦИИ ВЗРЫВА
exp_fr = 0 # номер начального кадра
exp_max_fr = len( SPRITES['explosion'] ) # номер последнего кадра (число кадров)

# ИГРОВОЙ ЦИКЛ
is_on_game = True # цикл запущен
while is_on_game:
    CLOCK.tick(FPS) # ждем следующий кадр (время следующего обновления экрана)

    SCREEN.blit(SPRITES['background'], (0, 0))

    player.update()
    SCREEN.blit(player.image, player.rect) # рисуем игрока в верхнем левом углу экрана

    SCREEN.blit(SPRITES['explosion'][exp_fr], (500, 300)) # рисуем текущий кадр взрыва в координатах X:500 Y:300
    exp_fr += 1 # переключаем следующий кадр взрыва
    if (exp_fr == exp_max_fr) : exp_fr = 0 # если номер кадра взрыва равен числу всех кадров - сбрасываем его на 0

    PG.display.flip() # обновляем экран

    # получаем все события
    for event in PG.event.get():
        # останавливаем игровый цикл если было закрыто окно или нажата клавиша ESCAPE
        if event.type == PG.QUIT or (event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE):
            is_on_game = False

# завершение выполнения программы
PG.quit() # выходим из Pygame
sys.exit() # выключаем программу
