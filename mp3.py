import os
import shutil
from pathlib import Path

# Путь к папке с файлами, которые нужно заменить
target_directory = 'venv/img mp3'

# Путь к файлу, которым нужно заменить все файлы в целевой папке
replacement_file = 'venv/aye/30finih_azs.mp3'

# Проверяем, существует ли целевая папка
if not os.path.exists(target_directory):
    print(f"Ошибка: Директория {target_directory} не существует.")
else:
    # Проверяем, существует ли файл для замены
    if not os.path.exists(replacement_file):
        print(f"Ошибка: Файл {replacement_file} не существует.")
    else:
        # Проходим по всем файлам в целевой папке
        for file in os.listdir(target_directory):
            target_file_path = os.path.join(target_directory, file)

            # Проверяем, является ли элемент файлом
            if os.path.isfile(target_file_path):
                try:
                    # Создаем временный файл в целевой папке с тем же именем

                    temp_file_path = target_file_path + '.tmp'
                    print(replacement_file)
                    shutil.copy(replacement_file, temp_file_path)

                    # Переименовываем временный файл, заменяя оригинальный файл
                    os.replace(temp_file_path, target_file_path)

                    print(f'Файл {file} был заменен.')
                except Exception as e:
                    print(f"Произошла ошибка при замене файла {file}: {e}")