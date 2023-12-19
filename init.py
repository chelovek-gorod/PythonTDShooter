# ФАЙЛ ИНИЦИАЛИЗАЦИИ И ЗАГРУЗКИ ИГРОВЫХ РЕСУРСОВ

# из файла constants импортируем размеры игрового окна
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Импортируем pygame в переменную PG
import pygame as PG
PG.init() # инициализируем pygame (без этого не работают шрифты и некоторый функционал)
PG.mixer.init() # инициализируем PyGame.mixer для работы с фоновой музыкой и звуками

SPRITE = PG.sprite.Sprite # выносим класс Sprite (из объекта sprite библиотеки pygame) в константу спрайтов
GROUP = PG.sprite.Group # выносим класс Group (из объекта sprite библиотеки pygame) в константу группы спрайтов

# функция для загрузки спрайтов (из одиночной картинки)
# file_name - имя загружаемого файла
def get_sprite(file_name):
    # возвращаем загруженное изображение с прозрачным фоном (если фон у изображения прозрачный)
    return PG.image.load(SPRITES_PATH + file_name).convert_alpha()

# функция для загрузки анимированных спрайтов (в одном изображении собрано несколько кадров)
# file_name - имя загружаемого файла, frame_width и frame_height - ширина и высота кадра, frames - количество кадров
def get_sprite_sheet(file_name, frame_width, frame_height, frames):
    sprite_sheet = [] # создаем список, куда будем складывать все кадры
    image = PG.image.load(SPRITES_PATH + file_name).convert_alpha() # загружаем исходное изображение
    image_width, image_height = image.get_width(), image.get_height() # определяем ширину и высоту загруженного изображения
    # далее будем вырезать по кадру из исходного изображения image и добавлять их в список кадров sprite_sheet
    image_x, image_y = 0, 0 # начальные координаты верхнего левого угла кадра, который нужно получить из исходного изображения image
    current_frame = 0 # номер текущего получаемого кадра
    while image_y < image_height: # цикл, для перемещения по вертикали исходного изображения image
        while image_x < image_width: # цикл, для перемещения по горизонтали исходного изображения image
            # создаем поверхность с прозрачным фоном
            frame = PG.Surface((frame_width, frame_height), PG.SRCALPHA)
            # рисуем на поверхности текущий кадр
            frame.blit(image, (0, 0), (image_x, image_y, image_x + frame_width, image_y + frame_height))
            sprite_sheet.append(frame) # добавляем полученный кадр в список кадров
            image_x += frame_width # смещаемся по оси x к следующему кадру
            current_frame += 1 # увеличиваем номер текущего кадра
            if (current_frame == frames): return sprite_sheet # если номер кадра равен числу необходимых кадров - возвращаем готовый список кадров
        # после того, как мы перебрали все кадры по горизонтали - переходим на следующий ряд кадров (шаг вниз по оси y)
        image_x = 0 # возвращаемся в начало координат по оси x (чтобы новый ряд считывать с первого кадра этого ряда)
        image_y += frame_height # переходим на следующий ряд кадров (шаг вниз по оси y)
    # если мы прошлись по всем рядам (все циклы выполнены)
    return sprite_sheet # возвращаем готовый список кадров

# функция для загрузки тайловых спрайтов (одно изображение, собранное из "плиток" (тайлов))
# file_name - имя загружаемого файла, image_width и image_height - ширина и высота изображения, которое необходима создать из тайлов
def get_tile_sprite(file_name, image_width, image_height):
    tile = PG.image.load(SPRITES_PATH + file_name).convert() # загружаем картинку тайла
    tile_width, tile_height = tile.get_width(), tile.get_height() # определяем ширину и высоту тайла

    image = PG.Surface((image_width, image_height)) # создаем поверхность, размера итогового тайлового спрайта
    image_x, image_y = 0, 0 # задаем координаты на поверхности, с которых начнем "выкладывать" тайлы

    # цикл для прохода по вертикали поверхности и горизонтали, с шагом, равному высоте и ширине тайла
    while image_y < image_height:
        while image_x < image_width:
            image.blit(tile, (image_x, image_y), (0, 0, tile_width, tile_height)) # отрисовываем тайл в текущих координатах
            image_x += tile_width # смещаемся на ширину тайла по оси X
        # когда мы выложили тайлы по горизотали
        image_x = 0 # обнуляем координату X (чтобы сместится к началу поверхности, для отрисовки следующего ряда)
        image_y += tile_height # смещаемся на высоту тайла по оси Y (для отрисовки следующего ряда)

    return image # возвращаем полученную картинку из тайлов

# функция загрузки звуковых эффектов
def init_sound(sound_name):
    sound = PG.mixer.Sound(SOUNDS_PATH + sound_name)
    #sound.set_volume(0.1)
    return sound

