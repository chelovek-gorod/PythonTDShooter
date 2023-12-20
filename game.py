# ГЛАВНЫЙ ФАЙЛ ИГРЫ с него производим запуск (ctrl + F5)

# дял сборки проекта с помощью pyinstaller (установть pyinstaller можно прописав в терминал: pip install pyinstaller)
# pyinstaller --onefile --name TDShooter --icon=src\images\shooter_128x128.ico -F --noconsole game.py

import sys # импорт модуля sys, для правильного выхода из игры

# из файла constants импортируем размеры игрового окна, частоту обновления экрана, здоровье юнитов
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, UNIT_HP
# из файла init импортируем PG(PyGame), словарь со спрайтами SPRITES, функции init_src и bg_music_play, звуки, музыку и событие остановки трека
from init import PG, SPRITES, init_src, bg_music_play, SOUNDS, MUSIC, MUSIC_END
# из файла level импортируем список игровых уровней levels_list и функцию создания уровня get_level
from level import levels_list, get_level

# из файлов ниже - импортируем классы и группы
from aim import Aim
from player import Player
from bullet import bullets_group
from wall import walls_group
from effect import effects_group
from label import labels_group, Label
from plasma import plasmas_group
from bot import bots_group
from button import Button, buttons_group
from title import Title, titles_group

# функция создания меню (принимает тип меню)
def get_menu(menu_type = ''):
    global background # получаем доступ к редактированию переменной background (иначе её не получиться изменить)
    titles_group.empty() # очищаем заголовки меню
    buttons_group.empty() # очищаем кнопки меню
    if menu_type == 'main': # если тип меню 'main' - создаем ГЛАВНОЕ МЕНЮ ИГРЫ
        background = SPRITES['main_menu'] # обновляем фоновое изображение для текущего меню
        Title(SCREEN_WIDTH/2, 100, 'Top Down Shooter', 120, (255, 0, 0))  # создаем заголовок меню
        Button(SCREEN_WIDTH/2, 500, start_game, 'START') # создаем кнопку с координатами, функцией клика и текстом
        Button(SCREEN_WIDTH/2, 600, exit_game, 'EXIT') # создаем кнопку с координатами, функцией клика и текстом
    elif menu_type == 'pause':
        background = SPRITES['next_menu'] # обновляем фоновое изображение для текущего меню
        Title(SCREEN_WIDTH/2, 300, 'pause', 60, (255, 255, 255)) # создаем заголовок меню
        Button(SCREEN_WIDTH/2, 400, resume_game, 'RESUME') # создаем кнопку с координатами, функцией клика и текстом
        Button(SCREEN_WIDTH/2, 500, restart_game, 'MAIN MENU') # создаем кнопку с координатами, функцией клика и текстом
        Button(SCREEN_WIDTH/2, 600, exit_game, 'EXIT') # создаем кнопку с координатами, функцией клика и текстом
    elif menu_type == 'game_over':
        background = SPRITES['lose_menu'] # обновляем фоновое изображение для текущего меню
        Title(SCREEN_WIDTH/2, 100, 'GAME OVER', 90, (0, 0, 0), (255, 0, 0)) # создаем заголовок меню
        Button(SCREEN_WIDTH/2, 500, restart_game, 'MAIN MENU') # создаем кнопку с координатами, функцией клика и текстом
        Button(SCREEN_WIDTH/2, 600, exit_game, 'EXIT') # создаем кнопку с координатами, функцией клика и текстом
    elif menu_type == 'game_win':
        background = SPRITES['main_menu'] # обновляем фоновое изображение для текущего меню
        Title(SCREEN_WIDTH/2, 100, 'YOU WIN', 90, (255, 255, 255)) # создаем заголовок меню
        Button(SCREEN_WIDTH/2, 500, restart_game, 'MAIN MENU') # создаем кнопку с координатами, функцией клика и текстом
        Button(SCREEN_WIDTH/2, 600, exit_game, 'EXIT') # создаем кнопку с координатами, функцией клика и текстом
    else: # уровень пройден
        background = SPRITES['next_menu'] # обновляем фоновое изображение для текущего меню
        Title(SCREEN_WIDTH/2, 100, f'Level {level} done', 90, (255, 255, 255)) # создаем заголовок меню
        Button(SCREEN_WIDTH/2, 400, next_level, 'CONTINUE') # создаем кнопку с координатами, функцией клика и текстом
        Button(SCREEN_WIDTH/2, 500, restart_game, 'MAIN MENU') # создаем кнопку с координатами, функцией клика и текстом
        Button(SCREEN_WIDTH/2, 600, exit_game, 'EXIT') # создаем кнопку с координатами, функцией клика и текстом

