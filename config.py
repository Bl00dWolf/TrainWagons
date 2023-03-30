# Этот файл для переменных среды, который в принципе не должен быть в Git как либо указан, но в данном случаи
# он в Гите, т.к. это учебный проект и мы не боимся за безопасность

AES_KEY: bytes = b'tz$x&SI#23C46Cx@VRgqAi5wDk9JqQLx'  # Должен быть либо 16 байт (символов) либо 32.
CLIENT_IP, CLIENT_PORT = 'localhost', 2721
SERVER_IP, SERVER_PORT = 'localhost', 2721
SRV_TURNOFF_KEY = b'4[ygYqmEZ"cFx=IJ&^F+3?$HmVZR2R'
SRV_RECORDS_FILE = 'data_file.json'  # имя файла или полный путь к файлу записей, которые создает сервер
