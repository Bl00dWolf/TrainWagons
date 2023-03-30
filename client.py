import funcs
import json
import time
import socket

# В цикле запускаем вывод консольного меню с вариантами ответов
while True:
    # Печатаем нашу менюху
    print(f"""{'-' * 45}
Выберите опцию:
1) Создать QR-кодовое изображение с данными из указанного файла
2) Расшифровать изображение с указанным QR-кодом и передать данные на сервер
{'-' * 45}
""")
    # Просим пользователя выполнять ввод, выбрав пункт меню. Если пользак выбрал что-то не то
    # пишем ему что он выбрал что-то не то и соот. опять цикл перезапускается
    try:
        choice = int(input())
    except ValueError:
        print('Некорректный формат данных, введите целое число соответствующее нужной опции в меню\n')
        time.sleep(2)
        continue

    if choice < 1 or choice > 2:
        print('Опции под таким номером нет, введите целое число соответствующее нужной опции в меню\n')
        time.sleep(2)
        continue
    elif choice == 1:
        filename = input('Введите полный путь до файла с данными:\n')
        path = input('Введите путь и имя файла для сохранения QR-кода\n'
                     'Например: C:\QRCode.png\n')
        funcs.make_qrcode_datafile(filename, path)
        time.sleep(2)
    elif choice == 2:
        filename = input('Введите полный путь до QRCode файла:\n')

        print('Считываем данные из файла\n')
        raw_data = funcs.get_data_from_QRCode_image(filename)  # считываем сырые данные из файла

        print('Преобразуем данные\n')
        data = funcs.make_dict_from_data(raw_data)  # преобразуем в питоновский словарь

        print('Шифруем данные\n')
        crypted_data = funcs.crypt_data(json.dumps(data))  # преобразуем в json и криптуем через AES

        print('Подключаемся к серверу\n')
        funcs.send_data_to_server(crypted_data)

        # data = funcs.decrypt_data(crypted_data)
        # print(f'decrypted json = {data}')
        # print(f'decrypted python = {json.loads(data)}')
