import os
from tqdm import tqdm


def print_indent() -> None:
    print()
    print('-' * 30)
    print()


# Returns folder size in more convenient format
def human_read_format(size: int) -> dict:
    sizes_types = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
    counter = 0

    while size >= 1024:
        size = size / 1024
        counter += 1

    return {'size': round(size, 2), 'size_type': sizes_types[counter]}


# Returns a folder size in bytes
def get_folder_size(folder_name: str) -> int:
    folder_size = 0

    # Going through every file in directory using os.walk, counting folder size by adding each file
    # size (rather slow, but reliable way)
    for path, dirs, files in os.walk(folder_name):
        for file in files:
            file_path = os.path.join(path, file)
            folder_size += os.path.getsize(file_path)

    return folder_size


def main() -> None:
    directory = input('Input path to directory: ')

    result = []
    errors = []

    # Going through each file and folder using os.listdir. tqdm is just a progressbar
    for item in tqdm(os.listdir(directory), unit=' folders'):
        try:
            item_path = rf'{directory}\{item}'
            # Since get_folder_size can only count size of folders, counting size of files separately
            if os.path.isfile(item_path):
                result.append({'item': item, 'size': os.path.getsize(item_path)})
            else:
                result.append({'item': item, 'size': get_folder_size(item_path)})
        except Exception as e:
            # Adding all errors in the list, so we can print them later
            errors.append(f'Exception ({e}) occurred with file {item}')

    if errors:
        print()
        print('Following errors have occurred: ')
        print('\n'.join(errors))

    print_indent()

    # Sorting the result based in bytes size and that changing size to more readable format for output
    result = sorted(result, key=lambda x: x['size'], reverse=True)
    result = list(map(lambda x: {**x, 'size': human_read_format(x['size'])}, result))

    for item in result:
        print(f'{item["item"]} - {item["size"]["size"]} {item["size"]["size_type"]}')

    print_indent()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            # Catching all exceptions from main, so app won't crash
            print(f'Exception ({e}) occurred')
            print_indent()
