import os
import shutil

from copy_static import copy_static


def main():
    public = "public"
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    copy_static("static", public)

if __name__ == '__main__':
    main()