# функция запуска игры
def start_game():
    next_level() # генерируем первый уровень (вызвав функцию next_level)

# функция паузы
def pause_game():
    global is_on_game # получаем доступ к редактированию переменной is_on_game (иначе её не получиться изменить)
    is_on_game = False # переключаем игру в состояние False (для показа меню)
    get_menu('pause') # создаем меню паузы

# функция возврата в паузы из паузы
def resume_game():
    global is_on_game, background # получаем доступ к редактированию переменных is_on_game и background
    is_on_game = True # переключаем игру в состояние True (для показа игрового процесса)
    background = level_background # возвращаем в переменную background фон текущего уровня

# функция выхода их игры
def exit_game():
    global is_on_loop # получаем доступ к редактированию переменной is_on_loop (иначе её не получиться изменить)
    is_on_loop = False # останавливаем главный игровой цикл, для закрытия окна с игрой

# функция проигрыша
def game_over():
    global is_on_game # получаем доступ к редактированию переменной is_on_game (иначе её не получиться изменить)
    is_on_game = False # переключаем игру в состояние False (для показа меню)
    get_menu('game_over') # создаем меню проигрыша
    SOUNDS['game_over'].play() # проигрываем звуковой эффект проигрыша

# функция победы
def game_win():
    global is_on_game  # получаем доступ к редактированию переменной is_on_game (иначе её не получиться изменить)
    is_on_game = False # переключаем игру в состояние False (для показа меню)
    get_menu('game_win') # создаем меню победы
    bg_music_play(MUSIC['win']) # запускаем победную фоновую музыку

# функция завершения уровня
def level_cleared(): 
    global is_on_game # получаем доступ к редактированию переменной is_on_game (иначе её не получиться изменить)
    is_on_game = False # переключаем игру в состояние False (для показа меню)
    get_menu() # создаем меню завершения уровня

# функция перезапуска игры
def restart_game():
    global level, player # получаем доступ к редактированию переменных level и player
    level = 0 # обнуляем текущий уровень
    if player != None: # если игрок был ранее создан
        player.healthbar.kill() # уничтожаем полосу здоровья игрока (иначе останется в оперативной памяти)
        player.bullets_label.kill() # уничтожаем надпись с числом пуль игрока (иначе останется в оперативной памяти)
        player.kill() # уничтожаем игрока
    player = Player() # создаем игрока
    get_menu('main') # создаем главное меню игры
    bg_music_play(MUSIC['win']) # запускаем фоновую музыку для главного меню

# функция обновления меню (принимает координаты мыши и события, для отслеживания наведения на кнопки и клика)
def menu_loop(mouse_x, mouse_y, events):
    titles_group.draw(SCREEN) # рисуем заголовок (или несколько заголовков, если их в меню будет несколько)
    buttons_group.update(mouse_x, mouse_y, events) # обновляем кнопки (отслеживаем курсор и клики)
    buttons_group.draw(SCREEN) # рисуем кнопки

# функция обновления игры (принимает координаты мыши и события)
def game_loop(mouse_x, mouse_y, events):
    walls_group.draw(SCREEN) # рисуем стены уровня
    player.update(mouse_x, mouse_y, events, plasmas_group, walls_group) # обновляем игрока
    bullets_group.update(walls_group) # обновляем пули игрока
    bullets_group.draw(SCREEN) # рисуем пули игрока

    plasmas_group.update(walls_group) # обновляем выстрелы врагов
    plasmas_group.draw(SCREEN) # рисуем выстрелы врагов

    player.draw(SCREEN) # рисуем игрока
    bots_group.update(player, bullets_group, walls_group, SCREEN) # обновляем врагов

    effects_group.update(SCREEN) # рисуем эффекты
    labels_group.draw(SCREEN) # рисуем надписи

    if player.hp <= 0 : game_over() # если у игрока закончилось hp - вызываем функцию проигрыша

    if len(bots_group) == 0: # если уничтожили всех врагов
        if level == levels_number: game_win() # если это был последний уровень - вызываем функцию победы
        else : level_cleared() # иначе - вызываем функцию завершения уровня

