import funcs
import json
import time

# В цикле запускаем вывод консольного меню с вариантами ответов
while True:
    # Печатаем нашу менюху
    print(f"""{'-' * 45}
Выберите опцию:
0) Выход
1) Создать QR-кодовое изображение с данными из указанного файла
2) Расшифровать изображение с указанным QR-кодом и передать данные на сервер
3) Завершить работу программы на серверной части.
{'-' * 45}
""")
    # Просим пользователя выполнять ввод, выбрав пункт меню. Если пользователь выбрал что-то не то
    # пишем ему что он выбрал что-то не то и опять цикл перезапускается
    try:
        choice = int(input())
    except ValueError:
        print('Некорректный формат данных, введите целое число соответствующее нужной опции в меню\n')
        time.sleep(2)
        continue

    if choice < 0 or choice > 3:
        print('Опции под таким номером нет, введите целое число соответствующее нужной опции в меню\n')
        time.sleep(2)
        continue

    elif choice == 0:
        print('Выход')
        break

    elif choice == 1:
        filename = input('Введите полный путь до файла с данными:\n')
        path = input('Введите путь и имя файла для сохранения QR-кода\n'
                     'Например: C:\QRCode.png\n')
        funcs.make_qrcode_datafile(filename, path)
        time.sleep(2)

    elif choice == 2:
        filename = input('Введите полный путь до QRCode файла:\n')

        print('Считываем данные из файла...')
        raw_data = funcs.get_data_from_QRCode_image(filename)  # считываем сырые данные из файла
        if not raw_data:
            continue

        print('Преобразуем данные...')
        data = funcs.make_dict_from_data(raw_data)  # преобразуем в питоновский словарь
        if not data:
            print('Нет новых данных, завершение.')
            continue

        print('Шифруем данные...')
        crypted_data, AES_nonce = funcs.crypt_data(json.dumps(data))  # преобразуем в json и криптуем через AES

        # Подключаемся к серверу и передаем данные
        print('Подключаемся к серверу...')
        funcs.send_data_to_server(AES_nonce + crypted_data)  # передаем AES nonce и наши данные

    elif choice == 3:
        funcs.server_exit_program()