# функция проигрывания фоновой музыки
# music - имя загружаемого файла (music = None - значение по умолчанию, нужно для повторного проигрывания трек, после его окончания)
def bg_music_play(music = None):
    global current_bg_music # получаем доступ к редактированию переменной current_bg_music (иначе ее не получиться изменить)
    if music : current_bg_music = music # название трека в переменную current_bg_music, если он был передан

    PG.mixer.music.load(current_bg_music) # дожидаемся загрузки файла фоновой музыки
    PG.mixer.music.set_volume(0.7) # задаем громкость фоновой музыки (0...1)
    PG.mixer.music.play() # запускаем фоновую музыку

# переменная с текущей фоновой музыкой
current_bg_music = None

# создаем PyGame событие MUSIC_END, которое сработает при окончании трека фоновой музыки
MUSIC_END = PG.USEREVENT + 1 # +1, так как мы к существующим событиям добавляем новое
PG.mixer.music.set_endevent(MUSIC_END) # привязываем событие к окончанию трека

# создаем переменные с путями расположения (папки) спрайтов, звуков и шрифтов
SPRITES_PATH = './src/sprites/'
SOUNDS_PATH = './src/sounds/'
FONTS_PATH = './src/fonts/'

SPRITES = {} # создаем словарь со спрайтами
FONTS = {} # создаем словарь со шрифтами
SOUNDS = {} # создаем словарь с звуковыми эффектами
MUSIC = {} # создаем словарь с фоновой музыкой

# функция инициализации (загрузки) игровых ресурсов (спрайты, звуки и шрифты)
def init_src():
    # загружаем тайловые спрайты, спрайты и анимированные спрайты
    SPRITES['bg_grass'] = get_tile_sprite('bg_grass_128x128px.png', SCREEN_WIDTH, SCREEN_HEIGHT)
    SPRITES['bg_desert'] = get_tile_sprite('bg_desert_128x128px.png', SCREEN_WIDTH, SCREEN_HEIGHT)
    SPRITES['bg_night'] = get_tile_sprite('bg_night_128x128px.png', SCREEN_WIDTH, SCREEN_HEIGHT)
    SPRITES['wall'] = get_sprite('wall_128x128px.png')
    SPRITES['aim'] = get_sprite('aim_64x64px.png')
    SPRITES['player'] = get_sprite('player_128x128px.png')
    SPRITES['player_bullet'] = get_sprite('bullet_12x12px.png')
    SPRITES['bot'] = get_sprite('bot_128x128px.png')
    SPRITES['droid'] = get_sprite('droid_128x128px.png')
    SPRITES['plasma'] = get_sprite('plasma_12x12px.png')
    SPRITES['ricochet'] = get_sprite_sheet('explosion_64x64px_17frames.png', 64, 64, 17)
    SPRITES['splash'] = get_sprite_sheet('plasma_splash_128x128px_20frames.png', 128, 128, 20)
    SPRITES['blood1'] = get_sprite_sheet('blood_0_128x128px_8frames.png', 128, 128, 8)
    SPRITES['blood2'] = get_sprite_sheet('blood_1_128x128px_8frames.png', 128, 128, 8)
    SPRITES['blood3'] = get_sprite_sheet('blood_2_128x128px_10frames.png', 128, 128, 10)
    SPRITES['slime1'] = get_sprite_sheet('slime_0_128x128px_8frames.png', 128, 128, 8)
    SPRITES['slime2'] = get_sprite_sheet('slime_1_128x128px_8frames.png', 128, 128, 8)
    SPRITES['slime3'] = get_sprite_sheet('slime_2_128x128px_10frames.png', 128, 128, 10)
    SPRITES['destroy'] = get_sprite_sheet('explosion_256x256px_48frames.png', 256, 256, 48)

    # загружаем шрифты
    FONTS['regular'] = FONTS_PATH + 'Jura-Regular.ttf'

    # загружаем фоновую музыку
    MUSIC['level_1'] = SOUNDS_PATH + 'bgm_level_1.mp3'
    MUSIC['level_2'] = SOUNDS_PATH + 'bgm_level_2.mp3'
    MUSIC['level_3'] = SOUNDS_PATH + 'bgm_level_3.mp3'
    MUSIC['level_4'] = SOUNDS_PATH + 'bgm_level_4.mp3'
    MUSIC['level_5'] = SOUNDS_PATH + 'bgm_level_5.mp3'
    MUSIC['win'] = SOUNDS_PATH + 'bgm_win.mp3'

    # загружаем звуковые эффекты
    SOUNDS['alarm'] = init_sound('se_alarm.mp3')
    SOUNDS['game_over'] = init_sound('se_game_over.mp3')
    SOUNDS['explosion'] = init_sound('se_explosion.mp3')
    SOUNDS['plasma'] = init_sound('se_plasma.mp3')
    SOUNDS['reload'] = init_sound('se_reload.mp3')
    SOUNDS['shut'] = init_sound('se_shut.mp3')