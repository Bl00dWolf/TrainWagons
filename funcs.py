import qrcode
import cv2
from config import AES_KEY, IMG_NAME


def make_qrcode_datafile(filename: str, path: str) -> None:
    # Функция создает QRCode изображение в виде файла по указанному пути
    try:
        data = {}
        # Пробуем открыть файл, если не получается, то пишем ошибку
        with open(filename, encoding='UTF-8') as fl:
            for line in fl:  # Читаем каждую строку в файле
                line = line.strip()
                if line.find(' = ') != -1:  # Если строка соответствует нашему шаблону - добавляем в словарь
                    try:
                        # Считываем название города и количество вагонов из строки
                        city, wagons = line.split(' = ')[0], int(line.split(' = ')[1])
                    except ValueError:
                        # Если колво вагонов подано не как число, то пишем, что какая-то фигня
                        print(f'Неверный формат данных в строке, строка пропущена:\n{line}\n')
                    # Если вдруг город повторяется в списке - суммируем вагоны, а не перезаписываем
                    data[city] = data.setdefault(city, 0) + wagons
        if not data:
            print('Не получилось сформировать данные из файла. Скорее всего они в неверном формате\n')
            return
    except (FileNotFoundError, OSError):
        print('Файл не найден, скорее всего вы указали неверный путь\n')
        return

    qr = qrcode.make(data)
    try:
        qr.save(path)
    except OSError:
        print('Не удалось сохранить изображение с QrCode. Скорее всего вы неверно задали путь для сохранения\n')
        return


def get_data_from_QRCode_image(filename: str) -> dict:
    QRDetector = cv2.QRCodeDetector()
    try:
        data, *_ = QRDetector.detectAndDecode(cv2.imread(filename))
    except:
        print('Ошибка чтения файла, скорее всего вы выбрали неверный файл\n')
        return {}
    return data
