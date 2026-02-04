import os
import shutil

source_dir = "./test_downloads"

def sort_files_in_dir(directory):
    if not os.path.exists(directory):
        print(f"Директория {directory} не существует. Создаём для теста...")
        os.makedirs(directory)
        open(os.path.join(directory, "test1.txt"), 'w').close()
        open(os.path.join(directory, "image.jpg"), 'w').close()
        open(os.path.join(directory, "script.py"), 'w').close()
        open(os.path.join(directory, "document.pdf"), 'w').close()
        print("Тестовые файлы созданы.")

    print(f"Анализ директории: {directory}...")
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isdir(filepath):
            continue

        _, file_extension = os.path.splitext(filename)
        if not file_extension:
            continue
            
        extension = file_extension[1:].lower()
        target_folder = os.path.join(directory, extension)
        
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            print(f"Создана директория: {target_folder}")
            
        try:
            shutil.move(filepath, os.path.join(target_folder, filename))
            print(f"Перемещён файл: {filename} -> {extension}/")
        except Exception as e:
            print(f"Ошибка при перемещении {filename}: {e}")

if __name__ == "__main__":
    sort_files_in_dir(source_dir)