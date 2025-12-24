#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для удаления дубликатов строк из текстового файла.
Использует MD5 хеширование для эффективной работы с большими файлами.
"""

import hashlib
import argparse
import sys
import os


def remove_duplicates(input_file, output_file):
    """
    Удаляет дубликаты строк из входного файла и сохраняет результат в выходной файл.

    Args:
        input_file (str): Путь к входному файлу
        output_file (str): Путь к выходному файлу

    Returns:
        tuple: (количество уникальных строк, количество дубликатов)
    """
    seen_hashes = set()
    unique_count = 0
    duplicate_count = 0

    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', encoding='utf-8') as f_out:

            for line in f_in:
                # Генерируем компактный хеш строки для экономии RAM
                line_hash = hashlib.md5(line.encode('utf-8')).digest()

                if line_hash not in seen_hashes:
                    f_out.write(line)
                    seen_hashes.add(line_hash)
                    unique_count += 1
                else:
                    duplicate_count += 1

        return unique_count, duplicate_count

    except FileNotFoundError:
        print(f"Ошибка: Входной файл '{input_file}' не найден.")
        sys.exit(1)
    except PermissionError:
        print(f"Ошибка: Нет доступа к файлу '{input_file}' или '{output_file}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Удаляет дубликаты строк из текстового файла',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py input.txt output.txt
  python main.py -i data.txt -o cleaned.txt
  python main.py --input large_file.txt --output unique_lines.txt
        """
    )

    parser.add_argument(
        'input_file',
        nargs='?',
        help='Путь к входному файлу'
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Путь к выходному файлу'
    )
    parser.add_argument(
        '-i', '--input',
        dest='input_file_alt',
        help='Путь к входному файлу (альтернативный способ)'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_file_alt',
        help='Путь к выходному файлу (альтернативный способ)'
    )

    args = parser.parse_args()

    # Определяем пути к файлам
    input_file = args.input_file_alt or args.input_file
    output_file = args.output_file_alt or args.output_file

    # Проверяем наличие обязательных аргументов
    if not input_file:
        parser.error("Необходимо указать входной файл (используйте позиционный аргумент или -i/--input)")

    if not output_file:
        parser.error("Необходимо указать выходной файл (используйте позиционный аргумент или -o/--output)")

    # Проверяем существование входного файла
    if not os.path.exists(input_file):
        print(f"Ошибка: Входной файл '{input_file}' не существует.")
        sys.exit(1)

    # Предупреждаем, если выходной файл уже существует
    if os.path.exists(output_file):
        response = input(f"Выходной файл '{output_file}' уже существует. Перезаписать? (y/n): ")
        if response.lower() not in ['y', 'yes', 'д', 'да']:
            print("Операция отменена.")
            sys.exit(0)

    print(f"Обработка файла: {input_file}")
    unique_count, duplicate_count = remove_duplicates(input_file, output_file)

    print(f"\n✓ Готово! Очищенные данные сохранены в: {output_file}")
    print(f"  Уникальных строк: {unique_count}")
    print(f"  Дубликатов удалено: {duplicate_count}")
    print(f"  Всего обработано: {unique_count + duplicate_count}")


if __name__ == "__main__":
    main()