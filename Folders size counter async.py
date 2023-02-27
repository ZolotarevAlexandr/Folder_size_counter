import os
import asyncio
import time

sizes_types = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']


def human_read_format(size):
    counter = 0
    while size >= 1024:
        size = size / 1024
        counter += 1

    return round(size, 2), sizes_types[counter]


async def count_size(full_name):
    size = 0
    for path, dirs, files in os.walk(full_name):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    return size


async def get_item_size(full_name, short_name):
    print(f'Started counting {short_name}')
    if os.path.isfile(full_name):
        return short_name, human_read_format(os.path.getsize(full_name))

    folder_size = await count_size(full_name)
    print(f'Finished counting {short_name}')
    return short_name, human_read_format(folder_size)


async def main():
    directory = input('Input path to directory: ')

    result = []
    errors = []
    try:
        for future in asyncio.as_completed([get_item_size(f'{directory}\\{item}', item)
                                           for item in os.listdir(directory)]):
            result.append(await future)
    except Exception as e:
        errors.append(f'Exception ({e}) occurred')
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
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    while True:
        try:
            start = time.time()
            asyncio.run(main())
            print(time.time() - start)
        except Exception as e:
            print(f'Exception ({e}) occurred')
            print()
            print('-' * 30)
            print()
