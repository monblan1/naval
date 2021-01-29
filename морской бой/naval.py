import pygame
import pygame_widgets as pw
from pygame.sprite import Sprite
import sys
from random import randrange
from time import time
from time import sleep


class Ship:
    # Класс Ship - реализация поведения объекта корабль для игры "Морской бой"
    # свойство (указывается при создании объекта): палубность (1 - 4)
    # свойство (указывается при создании объекта):расположение (0 - горизонтальное, 1 - вертикальное)
    # свойство (указывается при создании объекта):ключевая точка (тег в формате: "столбец_строка")
    # свойство:массив со статусами точек, который формируется конструктором
    # свойство:массив с координатами точек корабля, который формируется конструктором
    # свойство:координаты точек вокруг корабля
    # свойство:статус гибели корабля
    # свойство (указывается при создании объекта):
    # префикс тега (для своих кораблей будет, например, "my", для чужих "nmy"
    # метод-конструктор:изменение массива со статусами точек, например [0,0,1,0]
    # метод:shoot(координаты точки), возвращает 1 - если попали, 2 - убил, 0 - мимо

    # свойства объектов, описанные в классе
    # длина
    length = 1
    # массив со статусами точек корабля
    status_map = []
    # массив с координатами точек корабля
    coord_map = []
    # точки вокруг корабля
    around_map = []
    # статус гибели корабля
    death = 0
    # префикс тега
    prefix = ""
    # свойство: корабль был создан и не выходит за рамки поля
    ship_correct = 1

    # метод-конструктор
    def __init__(self, length, rasp, keypoint):
        self.status_map = []
        self.around_map = []
        self.coord_map = []
        self.death = 0
        self.ship_correct = 1
        self.length = length
        # переопределить переменную self.prefix
        self.prefix = keypoint.split("_")[0]
        # создать массивы status_map и coord_map (в зависимости от направления)
        stroka = int(keypoint.split("_")[1])
        stolb = int(keypoint.split("_")[2])
        for i in range(length):
            self.status_map.append(0)
            # в зависимости от направления генерировать новые точки корабля
            # 0 - горизонт (увеличивать столбец), 1 - вертикаль (увеличивать строку)
            if ((rasp == 0) and (stolb + i > 9)) or ((rasp == 1) and (stroka + i > 9)):
                self.ship_correct = 0
            if rasp == 0:
                self.coord_map.append(self.prefix + "_" + str(stroka) + "_" + str(stolb + i))
            else:
                self.coord_map.append(self.prefix + "_" + str(stroka + i) + "_" + str(stolb))
        for point in self.coord_map:
            ti = int(point.split("_")[1])
            tj = int(point.split("_")[2])
            for ri in range(ti - 1, ti + 2):
                for rj in range(tj - 1, tj + 2):
                    if 0 <= ri <= 9 and 0 <= rj <= 9:
                        if not (self.prefix + "_" + str(ri) + "_" + str(rj) in self.around_map) and \
                                not (self.prefix + "_" + str(ri) + "_" + str(rj) in self.coord_map):
                            self.around_map.append(self.prefix + "_" + str(ri) + "_" + str(rj))

    # выстрел
    def shoot(self, shootpoint):
        # определить номер точки и изменить её статус
        status = 0
        for point in range(len(self.coord_map)):
            if self.coord_map[point] == shootpoint:
                self.status_map[point] = 1
                status = 1
                break
        if not (0 in self.status_map):
            status = 2
            self.death = 1
        return status


