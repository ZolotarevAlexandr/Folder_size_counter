import os


def human_read_format(size):
    sizes_types = ['Б', 'КБ', 'МБ', 'ГБ']
    counter = 0

    while size >= 1024:
        size = size / 1024
        counter += 1

    return round(size, 2), sizes_types[counter]


def get_folder_size(name):
    folder_size = 0
    for path, dirs, files in os.walk(name):
        for f in files:
            fp = os.path.join(path, f)
            folder_size += os.path.getsize(fp)
    return folder_size


def main():
    sizes_types = ['Б', 'КБ', 'МБ', 'ГБ']
    directory = input('Input path to directory ("." for current): ')

    result = []
    all_dirs_len = len(os.listdir(directory))
    for index, item in enumerate(os.listdir(directory)):
        try:
            if os.path.isfile(item):
                result.append((item, human_read_format(os.path.getsize(f'{directory}\\{item}'))))
            else:
                result.append((item, human_read_format(get_folder_size(f'{directory}\\{item}'))))
        except Exception as e:
            print(f'Exception ({e}) occurred on file {item}')
        print(f'Progress: {round((index / all_dirs_len) * 100)}%')

    result = sorted(result, key=lambda x: (sizes_types.index(x[1][1]), x[1][0]), reverse=True)
    for i, item in enumerate(result):
        print(f'{item[0]} - {item[1][0]}{item[1][1]}')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Exception ({e}) occurred')
    input('Press any button to exit')
