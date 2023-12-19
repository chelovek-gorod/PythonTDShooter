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

# отключаем отображение курсора мыши
PG.mouse.set_visible(False)

# создаем игровое окно (заданной в константах ширины и высоты)
SCREEN = PG.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# создаем счетчик обновления экрана
CLOCK = PG.time.Clock()

# инициализируем (загружаем) игровые ресурсы
init_src()

# создаем прицел игрока
aim = Aim()

# создаем игрока
player = Player()

# создаем переменную для финального текста (победа или поражение)
final_text = None

level = 0 # текущий игровой уровень
levels_number = len(levels_list) # определяем количество уровней
# создаем текст в верхнем правом углу с указанием текущего уровня
level_label = Label(SCREEN_WIDTH, 0, 24, 6, (0, 255, 0), 'right', f'Level: {level}')

background = None

# функция обновления уровня
def next_level():
    global level, background # получаем доступ к редактированию переменных level и background (иначе их не получиться изменить)
    bullets_group.empty() # очищаем группу спрайтов пуль игрока
    walls_group.empty() # очищаем группу спрайтов стен
    effects_group.empty() # очищаем группу спрайтов с эффектами
    plasmas_group.empty() # очищаем группу спрайтов с плазменными выстрелами врагов
    bots_group.empty() # очищаем группу спрайтов врагов
    player.hp = UNIT_HP # восстанавливаем здоровье игроку
    player.healthbar.render() # обновляем полосу здоровья игрока
    level_data = levels_list[level] # получаем данные о текущем уровне из списка уровней
    background = SPRITES[level_data['background']] # обновляем фон для текущего уровня
    get_level(level_data['map'], player) # генерируем новый уровень
    level += 1 # увеличиваем номер уровня
    level_label.render(f'Level: {level}') # обновляем текст с номером уровня
    bg_music_play(MUSIC['level_' + str(level)]) # запускаем фоновую музыку для данного уровня
    SOUNDS['alarm'].play() # запускаем звуковой эффект сирены

# генерируем первый уровень (вызвав функцию next_level)
next_level()
    
# ИГРОВОЙ ЦИКЛ
is_on_game = True # цикл запущен
while is_on_game:
    CLOCK.tick(FPS) # ждем следующий кадр (время следующего обновления экрана)

    events = PG.event.get() # получаем список всех событий, которые произошли между обновлениями экрана игры

    SCREEN.blit(background, (0, 0)) # сперва рисуем фон,что бы он был ниже всего остального

    walls_group.draw(SCREEN) # рисуем стены уровня

    # если игрок жив - игрок, враги и пули обновляются
    if player.hp > 0:
        # считываем позицию курсора мыши
        mouse_x, mouse_y = PG.mouse.get_pos()
        aim.update(mouse_x, mouse_y) # обновляем положение прицела

        player.update(mouse_x, mouse_y, events, plasmas_group, walls_group) # обновляем игрока

        bullets_group.update(walls_group) # обновляем пули игрока
        bullets_group.draw(SCREEN) # рисуем пули игрока

        plasmas_group.update(walls_group) # обновляем выстрелы врагов
        plasmas_group.draw(SCREEN) # рисуем выстрелы врагов

        player.draw(SCREEN) # рисуем игрока
        bots_group.update(player, bullets_group, walls_group, SCREEN) # обновляем врагов

    # иначе (если игрок мертв) - рисуем финальный текст с поражением
    else:
        if final_text == None: # записываем текст в переменную final_text, только если текста в ней еще нету
            final_text = Label(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - (96/2 + 24), 96, 24, (255, 0, 0), 'center', 'GAME OVER')
            SOUNDS['game_over'].play() # проигрываем звуковой эффект проигрыша

    effects_group.update(SCREEN) # рисуем эффекты

    labels_group.draw(SCREEN) # рисуем надписи

    # если все враги уничтожены
    if len(bots_group) == 0:
        # если это был последний уровень - рисуем финальный текст с победой
        if level == levels_number:
            if final_text == None: # записываем текст в переменную final_text, только если текста в ней еще нету
                final_text = Label(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - (96/2 + 24), 96, 24, (0, 0, 255), 'center', 'WIN')
        # иначе (если уровень не последний) - генерируем следующий уровень
        else : next_level()

    # последним рисуем курсор, что бы он был поверх всего остального
    SCREEN.blit(aim.image, aim.rect)

    PG.display.flip() # обновляем экран

    # получаем все события
    for event in events:
        # если фоновая музыка закончилась - запускаем заново
        if event.type == MUSIC_END : bg_music_play()
        # останавливаем игровый цикл если было закрыто окно или нажата клавиша ESCAPE
        if event.type == PG.QUIT or (event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE):
            is_on_game = False

# завершение выполнения программы
PG.quit() # выходим из Pygame
sys.exit() # выключаем программу