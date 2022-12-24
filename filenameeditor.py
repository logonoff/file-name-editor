""" Rename files in the current working directory using vscode.
"""
import os
import tempfile
import random
import sys
import math
import argparse

FILES = []
FILES_UPDATED = []


def main(path: str):
    """Main function
    @param path path to the directory to rename files in
    """
    # parse args
    print("Using path " + path)

    # enumerate files and store into FILES
    for file in os.listdir(path):
        FILES.append(file)

    path = create_filelist_txt()

    # open temporary file in vscode
    print("Close the file to continue")
    os.system("code -w " + path)

    # rename the files
    get_updated_names(path)
    update_file_names()


def create_filelist_txt() -> str:
    """
    Create a temporary file containing the names of the files in the cwd

    @return path to the temporary file
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        f_name = temp_dir + (str)(math.floor(random.random() * 10)) + '.txt'
        with open(f_name, 'w', encoding="utf-8") as file:
            file.writelines([f + "\n" for f in FILES])

        return f_name


def get_updated_names(path: str):
    """
    Get the new file names from the temporary file and store it

    @param path path to the temporary file to use
    """
    with open(path, 'r', encoding="utf-8") as file:
        file.seek(0)

        # get new file names
        for line in file.readlines():
            FILES_UPDATED.append(line)


def update_file_names():
    """
    Update the file names of each file in the cwd given the new names
    """
    i = 0  # quick hack to avoid conflicting file names

    for old_name, new_name in zip(FILES, FILES_UPDATED):
        # detect edge case where the file name is the same
        if os.path.isfile(new_name.strip()) and new_name.strip() != old_name:
            os.rename(old_name, str(i) + new_name.strip())
            i += 1
        else:
            os.rename(old_name, new_name.strip())


if __name__ == "__main__":
    # parse args
    p = argparse.ArgumentParser(description="Mass rename files with vscode.",
                                formatter_class=argparse.RawTextHelpFormatter,
                                epilog="""
The program will open a temporary file in vscode containing the names of the files in the cwd.

The order of the lines matter and correspond one-to-one to the new names of the files.

Duplicates are handled by prepending a number to the end of the file name but this is handled poorly so don't do it.

After renaming to your hearts content, close the file and the renaming shall commence.

Use with caution! There is no undo nor is there testing. You have been warned.
""")
    p.add_argument("-path",
                   action="store",
                   type=str,
                   dest="path",
                   default=os.getcwd(),
                   help="Path to the directory to rename files in. By default, the current working directory is used.")

    args = p.parse_args()

    sysArgs = sys.argv
    main(args.path)
