import shutil
import os
import sys
from pathlib import Path

def start():
    if len(sys.argv) < 2:
        sys.exit(1)
    folder_path = sys.argv[1]
    main(folder_path)


def main(path):
    list_folders = []
    list_files = []
    filtered_list_files = []
    filtered_list_folders = []
    lists_unk_files = []
    remove_list = []
    
    path_images = create_dir(path, 'images')               #создание папок для файлов и архивов (если их нету)
    path_documents = create_dir(path, 'documents')
    path_audio = create_dir(path, 'audio')
    path_video = create_dir(path, 'video')
    path_archives = create_dir(path, 'archives')
    path_unknown_files = create_dir(path, 'Unknown_files')
    ignore_dir = [f'{path_images}', f'{path_documents}', f'{path_audio}', f'{path_video}', f'{path_archives}', f'{path_unknown_files}']
    
    for root, dirs, files in os.walk(path):                  #списки всех папок и файлов 
        for folder in dirs:
            folders_path = os.path.join(root, folder)
            list_folders.append(folders_path)

        for file in files:
            files_path = os.path.join(root, file)
            list_files.append(files_path)
    
    for ignor_files in list_files:                          #удаление из списка файлов внутри папок (видео, документы и тд.)
        if not any(new_files in ignor_files for new_files in ignore_dir):
            filtered_list_files.append(ignor_files)
    
    for ignor_folders in list_folders:                      #удаление из списка созданых папок (видео, документы и тд.)
        if not any(new_folders in ignor_folders for new_folders in ignore_dir):
            filtered_list_folders.append(ignor_folders)    
    
    for files_form_list in filtered_list_files:             #перемещение файлов, распаковка архивов и транслитерация
        name_of_files = os.path.basename(files_form_list)
        file_name = os.path.splitext(name_of_files)[0]
        file_suf = os.path.splitext(name_of_files)[1]
        trans_file_name = normalize(file_name)
        if file_suf.upper() in lists_img:
            new_path = os.path.join(path_images, f'{trans_file_name}{file_suf}')
            os.rename(files_form_list, new_path)
        elif file_suf.upper() in lists_vid:
            new_path = os.path.join(path_video, f'{trans_file_name}{file_suf}')
            os.rename(files_form_list, new_path)
        elif file_suf.upper() in lists_doc:
            new_path = os.path.join(path_documents, f'{trans_file_name}{file_suf}')
            os.rename(files_form_list, new_path)
        elif file_suf.upper() in lists_mus:
            new_path = os.path.join(path_audio, f'{trans_file_name}{file_suf}')
            os.rename(files_form_list, new_path)
        elif file_suf.upper() in lists_arch:
            try:
                new_path = os.path.join(path_archives, f'{trans_file_name}')
                shutil.unpack_archive(files_form_list, new_path)
                os.remove(files_form_list)
            except:
                print(f"Can't unpack: {name_of_files}")
                os.remove(files_form_list)
        
        elif file_suf.upper() not in lists_suf:
            lists_unk_files.append(f'{name_of_files}')
            new_path = os.path.join(path_unknown_files, f'{name_of_files}')
            os.rename(files_form_list, new_path)
    
    for folders_from_list in filtered_list_folders:         #удаление пустых папок 
        contents = os.listdir(folders_from_list)
        if not contents:
            remove_list.append(folders_from_list)
    for rem in remove_list:    
        os.rmdir(rem)
              
    
    new_filtered_list_folders = [item for item in filtered_list_folders if item not in remove_list]
    
    for folders_from_list in new_filtered_list_folders:     #транслитерация папок
        name_of_fold = os.path.basename(folders_from_list)
        new_name_of_fold = normalize(name_of_fold)
        path_components = folders_from_list.split(os.sep)
        path_components[-1] = new_name_of_fold
        path_for_new_name = os.sep.join(path_components)
        os.rename(folders_from_list, path_for_new_name)
    
    if len(new_filtered_list_folders) >= 1:
        main(path)
    else:  
        print(f'Unknown files: {os.listdir(path_unknown_files)}')
    

def normalize(name):                                        #функция транслитерации
    new_name = ""
    map = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', \
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', \
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', \
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', \
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    for i in name:
        if i.isalpha():
            if i in map:
                trans_i = map[i]
                new_name += trans_i
            elif i.isupper() and i.lower() in map:
                translit_i = map[i.lower()]
                new_name += translit_i.upper()
            else:
                new_name += i
        elif i.isdigit():
            new_name += i
        else:
            new_name += '_'
    return new_name


def create_dir(dir_path, name):   
                                                          #функция создания папок
    path_for_dir_1 = os.path.join(dir_path, name)
    path_for_dir_1 = Path(path_for_dir_1)
    try:    
        path_for_dir_1.mkdir()
        my_path = str(path_for_dir_1)
        return my_path
    except:   
        my_path = str(path_for_dir_1)
        return my_path
    
    
lists_img = ['.JPEG', '.PNG', '.JPG', '.SVG']
lists_vid = ['.AVI', '.MP4', '.MOV', '.MKV']
lists_doc = ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']
lists_mus = ['.MP3', '.OGG', '.WAV', '.AMR']
lists_arch = ['.ZIP', '.GZ', '.TAR']
lists_suf = lists_img + lists_vid + lists_doc + lists_mus + lists_arch


if __name__ == "__main__":
    start()