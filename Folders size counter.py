import os
from tqdm import tqdm

sizes_types = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']


def human_read_format(size):
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
    directory = input('Input path to directory: ')

    result = []
    errors = []
    for index, item in enumerate(tqdm(os.listdir(directory), unit=' folders')):
        try:
            if os.path.isfile(item):
                result.append((item, human_read_format(os.path.getsize(f'{directory}\\{item}'))))
            else:
                result.append((item, human_read_format(get_folder_size(f'{directory}\\{item}'))))
        except Exception as e:
            errors.append(f'Exception ({e}) occurred on file {item}')
    if errors:
        print()
        print('Following errors have occurred: ')
        print('\n'.join(errors))

    print()
    print('-' * 30)
    print()

    result = sorted(result, key=lambda x: (sizes_types.index(x[1][1]), x[1][0]), reverse=True)
    for i, item in enumerate(result):
        print(f'{item[0]} - {item[1][0]} {item[1][1]}')

    print()
    print('-' * 30)
    print()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(f'Exception ({e}) occurred')
            print()
            print('-' * 30)
            print()
