# gamelife
Игра жизнь
# Что это?
Место действия этой игры, «вселенная» - это размеченная на клетки поверхность, безграничная, ограниченная или замкнутая. Каждая клетка на этой поверхности может находиться в двух состояниях: быть живой или быть мертвой. Клетка имеет восемь соседей. Распределение живых клеток в начале игры называется первым поколением. Все что предоставляется в игре - это наблюдение за эволюцией клеток
# Правила
- Пустая(мертвая) клетка ровно с тремя живыми клетками-соседями оживает.
- Если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить; В противном случае(если соседок меньше двух или больше трех) клетка умирает(от «одиночества» или от «перенаселенности»). 
- Игрок не принимает прямого участия в игре, а лишь расставляет «живые» клетки, которые взаимодействуют согласно правилам без его участия. 
# Как запустить 
Запустить файл Init.py либо импортировать класс GameLife и вызвать метод run()
# Использованные пакеты
- pygame
- random
- sys
# Разработчик
Половинкина Дарья

