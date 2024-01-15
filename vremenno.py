from PIL import Image

# Открываем изображение
img = Image.open('Фото персонажей/Герои вариант 3.png')

# Обрезаем изображение (left, upper, right, lower)
animation_hero_1 = img.crop((-5, 905, 970, 1005))
icon_hero_1 = img.crop((-5, 1020, 70, 1125))

animation_hero_2 = img.crop((-5, 240, 760, 340))
icon_hero_2 = img.crop((-5, 360, 70, 465))

animation_hero_3 = img.crop((1025, 245, 1950, 345))
icon_hero_3 = img.crop((1025, 365, 1105, 470))

# Сохраняем обрезанное изображение
animation_hero_1.save('Фото персонажей/Герой 1.png')
icon_hero_1.save('Фото персонажей/Герой 1 иконка.png')
animation_hero_2.save('Фото персонажей/Герой 2.png')
icon_hero_2.save('Фото персонажей/Герой 2 иконка.png')
animation_hero_3.save('Фото персонажей/Герой 3.png')
icon_hero_3.save('Фото персонажей/Герой 3 иконка.png')
