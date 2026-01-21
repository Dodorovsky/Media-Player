from PIL import Image, ImageTk
import sys
import os
from modules.utils import resource_path


def load_image(path, size=None):
    img = Image.open(resource_path(path))
    if size:
        img = img.resize(size)
    return ImageTk.PhotoImage(img)
