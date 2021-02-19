import configparser
import os
from PIL import Image, ImageFile

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")  # читаем конфиг

maximum_size = config['DEFAULT'].getint('maximum_size')  # импорт из конфига
quality = config['DEFAULT'].getint('quality')
count = 0 if config["DEFAULT"].getint('count_of_photos') != 0 else -1  # создание счетчика
ImageFile.LOAD_TRUNCATED_IMAGES = True


def print_log(text):  # функция вывода в консоль
    if config['extra'].getboolean('log_console'):
        print(text)


for files in os.walk(os.getcwd()):  # проход по дереву всех файлов
    path = files[0]
    for file in files[-1]:  # отсекаем папки
        if file.split('.')[1] in config['DEFAULT']['image_formats'].split():  # проверяем формат из конфига
            if count < config["DEFAULT"].getint('count_of_photos') or count == -1:
                current_path = '{}\\{}'.format(path, file)
                im = Image.open(current_path)
                (width, height) = im.size  # узнаем разрешение фото

                if max(width, height) > maximum_size > 0:  # изменение размера
                    coefficient = max(width, height) / maximum_size
                    image = im.resize((int(width / coefficient), int(height / coefficient)), Image.ANTIALIAS)
                    image.save(current_path, quality=quality) if quality != 0 else image.save(current_path)

                    print_log(
                        '{}\nsize: {} x {}\ncoefficient: {}\ntotal size: {} x {}\nquality: {}\n'.format(current_path,
                                                                                                        width, height,
                                                                                                        coefficient,
                                                                                                        int(
                                                                                                            width / coefficient),
                                                                                                        int(
                                                                                                            height / coefficient),
                                                                                                        quality if quality != 0 else 'without changes'))
                    if count != -1:
                        count += 1
                elif bool(max(width,
                              height) == maximum_size or maximum_size == 0) and 100 > quality > 0:  # изменение сжатия
                    im.save(current_path, quality=quality)
                    print_log('{}\nsize: {} x {}\nquality: {}\n'.format(current_path, width, height, quality))
                    if count != -1:
                        count += 1
