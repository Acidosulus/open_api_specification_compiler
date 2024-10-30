import os
from msgspec import Struct
from rich import print
import argparse


class SpecFile(Struct):
    path: str
    url: str


def get_directory_structure(root_path):
    paths = []

    for root, dirs, files in os.walk(root_path):
        # Пропускаем файлы из самой корневой директории,
        # там у нас только заголовочный файл
        if root == root_path:
            continue

        for file in files:
            if file.endswith('.yaml'):
                relative_path = (os.path.join(root, file)
                                 .replace(root_path, "")
                                 .replace(".yaml", ""))
                formatted_path = relative_path.replace("\\", "/") + "/"
                paths.append(
                    SpecFile(
                        path=os.path.join(root, file),
                        url=formatted_path,
                    )
                )

    return paths


def get_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = [line.replace('\n', '') for line in file.readlines()]
    return content


def save_file_content(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines('\n'.join(content))


def create_specification(
        header_file_path,
        target_file_path,
):
    content = get_file_content(header_file_path)
    root_directory_path = os.path.dirname(header_file_path)
    paths = get_directory_structure(root_directory_path)
    if len(paths) > 0:
        content.append('')
        content.append('paths:')
        content.append('')

    for file in paths:
        content.append('  ' + file.url + ":")
        schema_path = get_file_content(file.path)
        content.extend(['    ' + line for line in schema_path])
        content.append('')

    save_file_content(target_file_path, content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create API specification.')
    parser.add_argument('specification',
                        help='Create YAML OPENAPI specification file')
    parser.add_argument('--head', required=True,
                        help='Path to the source head file')
    parser.add_argument('--output', required=True,
                        help='Path to the output file')

    args = parser.parse_args()

    if args.specification == 'specification':
        create_specification(args.head, args.output)