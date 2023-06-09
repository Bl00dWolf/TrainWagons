import qrcode
import cv2
import socket
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from config import AES_KEY, CLIENT_IP, CLIENT_PORT, SRV_TURNOFF_KEY


# Этот файл содержит в себе все основные функции для работы программы

def make_qrcode_datafile(filename: str, path: str) -> None:
    """
    Преобразует сырые данные, согласно шаблона, из файла в изображение с QR кодом и сохраняет его на диск
    :param filename: файл с сырыми данными, небоходимо указать полный путь, включая имя самого файла
    :param path: путь для сохранения изображения с qr code, включая имя файла
    :return: None
    """
    # Готовим строку с данными
    data = ''
    try:
        # Пробуем открыть файл
        with open(filename, encoding='UTF-8') as fl:
            for line in fl:  # Обрабатываем каждую строку файла
                if line.find(' = ') != -1:  # Если строка соответствует нашему шаблону - добавляем в data
                    data += line
    except (FileNotFoundError, OSError):
        print('[ERROR] Файл не найден, скорее всего Вы указали неверный путь\n')
        return

    qr = qrcode.make(data)  # добавляем дату в QR код
    try:
        qr.save(path)  # пробуем сохранить изображение с QR кодом
    except OSError:
        print('[ERROR] Не удалось сохранить изображение с QrCode. Скорее всего Вы неверно задали путь для сохранения\n')
        return

    # эта штука более продвинутая, как вариант, можно вывести QR Code в ASCII прямо в терминал =)
    # qr2 = qrcode.QRCode()
    # qr2.add_data(data)
    # qr2.print_ascii()


def get_data_from_QRCode_image(filename: str) -> str:
    """
    Считывает сырые данные из изображения с QR кодом
    :param filename: полный путь до файла, включая имя файла
    :return: строку с сырыми данными
    """
    QRDetector = cv2.QRCodeDetector()
    try:
        data, *_ = QRDetector.detectAndDecode(cv2.imread(filename))
    except:
        print('[ERROR] Ошибка чтения файла, скорее всего Вы выбрали неверный файл\n')
        return ''
    return data


def crypt_data(data: str) -> tuple[bytes, bytes]:
    """
    Шифрует данные (в виде строки) с помощью AES с применением заданного ключа и возвращает зашифрованную
    последовательность байт и nonce
    :param data: принимает строку с данными
    :return: возвращает зашифрованную последовательность байт и сгенерированный nonce (32 байта) в виде tuple
    """
    cipher = AES.new(AES_KEY, AES.MODE_EAX, get_random_bytes(32))
    return cipher.encrypt(data.encode(encoding='UTF-8')), cipher.nonce


def decrypt_data(data: bytes, nonce: bytes) -> str:
    """
    Расшифровывает данные (в виде последовательности байтов) с помощью AES с применением заданного ключа и nonce
    и возвращает расшифрованную строку
    :param nonce: сессионный nonce в виде байт 16 или 32 байта
    :param data: принимает зашифрованную строку в виде последовательности байт
    :return: возвращает расшифрованную строку с данными
    """
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce)
    return cipher.decrypt(data).decode(encoding='UTF-8')


def make_dict_from_data(raw_data: str) -> dict:
    """
    Преобразует сырые данные в понятный для Python словарь
    :param raw_data: сырые данные вида "Город" = число
    :return: словарь вида {'Город': число}
    """
    data = {}
    for line in raw_data.split('\n'):
        if line.find(' = ') != -1:
            try:
                city, wagons = line.split(' = ')[0], int(line.split(' = ')[1])
                data[city] = data.setdefault(city, 0) + wagons
            except ValueError:
                print(f'[ERROR] Ошибка в строке, строка будет пропущена: {line.strip()}')
    print('\n')
    return data


def send_data_to_server(crypted_data: bytes) -> None:
    """
    Передача байтовых данных на сервер. Последовательность завершения передачи данных - b'<EOFD>'
    :param crypted_data: зашифрованные данные
    :return: None
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP интернет сокет
    try:
        client.connect((CLIENT_IP, CLIENT_PORT))  # коннектимся по ип и по порту
    except ConnectionRefusedError:
        print('[ERROR] Не удалось установить соединение с сервером. Проверьте данные для подключения\n')
        return

    print('Передаем данные\n')
    # client.send(b'<START_OF_DATA_FILE>') # начала файла никак не обозначается. Надо ли это делать?
    client.sendall(crypted_data)
    client.send(b'<EOFD>')
    client.close()
    print('[INFO] Данные переданы успешно\n')


def server_exit_program() -> None:
    """
    Отправляет команду завершения работы программы на сервер.
    :return: None
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP интернет сокет
    try:
        client.connect((CLIENT_IP, CLIENT_PORT))  # коннектимся по ип и по порту
    except ConnectionRefusedError:
        print('[ERROR] Не удалось установить соединение с сервером. Проверьте данные для подключения\n')
        return

    # шифруем ключ, получаем шифрованный ключ и nonce
    cr_key, nonce = crypt_data(SRV_TURNOFF_KEY.decode(encoding='UTF-8'))

    print('[INFO] Передаем последовательность отключения')
    client.sendall(b'<ESCOF>' + nonce + cr_key + b'</ESCOF>')


def srv_read_json(json_file) -> dict:
    """
    Возвращает словать Python из json файла. В противном случае возвращает пустой словарь.
    :param json_file: json файл
    :return: словарь Python из json файла
    """
    data = {}
    try:
        with open(json_file, encoding='UTF-8') as fl:
            try:
                data = json.load(fl)
            except json.JSONDecodeError:
                print('[ERROR] Данные в файле повреждены и не могут быть считаны. Файл будет перезаписан на этапе записи.')
    except FileNotFoundError:
        print('[INFO] Файла с данными нет. Он будет создан на этапе записи.')
    return data


def srv_write_json(json_file, cur_data: dict, new_data: dict) -> None:
    """
    Обноаляет старые данные, если они есть и заносит все в json файл.
    :param json_file: файл JSON
    :param cur_data: текущие данные из файла JSON
    :param new_data: новые данные для записи в JSON
    """
    try:
        for city, value in new_data.items():
            cur_data[city] = cur_data.setdefault(city, 0) + new_data[city]
        with open(json_file, 'w', encoding='UTF-8') as fl:
            json.dump(cur_data, fl, indent=3)
    except:
        print(f'[ERROR] Не удалось создать файл. Возможно переменная конфигурации SRV_RECORDS_FILE задана наверно\n'
              f'SRV_RECORDS_FILE = {json_file}')
