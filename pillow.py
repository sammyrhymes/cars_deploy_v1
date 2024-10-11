from PIL import Image
import os
from django.conf import settings
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

def process_image(image, target_size=(1024, 768), quality=85):
    # Open the uploaded image
    img = Image.open(image)

    # Check the current size of the image
    if img.size != target_size:
        # Resize the image to the target size
        img = img.resize(target_size, Image.LANCZOS)

    # Create a new filename with .jpeg extension
    base_filename, _ = os.path.splitext(image.name)
    new_filename = f"{base_filename}.jpg"

    # Save the processed image to a BytesIO object
    output = BytesIO()
    img.convert('RGB').save(output, format='JPEG', quality=quality)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        None,
        new_filename,
        'image/jpeg',
        output.getbuffer().nbytes,
        None
    )

def processimage(image, target_size=(1280, 853), quality=85):
    # Open the uploaded image
    img = Image.open(image)

    # Check the current size of the image
    if img.size != target_size:
        # Resize the image to the target size
        img = img.resize(target_size, Image.LANCZOS)

    # Create a new filename with .jpeg extension
    base_filename, _ = os.path.splitext(image.name)
    new_filename = f"{base_filename}.jpg"

    # Save the processed image to a BytesIO object
    output = BytesIO()
    img.convert('RGB').save(output, format='JPEG', quality=quality)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        None,
        new_filename,
        'image/jpeg',
        output.getbuffer().nbytes,
        None
    )