"""
    Module used to play Around
"""
import os
from typing import Optional


def double_string(text: str) -> str:
    """
    Function to double a given input String

    Args:
        text: String to double

    Returns:
        value: Value which contains the doubled String
    """
    value = text * 2
    return value


def write_string_to_file(
    text: str, file_name: str, data_dir: Optional[str] = "./../data/raw/"
) -> str:
    """ Function

    Args:
        text: String which will be written to File
        file_name: Filename
        data_dir: Optional data path

    Returns:
        file_path: Path to the created file

    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with open(data_dir + file_name, "w") as text_file:
        text_file.write(text)


if __name__ == "__main__":
    write_string_to_file("Hallo Welt", "test.txt")