class Field(Sprite):
    def __init__(self, screen, x, y, width, height, indent):
        super(Field, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Установка размеров и свойств поля
        self.width, self.height = width, height
        self.field_color = (136, 149, 216)
        self.border_thickness = indent
        # Показать текущую статистику поля: 0 пусто, 1 не может быть нарисован, 2 нарисован корабль.
        # 3 выстрел
        self.status = 0

        # Построить объект поля квадрат и поместить его на поле
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.y = y
        self.rect.x = x

    def draw_field(self):
        pygame.draw.rect(self.screen, self.field_color, self.rect)


class Application:
    # Приложение.
    # Наследует класс Frame. Создание окна, холста и всех функций для реализации приложения

    # ширина рабочего поля
    width = 1600
    # высота рабочего поля
    height = 696
    # цвет фона холста
    bg = "white"
    # отступ между ячейками
    indent = 2
    # размер одной из сторон квадратной ячейки
    gauge = 46
    # смещение по y (отступ сверху)
    offset_y = 159
    # смещение по x пользовательского поля
    offset_x_user = 1011
    # смещение по x поля компьютера
    offset_x_comp = 111
    # время генерации флота
    fleet_time = 0
    # компьютерный флот
    fleet_comp = []
    # наш флот
    fleet_user = []
    # массив точек, в которые стрелял компьютер
    comp_shoot = []
    # массив точек, в которые я стрелял
    my_shoot = []
    # все мое поле
    my_fields = []
    # все поле копьютера
    nmy_fields = []
    # смещение по y (отступ сверху) расположения кнопок
    offset_y_buttons = 625
    # смещение по x кнопки "новая игра"
    offset_x_new_game = 670
    # смещение по x кнопки "авторасстановка"
    offset_x_auto = 756
    # смещение по x кнопки "выход из игры"
    offset_x_exit_game = 842

    def create_text(self, xc, yc, text, color, size):
        basicFont = pygame.font.SysFont(None, size)
        text = basicFont.render(text, False, color)
        textRect = text.get_rect()
        textRect.centerx = xc
        textRect.centery = yc
        self.screen.blit(text, textRect)
        pygame.display.update()

    def new_game(self):
        self.screen.blit(self.bg, (0, 0))
        # добавление игровых полей пользователя и компьютера
        # создание поля для пользователя
        # перебор строк
        for i in range(10):
            # перебор столбцов
            self.my_fields.append([])
            for j in range(10):
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_user
                xk = self.gauge
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                yk = self.gauge
                # добавление прямоугольника на холст с тегом в формате:
                # префикс_строка_столбец
                new_field = Field(self.screen, xn, yn, xk, yk, self.indent)
                self.my_fields[i].append(new_field)
                new_field.draw_field()

        # создание поля для компьютера
        # перебор строк
        for i in range(10):
            # перебор столбцов
            self.nmy_fields.append([])
            for j in range(10):
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                xk = self.gauge
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                yk = self.gauge
                # добавление прямоугольника на холст с тегом в формате:
                # префикс_строка_столбец
                new_field = Field(self.screen, xn, yn, xk, yk, self.indent)
                self.nmy_fields[i].append(new_field)
                new_field.draw_field()

        self.fleet_time = time()

        # генерация кораблей противника
        self.createShips("nmy")
        # генерация своих кораблей
        if auto:
            self.createShips("my")
        else:
            self.createShipsByUser("my")

    def createShips(self, prefix):
        # функция генерации кораблей на поле
        # количество сгенерированных кораблей
        count_ships = 0
        while count_ships < 10:
            # массив занятых кораблями точек
            fleet_array = []
            # обнулить количество кораблей
            count_ships = 0
            # массив с флотом
            fleet_ships = []
            # генерация кораблей (length - палубность корабля)
            for length in reversed(range(1, 5)):
                # генерация необходимого количества кораблей необходимой длины
                for i in range(5 - length):
                    # генерация точки со случайными координатами, пока туда не установится корабль
                    try_create_ship = 0
                    while 1:
                        try_create_ship += 1
                        # если количество попыток превысило 50, начать всё заново
                        if try_create_ship > 50:
                            break
                        # генерация точки со случайными координатами
                        ship_point = prefix + "_" + str(randrange(10)) + "_" + str(randrange(10))
                        # случайное расположение корабля (либо горизонтальное, либо вертикальное)
                        orientation = randrange(2)
                        # создать экземпляр класса Ship
                        new_ship = Ship(length, orientation, ship_point)
                        # если корабль может быть поставлен корректно
                        # и его точки не пересекаются с уже занятыми точками поля
                        # пересечение множества занятых точек поля и точек корабля:
                        intersect_array = list(set(fleet_array) & set(new_ship.coord_map))
                        if new_ship.ship_correct == 1 and len(intersect_array) == 0:
                            # добавить в массив со всеми занятыми точками
                            # точки вокруг корабля и точки самого корабля
                            fleet_array += new_ship.around_map + new_ship.coord_map
                            fleet_ships.append(new_ship)
                            count_ships += 1
                            break
        print(prefix, time() - self.fleet_time, "секунд")
        # отрисовка кораблей
        if prefix == "nmy":
            self.fleet_comp = fleet_ships
        else:
            self.fleet_user = fleet_ships
            self.paintShips(fleet_ships)

    def createShipsByUser(self, prefix):
        # функция генерации кораблей на поле
        # количество сгенерированных кораблей
        count_ships = 0
        while count_ships < 10:
            # массив занятых кораблями точек
            fleet_array = []
            # обнулить количество кораблей
            count_ships = 0
            # массив с флотом
            fleet_ships = []
            # генерация кораблей (length - палубность корабля)
            # расположение корабля (либо горизонтальное, либо вертикальное)
            orientation = 0
            for length in reversed(range(1, 5)):
                # генерация необходимого количества кораблей необходимой длины
                for i in range(5 - length):
                    # генерация точки со случайными координатами, пока туда не установится корабль
                    try_create_ship = 0
                    while 1:
                        try_create_ship += 1
                        # если количество попыток превысило 50, начать всё заново
                        if try_create_ship > 50:
                            break

                        cellChosed = False

                        # ждем от пользователя выбор ячейки где будет корабль
                        while not cellChosed:

                            mousePressed = False
                            # ждем пока пользователь ткнет мышкой
                            while not mousePressed:
                                events = pygame.event.get()
                                needToRedraw = False
                                for event in events:
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        mouse_x, mouse_y = pygame.mouse.get_pos()
                                        mousePressed = True
                                    # отображаем проект корабря
                                    elif event.type == pygame.MOUSEWHEEL:
                                        if orientation == 0:
                                            orientation = 1
                                            needToRedraw = True
                                        else:
                                            if orientation == 1:
                                                orientation = 0
                                                needToRedraw = True
                                    elif event.type == pygame.MOUSEMOTION:
                                        mouse_x, mouse_y = pygame.mouse.get_pos()
                                        needToRedraw = True

                                    self.exit_button.listen(events)
                                    self.exit_button.draw()
                                    self.new_button.listen(events)
                                    self.new_button.draw()
                                    self.auto_button.listen(events)
                                    self.auto_button.draw()

                                    if not self.running:
                                        return

                                    if needToRedraw:
                                        cellChosed = False
                                        for im in range(10):
                                            for jm in range(10):
                                                xn = jm * self.gauge + (jm + 1)\
                                                     * self.indent + self.offset_x_user
                                                yn = im * self.gauge + (
                                                            im + 1) * self.indent + self.offset_y
                                                xk = xn + self.gauge
                                                yk = yn + self.gauge
                                                if xn <= mouse_x <= xk and yn <= mouse_y <= yk:
                                                    cellChosed = True
                                                    break
                                                else:
                                                    mousePressed = False
                                            if cellChosed:
                                                break
                                        # если мышь над полем
                                        if cellChosed:
                                            # создаем корабль
                                            ship_point = prefix + "_" + str(im) + "_" + str(jm)

                                            # создать экземпляр класса Ship
                                            new_ship = Ship(length, orientation, ship_point)

                                            # отрисовать поле и уже существующие корабли
                                            for iv in range(10):
                                                # перебор столбцов
                                                for jv in range(10):
                                                    # добавление прямоугольника на холст с тегом
                                                    # в формате:
                                                    # префикс_строка_столбец
                                                    self.my_fields[iv][jv].draw_field()
                                            self.paintShips(fleet_ships)
                                            self.paintProjectShip(new_ship)
                                            needToRedraw = False

                                    pygame.display.update()

                            # определяем в какое поле ткнули
                            cellChosed = False
                            for im in range(10):
                                for jm in range(10):
                                    xn = jm * self.gauge + (
                                                jm + 1) * self.indent + self.offset_x_user
                                    yn = im * self.gauge + (im + 1) * self.indent + self.offset_y
                                    xk = xn + self.gauge
                                    yk = yn + self.gauge
                                    if xn <= mouse_x <= xk and yn <= mouse_y <= yk:
                                        cellChosed = True
                                        break
                                if cellChosed:
                                    break

                        # передаем на размещение
                        ship_point = prefix + "_" + str(im) + "_" + str(jm)
                        # создать экземпляр класса Ship
                        new_ship = Ship(length, orientation, ship_point)
                        # если корабль может быть поставлен корректно
                        # и его точки не пересекаются с уже занятыми точками поля
                        # пересечение множества занятых точек поля и точек корабля:
                        intersect_array = list(set(fleet_array) & set(new_ship.coord_map))
                        if new_ship.ship_correct == 1 and len(intersect_array) == 0:
                            # добавить в массив со всеми занятыми точками
                            # точки вокруг корабля и точки самого корабля
                            fleet_array += new_ship.around_map + new_ship.coord_map
                            fleet_ships.append(new_ship)
                            count_ships += 1
                            self.paintShips(fleet_ships)
                            break

        print(prefix, time() - self.fleet_time, "секунд")
        # отрисовка кораблей
        if prefix == "nmy":
            self.fleet_comp = fleet_ships
        else:
            self.fleet_user = fleet_ships
            self.paintShips(fleet_ships)

    # метод для отрисовки кораблей
    def paintShips(self, fleet_ships):
        # отрисовка кораблей
        for obj in fleet_ships:
            for point in obj.coord_map:
                if point.split('_')[0] == "my":
                    self.screen.fill(
                        (208, 185, 160),
                        self.my_fields[int(point.split('_')[1])][int(point.split('_')[2])].rect)
                    # pygame.display.update()
                if point.split('_')[0] == "nmy":
                    self.screen.fill(
                        (208, 185, 160),
                        self.nmy_fields[int(point.split('_')[1])][int(point.split('_')[2])].rect)
                    pygame.display.update()
        pygame.display.update()

        # метод для отрисовки проекта кораблей

    def paintProjectShip(self, oneShip):
        # отрисовка корабля
        for point in oneShip.coord_map:
            if point.split('_')[0] == "my":
                # проверяем не вылезли ли кубики за поле
                if not (int(point.split('_')[1]) > 9 or int(point.split('_')[2]) > 9):
                    self.screen.fill((108, 185, 160), self.my_fields[int(point.split('_')[1])][
                        int(point.split('_')[2])].rect)

    # метод рисования в ячейке креста на белом фоне
    def paintCross(self, i, j, tag):

        if tag == "nmy":
            self.screen.fill((197, 156, 191), self.nmy_fields[i][j].rect)
            pygame.display.update()
        if tag == "my":
            self.screen.fill((197, 156, 191), self.my_fields[i][j].rect)
            pygame.display.update()

    # метод рисования промаха
    def paintMiss(self, point):
        # найти координаты
        i = int(point.split("_")[1])
        j = int(point.split("_")[2])
        if point.split("_")[0] == "nmy":
            self.screen.fill((191, 199, 237), self.nmy_fields[i][j].rect)
            pygame.display.update()
        if point.split("_")[0] == "my":
            self.screen.fill((191, 199, 237), self.my_fields[i][j].rect)
            pygame.display.update()

    # метод проверки финиша
    def checkFinish(self, typee):
        # type - указание, от чьего имени идёт обращение
        status = 0
        if typee == "user":
            for ship in self.fleet_comp:
                status += ship.death
        else:
            for ship in self.fleet_user:
                status += ship.death
        return status

    # метод игры компьютера
    # параметр step - шаг, с которым происходит выстрел,
    # если он 0 - значит выстрел является первым после промаха
    # если 1 - значит надо стрелять рядом с последним выстрелом
    def compPlay(self, step=0):
        print(step)
        # если step = 0, то генерировать случайные точки
        if step == 0:
            # генерировать случайные точки,
            # пока не будет найдена пара, которой не было в списке выстрелов
            while 1:
                i = randrange(10)
                j = randrange(10)
                if not ("my_" + str(i) + "_" + str(j) in self.comp_shoot):
                    break
        else:
            # взять предпоследнюю точку, выбрать любую точку вокруг (по горизонтали или вертикали)
            # массив точек вокруг
            points_around = []
            i = int(self.comp_shoot[-1].split("_")[1])
            j = int(self.comp_shoot[-1].split("_")[2])
            for ti in range(i - 1, i + 2):
                for tj in range(j - 1, j + 2):
                    if 0 <= ti <= 9 and 0 <= tj <= 9 and ti != tj and (ti == i or tj == j) and \
                            not (ti == i and tj == j) and \
                            not ("my_" + str(ti) + "_" + str(tj) in self.comp_shoot):
                        points_around.append([ti, tj])
            # cлучайная точка из массива
            select = randrange(len(points_around))
            i = points_around[select][0]
            j = points_around[select][1]
        hit_status = 0
        for obj in self.fleet_user:
            # если координаты точки совпадают с координатой корабля, то вызвать метод выстрела
            if "my_" + str(i) + "_" + str(j) in obj.coord_map:
                # изменить статус попадания
                hit_status = 1
                # мы попали, поэтому надо нарисовать крест
                self.paintCross(i, j, "my")
                # добавить точку в список выстрелов компьютера
                self.comp_shoot.append("my_" + str(i) + "_" + str(j))
                # если метод вернул двойку, значит, корабль убит
                if obj.shoot("my_" + str(i) + "_" + str(j)) == 2:
                    hit_status = 2
                    # изменить статус корабля
                    obj.death = 1
                    # все точки вокруг корабля сделать точками, в которые мы уже стреляли
                    for point in obj.around_map:
                        # нарисовать промахи
                        self.paintMiss(point)
                        # добавить точки вокруг корабля в список выстрелов компьютера
                        self.comp_shoot.append(point)
                break
        # если статус попадания остался равным нулю - значит, мы промахнулись,
        # передать управление компьютеру
        # иначе дать пользователю стрелять
        print("hit_status", hit_status)
        if hit_status == 0:
            # добавить точку в список выстрелов
            self.comp_shoot.append("my_" + str(i) + "_" + str(j))
            self.paintMiss("my_" + str(i) + "_" + str(j))
        else:
            # проверить выигрыш, если его нет - передать управление компьютеру
            if self.checkFinish("comp") < 10:
                if hit_status == 1:
                    step += 1
                    if step > 4:
                        self.compPlay()
                    else:
                        self.compPlay(step)
                else:
                    self.compPlay()
            else:
                self.create_text(self.width / 2, self.height / 2, "Вы проиграли!", (189, 18, 18),
                                 200)

    # метод для игры пользователя
    def userPlay(self, x, y):
        for i in range(10):
            for j in range(10):
                xn = j * self.gauge + (j + 1) * self.indent + self.offset_x_comp
                yn = i * self.gauge + (i + 1) * self.indent + self.offset_y
                xk = xn + self.gauge
                yk = yn + self.gauge
                if xn <= x <= xk and yn <= y <= yk:
                    # проверить попали ли мы в корабль
                    hit_status = 0
                    for obj in self.fleet_comp:
                        # если координаты точки совпадают с координатой корабля,
                        # то вызвать метод выстрела
                        if "nmy_" + str(i) + "_" + str(j) in obj.coord_map:
                            # изменить статус попадания
                            hit_status = 1
                            # мы попали, поэтому надо нарисовать крест
                            self.paintCross(i, j, "nmy")
                            # если метод вернул двойку, значит, корабль убит
                            if obj.shoot("nmy_" + str(i) + "_" + str(j)) == 2:
                                # изменить статус корабля
                                obj.death = 1
                                # все точки вокруг корабля сделать точками, в которые мы уже стреляли
                                for point in obj.around_map:
                                    # нарисовать промахи
                                    self.paintMiss(point)
                            break
                    # если статус попадания остался равным нулю - значит, мы промахнулись,
                    # передать управление компьютеру
                    # иначе дать пользователю стрелять
                    if hit_status == 0:
                        self.paintMiss("nmy_" + str(i) + "_" + str(j))
                        # проверить выигрыш, если его нет - передать управление компьютеру
                        if self.checkFinish("user") < 10:
                            # проверить не стрелял ли уже туда
                            if not ("nmy_" + str(i) + "_" + str(j) in self.my_shoot):
                                # записать выстрел в журнал
                                self.my_shoot.append("nmy_" + str(i) + "_" + str(j))
                                # передать компьютеру
                                self.compPlay()
                        else:
                            self.create_text(self.width / 2, self.height / 2, "Вы выиграли!",
                                             (18, 189, 18), 200)
                    break

    def mainloop(self):

        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.userPlay(mouse_x, mouse_y)
            self.FPS.tick(15)
            self.exit_button.listen(events)
            self.exit_button.draw()
            self.new_button.listen(events)
            self.new_button.draw()
            self.auto_button.listen(events)
            self.auto_button.draw()

            pygame.display.update()

        if self.need_exit:
            sys.exit()
        return self.auto

    def exit_pressed(self):
        self.running = False
        self.need_exit = True

    def restart_pressed(self):
        self.running = False

    def auto_pressed(self):
        self.running = False
        self.auto = not self.auto
        sleep(1)

    def __init__(self, auto1):
        # инициализация окна
        pygame.init()
        self.auto = auto1
        self.FPS = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load("background.bmp")
        pygame.display.set_caption('Naval')
        self.running = True
        self.need_exit = False
        self.exit_button = pw.Button(
            self.screen, self.offset_x_exit_game, self.offset_y_buttons, 80, self.gauge,
            text='Выход',
            fontSize=18, margin=2,
            inactiveColour=(136, 149, 216),
            pressedColour=(136, 255, 216), radius=5,
            onClick=lambda: self.exit_pressed()
        )
        self.new_button = pw.Button(
            self.screen, self.offset_x_new_game, self.offset_y_buttons, 80, self.gauge,
            text='Заново',
            fontSize=18, margin=2,
            inactiveColour=(136, 149, 216),
            pressedColour=(136, 255, 216), radius=5,
            onClick=lambda: self.restart_pressed()
        )
        self.auto_button = pw.Button(
            self.screen, self.offset_x_auto, self.offset_y_buttons, 80, self.gauge, text='Авто',
            fontSize=18, margin=2,
            inactiveColour=(136, 149, 216),
            pressedColour=(136, 255, 216), radius=5,
            onClick=lambda: self.auto_pressed()
        )
        self.new_game()


auto = False

# инициализация приложения
while True:
    app = Application(auto)
    auto = app.mainloop()