# функция обновления уровня
def next_level():
    global level, background, level_background, is_on_game # получаем доступ к редактированию переменных
    bullets_group.empty() # очищаем группу спрайтов пуль игрока
    walls_group.empty() # очищаем группу спрайтов стен
    effects_group.empty() # очищаем группу спрайтов с эффектами
    plasmas_group.empty() # очищаем группу спрайтов с плазменными выстрелами врагов
    bots_group.empty() # очищаем группу спрайтов врагов
    player.prepare_to_next_level() # восстанавливаем hp и пули игрока
    level_data = levels_list[level] # получаем данные о текущем уровне из списка уровней
    level_background = SPRITES[level_data['background']] # обновляем фон для текущего уровня
    background = level_background # обновляем фон для отрисовки в игровом цикле
    get_level(level_data['map'], player) # генерируем новый уровень
    level += 1 # увеличиваем номер уровня
    level_label.render(f'Level: {level}') # обновляем текст с номером уровня
    bg_music_play(MUSIC['level_' + str(level)]) # запускаем фоновую музыку для данного уровня
    is_on_game = True # переключаем игру в состояние True (для показа игрового процесса) 
    SOUNDS['alarm'].play() # запускаем звуковой эффект сирены

PG.mouse.set_visible(False) # отключаем отображение курсора мыши
SCREEN = PG.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # создаем игровое окно (заданной в константах ширины и высоты)
CLOCK = PG.time.Clock() # создаем счетчик обновления экрана
init_src() # инициализируем (загружаем) игровые ресурсы

aim = Aim() # создаем прицел игрока
player = None # создаем игрока

level = 0 # текущий игровой уровень
levels_number = len(levels_list) # определяем количество уровней
# создаем текст в верхнем правом углу с указанием текущего уровня
level_label = Label(SCREEN_WIDTH, 0, 24, 6, (0, 255, 0), 'right', f'Level: {level}')

background = None # переменная фона, рисуемого в игровом цикле
level_background = None # переменная фона текущего уровня

is_on_game = False # Игра не началась (сейчас активно меню)

# ЗАПУСК ИГРЫ
restart_game()
    
# ИГРОВОЙ ЦИКЛ
is_on_loop = True # цикл запущен
while is_on_loop:
    CLOCK.tick(FPS) # ждем следующий кадр (время следующего обновления экрана)
    events = PG.event.get() # получаем список всех событий, которые произошли между обновлениями экрана игры
    mouse_x, mouse_y = PG.mouse.get_pos() # считываем позицию курсора мыши
    aim.update(mouse_x, mouse_y) # обновляем положение прицела
    SCREEN.blit(background, (0, 0)) # сперва рисуем фон,что бы он был ниже всего остального

    if is_on_game: game_loop(mouse_x, mouse_y, events) # если игра и - вызываем функцию game_loop()
    else: menu_loop(mouse_x, mouse_y, events) # иначе - показываем игровое меню (функция menu_loop())

    # последним рисуем курсор, что бы он был поверх всего остального
    SCREEN.blit(aim.image, aim.rect)

    PG.display.flip() # обновляем экран

    # получаем все события
    for event in events:
        # если фоновая музыка закончилась - запускаем заново
        if event.type == MUSIC_END : bg_music_play()
        # останавливаем игровой цикл если было закрыто окно или нажата клавиша ESCAPE
        if event.type == PG.QUIT: # проверка закрытия игрового окна
            is_on_loop = False # останавливаем главный цикл игры
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE: # если нажата кнопка ESCAPE (ESC)
            if is_on_game : pause_game() # если во время игры - ставим игру на паузу
            else : is_on_loop = False # иначе (в любои игровом меню) - останавливаем главный цикл игры

# завершение выполнения программы
PG.quit() # выходим из Pygame
sys.exit() # выключаем программу