import os
import shutil
import stat

def get_and_increment_counter():
    try:
        with open('counter.txt', 'r') as file:
            k = int(file.read().strip())
    except FileNotFoundError:
        k = 0
    k += 1
    with open('counter.txt', 'w') as file:
        file.write(str(k))
    return k

def move_folder_3(folder_path, phone):
    try:
        target_directory = 'accounts2'

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        full_folder_path = os.path.abspath(folder_path)
        folder_name = os.path.basename(full_folder_path)
        target_path = os.path.join(target_directory)

        if phone == 0:
            account_path = os.path.join(target_path, f"Account{str(get_and_increment_counter())}")
        else:
            account_path = os.path.join(target_path, phone)

        tdata_path = os.path.join(account_path, "tdata")

        shutil.move(full_folder_path, tdata_path)
        shutil.rmtree(os.path.join(folder_path.split('/')[0], folder_path.split('/')[1]), ignore_errors=True)

        # Удаление файлов, не соответствующих критериям
        delete_unwanted_files(tdata_path)
    except Exception as ex:
        print(f'Ошибка {str(ex)}')

def move_folder_2(folder_path, success, phone, spam_folder=None):
    try:
        if success == True:
            target_directory = 'снятие спама'
        elif spam_folder:
            target_directory = spam_folder
        else:
            target_directory = 'не удалось'

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        full_folder_path = os.path.abspath(folder_path)
        folder_name = os.path.basename(full_folder_path)
        target_path = os.path.join(target_directory)

        if phone == 0:
            account_path = os.path.join(target_path, f"Account{str(get_and_increment_counter())}")
        else:
            account_path = os.path.join(target_path, phone)

        tdata_path = os.path.join(account_path, "tdata")

        shutil.move(full_folder_path, tdata_path)
        shutil.rmtree(os.path.join(folder_path.split('/')[0], folder_path.split('/')[1]), ignore_errors=True)

        # Удаление файлов, не соответствующих критериям
        delete_unwanted_files(tdata_path)
    except Exception as ex:
        print(f'Ошибка {str(ex)}')

def move_folder(folder_path, is_valid, have_spam_block, phone):
    try:
        if is_valid is not None:
            if is_valid:
                if have_spam_block:
                    target_directory = "спам"
                else:
                    target_directory = "не спам"
            else:
                target_directory = "невалидные_аккаунты"
        else:
            target_directory = "не проверен"

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        full_folder_path = os.path.abspath(folder_path)
        folder_name = os.path.basename(full_folder_path)
        target_path = os.path.join(target_directory)
        if phone == 0:
            account_path = os.path.join(target_path, f"Account{str(get_and_increment_counter())}")
        else:
            account_path = os.path.join(target_path, phone)
        os.makedirs(account_path)

        tdata_path = os.path.join(account_path, "tdata")

        shutil.move(full_folder_path, tdata_path)
        shutil.rmtree(os.path.join(folder_path.split('/')[0], folder_path.split('/')[1]), ignore_errors=True)

        # Удаление файлов, не соответствующих критериям
        delete_unwanted_files(tdata_path)
    except Exception as e:
        print(f"Ошибка: {e}")

def delete_unwanted_files(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if "D877F783D5D3EF8C" not in file_name and file_name != "key_datas":
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)

def get_folder_names(directory='accounts'):
    ready_directories = []

    for foldername, subfolders, filenames in os.walk(directory):
        for subfolder in subfolders:
            if "tdata" in subfolder.lower():
                directory_path = os.path.join(foldername, subfolder)
                print(directory_path)
                if directory_path not in ready_directories:
                    ready_directories.append(directory_path[9:])
    return ready_directories

def get_folder_names_2(directory='accounts'):
    ready_directories = []

    for foldername, subfolders, filenames in os.walk(directory):
        for subfolder in subfolders:
            if "tdata" in subfolder.lower():
                directory_path = os.path.join(foldername, subfolder)
                print(directory_path)
                if directory_path not in ready_directories:
                    ready_directories.append(directory_path[6:])
    return ready_directories

print(get_folder_names())
