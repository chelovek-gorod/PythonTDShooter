# Импортируем pygame в переменную PG
import pygame as PG
PG.init() # инициализируем pygame (без этого не работают шрифты и некоторый функционал)

# функция для загрузки спрайтов (из одиночной картинки)
def get_sprite(file_name):
    # возвращаем загруженное изображение с прозрачным фоном (если фон у изображения прозрачный)
    return PG.image.load(SPRITES_PATH + file_name).convert_alpha()

# функция для загрузки анимированных спрайтов (в одном изображении собрано несколько кадров)
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

# создаем переменные с путями расположения (папки) спрайтов, звуков и шрифтов
SPRITES_PATH = './src/sprites/'
SOUNDS_PATH = './src/sounds/'
FONTS_PATH = './src/fonts/'

# создаем словарь со спрайтами
SPRITES = {}

# функция инициализации (загрузки) игровых ресурсов (спрайты, звуки и шрифты)
def init_src():
    SPRITES['player'] = get_sprite('player_128x128px.png')
    SPRITES['explosion'] = get_sprite_sheet('explosion_128x128px_20frames.png', 128, 128, 20)