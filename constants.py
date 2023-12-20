# ИГРОВЫЕ НАСТРОЙКИ (константы)

# размеры экрана
SCREEN_WIDTH = 1280 # ширина
SCREEN_HEIGHT = 768 # высота

# размер условной ячейки игрового окна (128x128px)
CEIL_SIZE = 128

# частота обновления экрана
FPS = 60

# максимальный показатель здоровья всех юнитов
UNIT_HP = 100 # %

HALF_UNIT_SIZE = 64 # половина размера всех юнитов
# (для появления пуль, при стрельбе, на краю спрайта, для смещения полосы здоровья выше центра и пр.)

LEVEL_END_TIMEOUT = 2.4 # время до входа в меню после окончания уровня (секунд) 

# настройки игрока
PLAYER_ARMOR = 5 # на это число делится урон от вражеской атаки
PLAYER_SPEED = 3 # пикселей за 1 FPS
PLAYER_BULLET_SPEED = 12 # пикселей за 1 FPS
PLAYER_BULLET_POWER = 10 # урон, наносимый врагам
PLAYER_SHUT_TIMEOUT = 0.16 # время да нового выстрела при стрельбе (секунд)
PLAYER_RELOAD_TIMEOUT = 2.4 # время перезарядки оружия (секунд)
PLAYER_BULLETS = 24 # патронов в обойме

# настройки ботов
BOT_PLASMA_SPEED = 12 # пикселей за 1 FPS
BOT_PLASMA_POWER = 10 # урон, наносимый игроку
# bot
BOT_ARMOR = 2 # на это число делится урон от атаки игрока
BOT_SPEED = 3 # пикселей за 1 FPS
BOT_PLASMA_MIN_TIMEOUT = 0.12 # минимальное время да нового выстрела при стрельбе (секунд)
BOT_PLASMA_MAX_TIMEOUT = 2.4  # максимальное время да нового выстрела при стрельбе (секунд)
# droid
DROID_ARMOR = 5 # на это число делится урон от атаки игрока
DROID_SPEED = 4 # пикселей за 1 FPS
DROID_PLASMA_MIN_TIMEOUT = 0.12 # минимальное время да нового выстрела при стрельбе (секунд)
DROID_PLASMA_MAX_TIMEOUT = 1.2  # максимальное время да нового выстрела при стрельбе (секунд)
# cyborg
CYBORG_ARMOR = 10 # на это число делится урон от атаки игрока
CYBORG_SPEED = 2 # пикселей за 1 FPS
CYBORG_PLASMA_MIN_TIMEOUT = 0.06 # минимальное время да нового выстрела при стрельбе (секунд)
CYBORG_PLASMA_MAX_TIMEOUT = 1.2  # максимальное время да нового выстрела при стрельбе (секунд)
# spider
SPIDER_ARMOR = 1 # на это число делится урон от атаки игрока
SPIDER_SPEED = 5 # пикселей за 1 FPS
SPIDER_POWER = 10 # урон, наносимый игроку
SPIDER_TIMEOUT = 1.2  # время ожидания после нанесения урона игроку