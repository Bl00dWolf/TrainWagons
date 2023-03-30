import funcs
import json
import time
import socket
from config import SERVER_IP, SERVER_PORT

# data = funcs.decrypt_data(crypted_data)
# print(f'decrypted json = {data}')
# print(f'decrypted python = {json.loads(data)}')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Запускаем сервер...')
server.bind((SERVER_IP, SERVER_PORT))
print('Готовы к приему...')
server.listen()

client, ip_addr = server.accept()

crypt_data = b''
done = False
while not done:
    data = client.recv(1024)
    if data[-18:] == b'<END_OF_DATA_FILE>':
        done = True
    crypt_data += data

client.close()
server.close()

norm_data = funcs.decrypt_data(crypt_data[:-18])
norm_data = json.loads(norm_data)
print(norm_data)

