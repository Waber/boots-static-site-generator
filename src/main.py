import os
import shutil

from src.copy_static import copy_static
from src.generate_page import generate_page, generate_pages_recursive


def main():
    public = "public"
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    copy_static("static", public)
    generate_pages_recursive("content", "template.html", "public")

if __name__ == '__main__':
    main()
