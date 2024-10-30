import copy
import os
from msgspec import Struct
from rich import print
import re
import argparse
import  yaml
from pathlib import Path
from tempfile import TemporaryDirectory
from datamodel_code_generator import InputFileType, generate
from datamodel_code_generator import DataModelType, OpenAPIScope
import subprocess

class SpecFile(Struct):
    path: str
    url: str

def sanitize_filename(filename):
    sanitized = re.sub(r'[<>:"/\\|?*\n\t]', '_', filename)
    sanitized = sanitized.replace(' ', '').lower()
    sanitized = sanitized[1:] if sanitized.startswith('_') else sanitized
    return sanitized[:255]

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

def join_specifications(header, added_endpoint: dict, url:str):
    if added_endpoint.get('components') is not None:
        if added_endpoint['components'].get('schemas') is not None:

            if header.get('components') is None:
                header['components'] = {}
            if header['components'].get('schemas') is None:
                header['components']['schemas'] = {}

            header['components']['schemas'].update(
                added_endpoint['components']['schemas'])

            added_endpoint.pop('components')

    endpoint = {url: added_endpoint}
    header['paths'] = {**header['paths'], **endpoint}
    return header


def create_models(input_filename):
    params = [
        "datamodel-codegen",
        "--input", f"'{input_filename}'",
        "--input-file-type", "openapi",
        "--output ", f"'{input_filename.replace('.yaml', '_models').replace('__', '_')}.py'",
        "--openapi-scopes", "{parameters,paths,schemas}",
        "--output-model-type", "msgspec.Struct"
    ]
    script_filename = "generate_models.sh"

    with open(script_filename, "w") as script_file:
        script_file.write("#!/bin/bash\n")
        script_file.write(' '.join(params) + '\n')

    os.chmod(script_filename, 0o755)

    result = subprocess.run(["bash", script_filename])

    os.remove(script_filename)

    return result


def create_specification_yaml(
        header_file_path,
        target_file_path,
):
    print(        header_file_path,
        target_file_path)
    with open(header_file_path, "r", encoding="utf-8") as file:
        content = yaml.safe_load(file)
    header_empty = content
    paths = get_directory_structure(os.path.dirname(header_file_path))
    print(paths)

    if len(paths) > 0:
        if content.get('paths') is None:
            content['paths'] = {}

    for endpoint_file in paths:

        with open(endpoint_file.path, "r", encoding="utf-8") as file:
            endpoint_source = yaml.safe_load(file)

        content = join_specifications(
            copy.deepcopy(content),
            copy.deepcopy(endpoint_source),
            endpoint_file.url
        )

        sub_schema = join_specifications(
            copy.deepcopy(header_empty),
            copy.deepcopy(endpoint_source),
            endpoint_file.url
        )

        models_file_name = os.path.join(os.path.dirname(header_file_path),sanitize_filename(endpoint_file.url)+'_models.yaml')

        print(models_file_name)
        with open(models_file_name, "w", encoding="utf-8") as file:
            yaml.dump(sub_schema, file, default_flow_style=False, allow_unicode=True)
        create_models(models_file_name)

    with open(target_file_path, "w", encoding="utf-8") as file:
        yaml.dump(content, file, default_flow_style=False, allow_unicode=True)


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
        create_specification_yaml(args.head, args.output)



