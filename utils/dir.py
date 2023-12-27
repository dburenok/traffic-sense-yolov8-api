from pathlib import Path
from shutil import rmtree
import os


def init_dir(dir):
    if os.path.exists(dir) and os.path.isdir(dir):
        rmtree(dir)
    Path(dir).mkdir(exist_ok=False)


def delete_dir(dir):
    if os.path.exists(dir) and os.path.isdir(dir):
        rmtree(dir)