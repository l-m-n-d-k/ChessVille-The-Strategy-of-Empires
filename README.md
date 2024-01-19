# Пояснительная записка к проекту: ChessVille-The-Strategy-of-Empires

## Описание:
Проект "ChessVille-The-Strategy-of-Empires" представляет собой стратегическую игру для двух игроков, объединяющую элементы таких игр, как "Sid Meier's Civilization V", "Шахматы" и "Heroes of Might and Magic V". Игрокам предстоит управлять отрядами воинов, перемещаясь по карте, вступая в бои и захватывая вражеские отряды. Победителем становится тот, кто сможет покорить всех трех воинов противника, при этом бои проводятся по правилам шахмат.

## Реализация:
### 1. Создание основной карты:
Основная карта создана с использованием текстовых файлов или файлов CSV, позволяя игрокам перемещаться по карте и взаимодействовать с вражескими юнитами.

### 2. Иконки персонажей и перемещение:
Реализовано создание трех иконок персонажей игрока, каждый из которых может перемещаться по карте. При клике мыши персонажи перемещаются на клетки в зависимости от их типа, с развитием тумана войны.

### 3. Всплывающее окошко:
Добавлено всплывающее окошко для отображения войск при наведении курсора мыши на свой или вражеский отряд, обеспечивая игрокам информацию о силе войск.

### 4. Система боя:
На данном этапе ироки имеют возможность стажаться за счет своей боевой мощи. Она распределяется следующим образом:
* Король: 0
* Ферзь: 9
* Ладья: 5
* Слон: 3
* Конь: 3
* Пешка: 1

### 5. Титры и меню:
В игре присутствует главное меню, в которое можно войти при нажатии на Esc или на кнопку в левом верхнем углу, и титры, восхваляющие победившего игрока.

### 6. Механики в игре:
Основное поле. На основном поле есть клетки с разным видом рельефа: поля холмы, реки, горы. На клетки с горой ходить нельзя, клетки с рекой и холмом затрачивают 2 ОП*, клетка с полем затрачивает 1 ОП. Также есть туман войны, который скрывает рельеф и существ клетки.

Пауза. В левом верхнем углу есть кнопка для вызова паузы, при нажатии на неё появляется окошко, из которого можно выйти в главное меню либо продолжить игру.

Юниты. В игре есть 6 типов юнитов: 3 вида союзных героев, 3 вида вражеских героев, 2 вида нейтральных юнитов. Каждому из игроков достанутся свои 3 героя, действиями которых он может управлять. У каждого героя и нейтрального юнита есть своя армия. которая выдаётся в начале игры. Героям доступно 4 или 6 ОП в зависимости от типа героя, у одного из героев перемещение по холмам занимает 1 ОП, у другого перемещение по рекам занимает 1 ОП. Обзор у героев 3 или 4 клетки, также зависит от типа героя. Нападение на нейтральных юнитов тратит 2 ОП. При победе над нейтральным юнитом пользователь может забрать войска из отряда нейтрального юнита, пока не превысит лимит для своего отряда  в 20 фигур. При превышении данного лимита войска набирать дальше будет нельзя, но будет возможность удалить часть слабых фигур, чтобы взять на их место сильные. При поражении в бою герой безвозвратно утерян, при поражении всех 3 героев игрок проигрывает.

Миникарта. На миникарте в правом нижнем углу можно увидеть всю карту целиком, с использованием условных обозначений.

Иконки героев. При нажатии на иконку героя ты фокусируешься на нём , можешь совершать им действия. Иконка выбранного игрока выделяется красным, а при поражении зачёркивается крестом.

Табличка кратких характеристик. В левом нижнем углу есть табличка, в которой можно увидеть доступные ОП и свою боевую мощь.

Кнопки "Юнит ждёт приказа" и "Следующий ход". Пока у кого-то из союзных героев есть ОП, кнопка переходит в состояние "Юнит ждёт приказа", при нажатии на неё камера фокусируется на герое, у которого остались ОП. Когда у всех героев кончаются ОП, кнопка превращается в "Следующий ход". При нажатии на неё, ход переходит к другому игроку.

Кнопка ожидания левее от миникарты. Создана для того, чтобы обнулить очки передвижения выбранного героя.

Кнопка обмена войсками левее от миникарты. Создана для того, чтобы меняться войсками между союзными героями, если они находятся рядом.

Окошко характеристик при наведении на юнитов. При наведении на любого юнита появляется окошко характеристик, по которому можно узнать об отряде юнита и его боевой мощи с очками передвижения.


  *ОП - очки передвижения

## Используемые библиотеки:
pygame версии 2.5.0

## Инструкция по запуску:
* Скачайте все необходимые зависимости командой ```pip install -r requirements.txt```
* После скачиваний всех зависимойстей игра должна работать корректно, запуск производится через файл ```ChessVille.exe```

## Перспективы проекта:
Добавение функций шахматного боя, улкчшение графики и оптимизация игры

