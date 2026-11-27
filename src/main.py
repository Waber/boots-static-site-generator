import os
import shutil
import sys

from src.copy_static import copy_static
from src.generate_page import generate_pages_recursive


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    docs = "docs"
    if os.path.exists(docs):
        shutil.rmtree(docs)
    os.mkdir(docs)
    copy_static("static", docs)
    generate_pages_recursive("content", "template.html", docs, basepath)

if __name__ == '__main__':
    main()
