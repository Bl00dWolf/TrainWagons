import qrcode
import cv2
from config import AES_KEY, IMG_NAME


def make_qrcode_datafile(filename: str, path: str) -> None:
    # Функция создает QRCode изображение в виде файла по указанному пути
    try:
        data = {}
        # Пробуем открыть файл, если не получается, то пишем ошибку
        with open(filename, encoding='UTF-8') as fl:
            for line in fl.readline().strip():  # Читаем каждую строку в файле
                if line.find(' = ') != -1:  # Если строка соответствует нашему шаблону - добавляем в словарь
                    city, wagons = line.split(' = ')[0], int(line.split(' = ')[1])
                    data[city] = data.setdefault(city, 0) + wagons
        if not data:
            print('Не получилось сформировать данные из файла. Скорее всего они в неверном формате\n')
            return
    except FileNotFoundError:
        print('Файл не найден, скорее всего вы указали неверный путь\n')
        return

    qr = qrcode.make(data)
    qr.save(IMG_NAME)

# QRDetector = cv2.QRCodeDetector()
# data, *_ = QRDetector.detectAndDecode(cv2.imread(IMG_NAME))
