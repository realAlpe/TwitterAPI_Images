from os import listdir, getcwd
from os.path import isfile, join

import re
import shutil
from utils import create_directory


def sort_directory(directory: str) -> None:
    pattern = re.compile(r"(\S+) .+\.png")

    for item in listdir(directory):
        # If it is a file
        if isfile(join(directory, item)):
            # Extract the name from the file name (the first part)
            name = pattern.findall(item)[0]

            # Create a directory for the name if it doesn't already exist
            name_directory = join(directory, name)
            create_directory(name_directory)

            # Move the file from its source to the destination
            src_path = join(directory, item)
            dst_path = join(name_directory, item)
            shutil.move(src_path, dst_path)


def main() -> None:
    # Get all folders in the current directory
    directories = [f for f in listdir() if "." not in f]
    directories.remove("__pycache__")

    if len(directories) == 0:
        print(f"No directories found in {getcwd()}")
        return
    elif len(directories) == 1:
        sort_directory(directories[0])
        pass
    else:
        # Prompt the user which directory he would like to have sorted
        print("Which directory would you like to have sorted?")
        print("Enter the number left of the specified directory.")
        for i, directory in enumerate(directories):
            print(f"{i}: {directory}")

        index = 0
        while 0 <= index < len(directories):
            index = int(input())

        sort_directory(directories[index])


if __name__ == "__main__":
    main()
    input("Press enter to exit... ")
