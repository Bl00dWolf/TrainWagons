import funcs
import json
import socket
from config import SERVER_IP, SERVER_PORT, SRV_TURNOFF_KEY, SRV_RECORDS_FILE

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
        if data.endswith(b'<EOFD>'):  # если видим <EOFD> значит данные закончили передавать
            done = True
        elif data.startswith(b'<ESCOF>') and data.endswith(b'</ESCOF>'):  # смотрим если команда завершения
            try:
                key = funcs.decrypt_data(data[32 + 7:-8], data[7:32 + 7])  # пробуем получить ключ, расшифровываем его
                if key.encode(encoding='UTF-8') == SRV_TURNOFF_KEY:  # сверяем верный ли ключ на завершение программы
                    print('[ACTION] !!! Получена команда на завершение работы программы !!!')
                    done = True
            except:
                pass
        crypt_data += data  # записываем текущую порцию данных

    if data.startswith(b'<ESCOF>'):  # если последовательность завершения, то заканчиваем программу
        break
    client.close()  # закрываем коннект с клиентом текущий

    # Декриптим обратно в json строку с помощью AES, помним что первые 32 байта это nonce для AES, для расшифровки
    AES_nonce = crypt_data[:32]  # выдираем NONCE
    crypt_data = crypt_data[32:-6]  # выдираем данные, без nonce и без <EOFD>

    norm_data = funcs.decrypt_data(crypt_data, AES_nonce)  # расшифровываем данные
    norm_data = json.loads(norm_data)  # переводим данные в словарь Python

    cur_data = funcs.srv_read_json(SRV_RECORDS_FILE)  # читаем текущий файл json если он есть
    # пишем в файл новые значения, дополняя если надо старые
    funcs.srv_write_json(SRV_RECORDS_FILE, cur_data, norm_data)
    print(f'[INFO] Новые данные записаны в файл от хоста {ip_addr[0]}')
