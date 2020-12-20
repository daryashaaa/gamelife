import random
import sys
import pygame

class GameLife:
    def __init__(self, screen_width=800, screen_height=600, cell_size=10, alive_color=(0, 255, 255),
                 dead_color=(0, 0, 0), max_fps=10):
        """
        Инициализировать сетку, установить состояние игры по умолчанию, инициализировать экран
        :param screen_width: Ширина игрового окна
        :param screen_height: Высота игрового окна
        :param cell_size: Диаметр кругов
        :param alive_color: цвет RGB, например (255 ,255,255) для живых клеток
        :param dead_color: цвет RGB, мертвые клетки
        :param max_fps: максимальное количество кадров в секунду
        """
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.alive_color = alive_color
        self.dead_color = dead_color

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clear_screen()
        pygame.display.flip()

        self.max_fps = max_fps

        self.active_grid = 0
        self.num_cols = int(self.screen_width / self.cell_size)
        self.num_rows = int(self.screen_height / self.cell_size)
        self.grids = []
        self.init_grids()
        self.set_grid()

        self.paused = False
        self.game_over = False

    def init_grids(self):
        """
        Создание и сохранение активной и неактивной сетки по умолчанию
        :return:
        """

        def create_grid():
            """
            Создать пустую сетку
            :return:
            """
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows

        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def set_grid(self, value=None, grid=0):
        """
        Устанавливает сразу всю сетку(в зависимости от аргументов 0/1, поддержка случайных чисел).
        Пример:
          set_grid(0) # все клетки мертвы
          set_grid(1) # все живы
          set_grid() # случайные клетки
          set_grid(None) # так же случайное распределение
        :param grid: Индекс сетки, для активного / неактивного (0 или 1)
        :param value: Значение, чтобы установить для ячейки значение (0 или 1)
        :return:
        """
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value

    def draw_grid(self):
        """
        Учитывая состояние сетки и ячеек, нарисует ячейки на экране
        :return:
        """
        self.clear_screen()
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                # если клетка живая, то рисуем цвет живой клетки, иначе цвет неживой
                if self.grids[self.active_grid][r][c] == 1:
                    color = self.alive_color
                else:
                    color = self.dead_color
                pygame.draw.circle(self.screen,
                                   color,
                                   (int(c * self.cell_size + (self.cell_size / 2)),
                                    int(r * self.cell_size + (self.cell_size / 2))),
                                   int(self.cell_size / 2),
                                   0)
        pygame.display.flip()

    def clear_screen(self):
        """
        Заполнить весь экран мертвым цветом
        :return:
        """
        self.screen.fill(self.dead_color)

    def get_cell(self, row_num, col_num):
        """
        Получить живое / мертвое (0/1) состояние определенной ячейки в активной сетке
        :param row_num: номер стобца
        :param col_num: номеря колонки
        :return: 0 или 1 в зависимости от состояния ячейки. По умолчанию 0 (мертвый)
        """
        try:
            cell_value = self.grids[self.active_grid][row_num][col_num]
        except:
            cell_value = 0
        return cell_value

    def check_cell_neighbors(self, row_index, col_index):
        """
        Получение количество живых соседних ячеек и определение состояние ячейки
        для следующего поколения. Определяет, живет ли он, умирает, выживает или рождается.
        :param row_index: Номер строки ячейки для проверки
        :param col_index: Номер столбца ячейки для проверки
        :return: Состояние, в котором ячейка должна быть в следующем поколении (0 или 1)
        """
        num_alive_neighbors = 0  # количество живых клеток вокруг нашей клетки
        # подсчитываем вокруг клетки живые, всего 8 мест где могут они находиться
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        # Правила смерти или жизни
        if self.grids[self.active_grid][row_index][col_index] == 1:  # живоое если
            if num_alive_neighbors > 3:  # если Перенаселение, то мертв
                return 0
            if num_alive_neighbors < 2:  # Мало живых соседей, мертв
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0:  # если мертв
            if num_alive_neighbors == 3:  # но имеет три соседа
                return 1  # возвращение к жизни

        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        """
        Проверяет состояние текущего поколения, подготавливает следующее поколение
        :return:
        """
        self.set_grid(0, self.inactive_grid())
        for r in range(self.num_rows - 1):
            for c in range(self.num_cols - 1):
                next_gen_state = self.check_cell_neighbors(r, c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        """
        Простая вспомогательная функция для получения индекса неактивной сетки
        Если активная сетка равна 0, вернется 1 и наоборот
        :return:
        """
        return (self.active_grid + 1) % 2

    def handle_events(self):
        """
        Обработка любых нажатий клавиш и мыши
        s/ы - старт/начало
        q/й - выход
        r/к - случайные значения на сетке
        :return:
        """
        for event in pygame.event.get():
            # если нажата кнопка мыши левая, то помещаем туда живую клетку предаврительно поставив игру на паузу
            if pygame.mouse.get_pressed()[0]:
                self.paused = True
                x, y = pygame.mouse.get_pos()
                for c in range(self.num_cols):
                    for r in range(self.num_rows):
                        # делим координаты мыши на 10, получая целое число
                        dx = x // 10
                        dy = y // 10
                        if dx == c and dy == r:
                            self.grids[self.active_grid][r][c] = 1
                            self.draw_grid()
            # если нажата правая кнопка мыши, то убираем живую клетку с этого места(где установлена мышь)
            # предварительноо поставив на паузу
            if pygame.mouse.get_pressed()[2]:
                self.paused = True
                x, y = pygame.mouse.get_pos()
                for c in range(self.num_cols):
                    for r in range(self.num_rows):
                        # делим координаты мыши на 10, получая целое число
                        dx = x // 10
                        dy = y // 10
                        if dx == c and dy == r:
                            self.grids[self.active_grid][r][c] = 0
                            self.draw_grid()
            # кнопки для управления игрой, т.е. паузка - случайное расположение живых клеток - выход
            if event.type == pygame.KEYDOWN and event.type != pygame.MOUSEBUTTONDOWN:
                print("Нажата клавиша")
                if event.unicode == 's' or event.unicode == 'ы':
                    if self.paused:
                        self.paused = False
                        print("Старт.")
                    else:
                        self.paused = True
                        print("Паузка.")
                elif event.unicode == 'r' or event.unicode == 'к':
                    print("Случайные клетки.")
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid)  # случайное распределение
                    self.set_grid(0, self.inactive_grid())  # задать 0
                    self.draw_grid()
                elif event.unicode == 'q' or event.unicode == 'й':
                    print("Выход.")
                    self.game_over = True
                elif event.unicode == 't' or event.unicode == 'е':
                    self.active_grid = 0
                    self.set_grid(0, self.active_grid)
                    self.set_grid(0, self.inactive_grid())
                    self.clear_screen()
                    print('очистка')
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        """
        Запуск игры
        :return:
        """
        # получаем объект время для ограничения кадров
        clock = pygame.time.Clock()
        # ставим игру на паузу
        self.paused = True
        # запускаем бесконечный цикл
        while True:
            # если игра завершена, завершаем функцию
            if self.game_over:
                return
            # вызываем функцию в которой описаны ситуации с кнопками и действиями пользователя
            self.handle_events()
            # если игра не на паузе, то производим вызов функции обновляющую популяцию, следующеее поколение
            if not self.paused:
                self.update_generation()
            # вызов функции отрисовки на экран
            self.draw_grid()
            # ограничеие на кадры в секунду
            clock.tick(self.max_fps)

