
import os
from datetime import datetime
from PIL import Image, ImageFilter, ImageStat

input_path = "Lab2_Media/data/input/"
output_path = "Lab2_Media/data/output/"
log_path = "Lab2_Media/logs/history.txt"


#Box-фильтр (усреднение)
def box_filter(image):
    kernel = [1, 1, 1,
              1, 1, 1,
              1, 1, 1]
    #применяем фильтр к изображению
    result = image.filter(ImageFilter.Kernel((3, 3),kernel,scale=9))

    return result


#баланс белого (метод Серого мира)
def gray_world(image):
    #получаем средние значения каждого цветового канала
    stat = ImageStat.Stat(image)
    red, green, blue = stat.mean

    #находим общее среднее значение
    average = (red + green + blue) / 3

    #вычисляем коэффициенты коррекции для каждого цвета
    red_coef = average / red if red != 0 else 1
    green_coef = average / green if green != 0 else 1
    blue_coef = average / blue if blue != 0 else 1

    #разделяем изображение
    r, g, b = image.split()

    #изменяем яркость каждого с помощью коэффициентов
    r = r.point(lambda x: min(255, int(x * red_coef)))
    g = g.point(lambda x: min(255, int(x * green_coef)))
    b = b.point(lambda x: min(255, int(x * blue_coef)))

    #соединяем обратно в одно изображение
    result = Image.merge("RGB", (r, g, b))

    return result


#записываем информацию в журнал
def zapis_v_log(name, filter_name, status):
    #получаем текущую дату и время
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    #открываем файл
    with open(log_path, "a", encoding="UTF-8") as file:
        file.write(
            f"[{time}] Файл: {name} | "
            f"Фильтр: {filter_name} | "
            f"Статус: {status}\n")


#основная обработка изображения
def obrabotka(name):
    #формируем полный путь к изображению
    full_path = os.path.join(input_path, name)

    try:
        #пытаемся открыть изображение
        with Image.open(full_path) as image:
            #загружаем изображение в память
            image.load()

            #переводим изображение в формат RGB
            image = image.convert("RGB")

    #если нет прав на чтение
    except PermissionError:
        print(
            f"Ошибка: Нет прав на чтение файла {name}. "
            "Обратитесь к администратору")
        zapis_v_log(name, "Box-фильтр + Серый мир", "Ошибка доступа")
        return

    #если файл не существует
    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        zapis_v_log(name, "Box-фильтр + Серый мир", "Файл не найден")
        return

    #если файл поврежден или не является изображением
    except (OSError, ValueError):
        print("Ошибка: Не удалось открыть изображение")
        zapis_v_log(name, "Box-фильтр + Серый мир", "Ошибка обработки")
        return

    result = box_filter(image)

    result = gray_world(result)

    try:
        result.save(output_path + "result.jpg", format="JPEG")

        print("Изображение успешно обработано!")
        print("Результат сохранен в data/output/result.jpg")

        zapis_v_log(name, "Box-фильтр + Серый мир", "Успешно")

    except (PermissionError, OSError):
        print("Ошибка: Не удалось сохранить изображение")
        zapis_v_log(name, "Box-фильтр + Серый мир", "Ошибка сохранения")


while True:
    name = input("(Для выхода напишите Esc) | Какой файл обработать: ")

    if name.strip() == "Esc":
        break

    #лишние пробелы
    name = name.strip()

    if not name:
        print("Ошибка: Имя файла не указано")
        continue

    obrabotka(name)
