# ПОЛОСА ЗДОРОВЬЯ

# из файла init импортируем PG(PyGame), класс SPRITE
from init import PG, SPRITE
# из файла constants импортируем размер половины юнита (чтобы смещать полосу от цента вверх на это расстояние)
from constants import HALF_UNIT_SIZE

# настройки полосы здоровья
HB_WIDTH = 100 # штртна
HB_HEIGHT = 10 # высота
HB_BORDER = 2 # толщина рамки
HB_BG_WIDTH = HB_WIDTH + HB_BORDER * 2 # ширина фона, с учетом толщины рамки с обеих сторон
HB_BG_HEIGHT = HB_HEIGHT + HB_BORDER * 2 # высота фона, с учетом толщины рамки с обеих сторон

# класс Healthbar (наследуется от класса SPRITE из библиотеки PyGame, для того чтобы можно было удалять методом .kill(), вместе с хозяином)
class Healthbar(SPRITE):
    # функция-конструктор (создает объект полосы, принимает спрайт-хозяина)
    def __init__(self, sprite):
        SPRITE.__init__(self) # вызов конструктора родительского класса (обязательно нужно делать в самом начале)
        self.sprite = sprite # в поле sprite записываем владельца, чьё здоровье нужно отображать
        self.render() # вызываем метод обновления вида полосы здоровья
    
    # метод обновления вида полосы здоровья
    def render(self):
        # ФОН
        self.image = PG.Surface((HB_BG_WIDTH, HB_BG_HEIGHT), PG.SRCALPHA) # создаем пустое изображение заданного размера с прозрачным фоном 
        self.image.fill((0, 0, 0, 85)) # заливаем его черным цветом с альфа-каналом (4-е значение, где 0 полностью прозрачный а 255 видимый) 
        self.rect = self.image.get_rect()  # создаем прямоугольник по размерам созданного изображения
        
        # ПОЛОСА ЗДОРОВЬЯ
        health = PG.Surface((self.sprite.hp, HB_HEIGHT), PG.SRCALPHA) # рисуем полосу шириной равной здоровью хозяина и заданной высоты
        if self.sprite.hp > 50 : health.fill((0, 255, 0, 128)) # если здоровье хозяина > 50% - цвет зеленый полу-прозрачный (128 из 255)
        elif self.sprite.hp > 20 : health.fill((255, 255, 0, 128)) # иначе если здоровье > 20% - цвет желтый полу-прозрачный (128 из 255)
        else : health.fill((255, 0, 0, 128)) # иначе - цвет красный полу-прозрачный (128 из 255)
        self.image.blit(health, (HB_BORDER, HB_BORDER)) # на фоновом изображении отображаем изображение полосы здоровья 

        # РАМКА
        PG.draw.rect(self.image, (0,0,0), (HB_BORDER, HB_BORDER, HB_WIDTH, HB_HEIGHT), HB_BORDER) # рисуем прямоугольную рамку поверх полосы

    # метод отрисовки полосы здоровья (принимает игровое окно)
    def draw(self, screen):
        self.rect.bottom = self.sprite.rect.centery - HALF_UNIT_SIZE # определяем координаты нижнего края полосы, относительно положения хозяина
        self.rect.centerx = self.sprite.rect.centerx # центрируем полосу по вертикали, относительно положения хозяина
        screen.blit(self.image, self.rect) # рисуем спрайт полосы здоровья в её прямоугольнике