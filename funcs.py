import qrcode
import cv2
from Crypto.Cipher import AES
from config import AES_KEY, AES_NONCE
import json


# Этот файл содержит в себе все основные функции для работы программы

def make_qrcode_datafile(filename: str, path: str) -> None:
    # Готовим строку с данными
    data = ''
    try:
        # Пробуем открыть файл
        with open(filename, encoding='UTF-8') as fl:
            for line in fl:  # Обрабатываем каждую строку файла
                if line.find(' = ') != -1:  # Если строка соответствует нашему шаблону - добавляем в data
                    data += line
    except (FileNotFoundError, OSError):
        print('Файл не найден, скорее всего вы указали неверный путь\n')
        return

    qr = qrcode.make(data)  # добавляем дату в QR код
    try:
        qr.save(path)  # пробуем сохранить изображение с QR кодом
    except OSError:
        print('Не удалось сохранить изображение с QrCode. Скорее всего вы неверно задали путь для сохранения\n')
        return


def get_data_from_QRCode_image(filename: str) -> str:
    QRDetector = cv2.QRCodeDetector()
    try:
        data, *_ = QRDetector.detectAndDecode(cv2.imread(filename))
    except:
        print('Ошибка чтения файла, скорее всего вы выбрали неверный файл\n')
        return ''
    return data


def crypt_data(data: str) -> bytes:
    cipher = AES.new(AES_KEY, AES.MODE_EAX, AES_NONCE)
    return cipher.encrypt(f"{data}".encode(encoding='UTF-8'))


def decrypt_data(data: bytes) -> dict | str:
    cipher = AES.new(AES_KEY, AES.MODE_EAX, AES_NONCE)
    return cipher.decrypt(data).decode(encoding='UTF-8')
