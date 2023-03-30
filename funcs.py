import qrcode
import cv2
from config import AES_KEY, IMG_NAME


def make_qrcode_datafile(filename: str):
    try:
        with open(filename, encoding='UTF-8') as fl:
            pass
    except FileNotFoundError as err:
        print('Файл не найден, скорее всего вы указали неверный путь\n')

    qr = qrcode.make({'Москва': 5, 'Волгоград': 10})
    qr.save(IMG_NAME)

# QRDetector = cv2.QRCodeDetector()
# data, *_ = QRDetector.detectAndDecode(cv2.imread(IMG_NAME))
