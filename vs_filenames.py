import os
import tempfile
import random
import sys
import math


FILES_ORIGINAL = []
FILES_UPDATED = []


def main(path: str, lacks_vs_code: bool):
    """
    Main function
    @param path path to the directory to rename files in
    @param lacks_vs_code if true, the default editor will be used instead of vscode
    """
    # validate path
    if not os.path.isdir(path):
        raise NotADirectoryError("Path is not a directory!")

    # parse args
    print("Using path " + path)

    # enumerate files and store into FILES
    for file in os.scandir(path):
        FILES_ORIGINAL.append(file.name)

    # create txt file with the file names
    path = create_filelist_txt()

    # use the default editor if vscode is not found
    if lacks_vs_code:
        print("Make your changes then press enter to continue")
        os.system(path)
        input()
    else:
        # open temporary file in vscode
        print("Make your changes then close the file to continue")
        os.system("code -w " + path)

    # get and rename files
    get_updated_names(path)
    update_file_names()

    # delete temporary file
    try:
        os.remove(path)
    except PermissionError:
        print("Permission denied while deleting the temporary file " + path)
        sys.exit(1)
    except OSError:
        print("Couldn't delete the temporary file " + path)
        sys.exit(1)


def create_filelist_txt() -> str:
    """
    Create a temporary file containing the names of the files in the cwd

    @return path to the temporary file
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # random file name to avoid conflicts
        f_name = temp_dir + (str)(math.floor(random.random() * 10)) + '.txt'

        # write the file names to the temporary file
        with open(f_name, 'w', encoding="utf-8") as file:
            for file_name in FILES_ORIGINAL:
                file.write(file_name + '\n')

        return f_name


def get_updated_names(path: str):
    """
    Get the new file names from the temporary file and store it

    @param path path to the temporary file to use
    """
    try:
        with open(path, 'r', encoding="utf-8") as file:
            file.seek(0)

            # get new file names
            for line in file.readlines():
                FILES_UPDATED.append(line)
    except FileNotFoundError:
        print("File not found! Was it deleted..?")
        sys.exit(1)
    except PermissionError:
        print("Permission denied when reading " + path)
        sys.exit(1)


def update_file_names():
    """
    Update the file names of each file in the cwd given the new names
    """
    # make sure the number of files hasn't changed
    assert len(FILES_ORIGINAL) == len(
        FILES_UPDATED), "Don't change the number of lines in the file!"

    i = 0  # quick hack to avoid conflicting file names

    for old_name, new_name in zip(FILES_ORIGINAL, FILES_UPDATED):
        # detect edge case where the file name is the same
        new = new_name.strip()

        if os.path.isfile(new) and (new != old_name):
            new = str(i) + new
            i += 1  # keeps the file name unique

        # rename the file and handle errors
        try:
            os.rename(old_name, new)
        except PermissionError:
            print("Permission denied when renaming " + old_name + " to " + new)
        # ensures that the file name is valid, e.g., length, invalid characters
        except OSError:
            print("Error renaming " + old_name + " to " + new + "!")


def entry():
    """Entry point for the program
    """
    import argparse

    # parse args
    p = argparse.ArgumentParser(description="Mass rename files with vscode.",
                                formatter_class=argparse.RawTextHelpFormatter,
                                epilog="""
The program will open a temporary file in vscode containing the names of the files in the cwd.

If VS Code is not found in the PATH, the temporary file will be opened in the default text editor, and you'll have to close it manually, then press enter.

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
                   help="""Path to the directory to rename files in.
By default, the current working directory is used.""")

    # check if vscode is in the path
    import shutil
    p.add_argument("-no-code",
                   action=argparse.BooleanOptionalAction,
                   type=bool,
                   default=not (shutil.which("code")),
                   help="If set to true, the default editor will be used instead of vscode.")

    args = p.parse_args()

    main(args.path, args.no_code)


if __name__ == "__main__":
    entry()
