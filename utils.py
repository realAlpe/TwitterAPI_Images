from json import dump, load
from subprocess import Popen

import os


def get_json(filename: str) -> object:
    with open(f"{filename}.json", "r+") as f:
        data = load(f)
    return data


def set_json(filename: str, obj: object, indent_length: int = 2) -> None:
    with open(f"{filename}.json", "w+") as f:
        dump(obj, f, indent=indent_length)


def get_json_attribute(filename: str, key: str):
    data: dict = get_json(filename)
    return data.get(key)


def get_since_id() -> int:
    # Get the last since_id in order to avoid duplication
    create_file("since_id.json")
    since_id = get_json_attribute("since_id", "since_id")
    if since_id is None:
        since_id = int(input("Please enter the ID of a tweet that is not too old.\n"))
    return since_id


def set_since_id(id: int) -> None:
    set_json("since_id", {"since_id": id})


def get_options_attribute(key: str):
    return get_json_attribute("options", key)


def create_file(file_path: str) -> None:
    if not os.path.exists(file_path):
        with open(file_path, "w+") as f:
            f.write(r"{}")


def create_directory(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)


def open_directory(directory_path) -> None:
    directory_path = get_options_attribute("folder_name")
    current_directory: str = os.path.dirname(__file__)
    image_directory = os.path.join(current_directory, directory_path)
    Popen(rf'explorer /select,"{image_directory}"')
