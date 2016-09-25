from uuid import uuid4
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os


# Intended to be used as an argument for upload_to option in ImageField
# Generates a random path for an image formatted as
# 'MEDIA_ROOT/<args[0]>/.../<random id>.<ext>'
# The path keeps the file extension of the input file
def random_path(*args):
    def path(instance, filename):
        directory = '/'.join(args)
        _, ext = os.path.splitext(filename)
        random_id = uuid4().hex
        return '{}/{}{}'.format(directory, random_id, ext)
    return path


# Converts the input image to a 256 colors png,
# creates a thumbnail with the specified height and width
# and returns a new file
def optimize_png(filename, width, height):
    img = Image.open(filename)
    img = img.convert('P')
    img.thumbnail((width, height))
    path, ext = os.path.splitext(filename)
    buf = BytesIO()
    if ext != '.png':
        # os.remove(filename)
        filename = path + '.png'
    img.save(buf, 'png')
    print(filename)
    return SimpleUploadedFile(
        filename,
        buf.getvalue(),
        'image/png')


def optimize_jpg(filename, width, height):
    img = Image.open(filename)
    img.thumbnail((width, height))
    path, ext = os.path.splitext(filename)
    buf = BytesIO()
    if ext != '.jpg':
        # os.remove(filename)
        filename = path + '.jpg'
    img.save(buf, 'jpeg', quality=80, optimize=True)
    return SimpleUploadedFile(
        filename,
        buf.getvalue(),
        'image/jpeg')
