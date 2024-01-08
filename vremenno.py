from PIL import Image


def darken_image(file_name, output_name):
    # Открываем исходное изображение
    image = Image.open(file_name)

    # Создаем новый пустой объект Image с такими же размерами и параметрами
    darkened_image = Image.new(image.mode, image.size)

    # Получаем данные пикселей для манипуляции
    pixels = image.load()
    darkened_pixels = darkened_image.load()

    # Проходимся по каждому пикселю изображения
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # Получаем значения RGB и применяем затемнение
            r, g, b = pixels[i, j]
            darkened_r = max(r - 30, 0)
            darkened_g = max(g - 30, 0)
            darkened_b = max(b - 30, 0)

            # Записываем затемненный пиксель в новое изображение
            darkened_pixels[i, j] = (darkened_r, darkened_g, darkened_b)

    # Сохраняем измененное изображение под новым именем
    darkened_image.save(output_name)


def convert_white(file_name, output_name):
    # Открываем исходное изображение
    image = Image.open(file_name)

    # Создаем новый пустой объект Image с такими же размерами и параметрами
    darkened_image = Image.new(image.mode, image.size)

    # Получаем данные пикселей для манипуляции
    pixels = image.load()
    darkened_pixels = darkened_image.load()

    # Проходимся по каждому пикселю изображения
    print(image.size)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # Получаем значения RGB и применяем затемнение
            r, g, b, *c = pixels[i, j]
            try:
                r1, g1, b1, *c = pixels[i + 10, j]
                r2, g2, b2, *c = pixels[i - 10, j]
                if (r >= 180 and g >= 180 and b >= 180) and all((not(r1 >= 180 and g1 >= 180 and b1 >= 180), not(r2 >= 180 and g2 >= 180 and b2 >= 180))):
                    darkened_pixels[i, j] = (r - 20, g - 20, b - 20)
                    continue
                else:
                    if r >= 180 and g >= 180 and b >= 180:
                        r = 255
                        g = 255
                        b = 255
                    darkened_pixels[i, j] = (r, g, b)
            except Exception:
                if r >= 180 and g >= 180 and b >= 180:
                    r = 255
                    g = 255
                    b = 255
                darkened_pixels[i, j] = (r, g, b)

            # Записываем затемненный пиксель в новое изображение

    # Сохраняем измененное изображение под новым именем
    darkened_image.save(output_name)


# Пример использования функции
darken_image('data/Кнопка ожидания.png', 'data/Зажатая кнопка ожидания.png')
darken_image('data/Следующий ход.png', 'data/Зажатый следующий ход.png')
darken_image('data/Ожидание приказа.png', 'data/Зажатое ожидание приказа.png')
darken_image('data/Кнопка характеристик.png', 'data/Зажатая кнопка характеристик.png')
convert_white('data/Анимация таймера.png', 'data/Анимация таймера.png')
