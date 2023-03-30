import funcs
import json
import time
import socket
from config import SERVER_IP, SERVER_PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # поднимаем TCP интернет соединение
print('Запускаем сервер...')
server.bind((SERVER_IP, SERVER_PORT))  # привязываемся Ип SERVER_IP и порту SERVER_PORT
print('Готовы к приему...')
server.listen()  # слушаем

print('Делайте с этими данными то, что необходимо =)\n')
while True:
    client, ip_addr = server.accept()  # Принимаем коннект

    crypt_data = b''  # для хранения данных
    done = False  # флаг
    while not done:  # пока идет передача, т.е. пока флаг False
        data = client.recv(1024)  # принимаем по 1024 байт
        if data[-6:] == b'<EOFD>':  # если видим <EOFD> значит данные закончили передавать
            done = True
        crypt_data += data  # записываем текущую порцию данных

    client.close()  # закрываем коннект с клиентом текущий

    # Декриптим обратно в json строку с помощью AES, помним что первые 32 байта это nonce для AES, для расшифровки
    AES_nonce = crypt_data[:32]  # выдираем NONCE
    crypt_data = crypt_data[32:-6]  # выдираем данные, без nonce и без <EOFD>

    norm_data = funcs.decrypt_data(crypt_data, AES_nonce) # расшифровываем данные
    norm_data = json.loads(norm_data) # переводим данные в словарь Python
    print(norm_data)
