import time
import funcs

while True:
    print(f"""{'-' * 45}
Выберите опцию:
1) Создать QR-кодовое изображение с данными из указанного файла
2) Расшифровать изображение с указанным QR-кодом и передать данные на сервер
{'-' * 45}
""")
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
        funcs.make_qrcode_datafile(filename)
        time.sleep(2)
