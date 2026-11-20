import os
import shutil


def copy_static(uri: str, directory: str):
    for dir in os.listdir(uri):
        if os.path.isdir(os.path.join(uri, dir)):
            os.mkdir(os.path.join(directory, dir))
            copy_static(os.path.join(uri, dir), os.path.join(directory, dir))
        elif os.path.isfile(os.path.join(uri, dir)):
            shutil.copy(os.path.join(uri, dir), os.path.join(directory, dir))
            print(f"Copied {os.path.join(uri, dir)} to {os.path.join(directory, dir)}")
