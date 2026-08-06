import os
import ssl
import certifi
import easyocr
import numpy as np

from io import BytesIO
from PIL import Image, ImageOps, UnidentifiedImageError


# Tell Python to use Certifi's trusted certificate bundle.
ssl._create_default_https_context = (
    lambda: ssl.create_default_context(
        cafile=certifi.where()
    )
)


# Load the OCR model once when the application starts.
reader = easyocr.Reader(["en"])


def extract_recipe(recipe_file):
    """
    Extract text from one uploaded recipe image.

    The uploaded image is opened with Pillow, corrected for phone-camera
    orientation, converted to RGB, resized when extremely large, and then
    passed to EasyOCR as a NumPy array.
    """

    try:
        # Read the uploaded file into memory.
        file_bytes = recipe_file.read()

        if not file_bytes:
            raise ValueError("The uploaded file is empty.")

        # Open and normalize the image.
        with Image.open(BytesIO(file_bytes)) as image:
            # Apply the orientation stored by phones and cameras.
            image = ImageOps.exif_transpose(image)

            # EasyOCR works reliably with a standard RGB image.
            image = image.convert("RGB")

            # Prevent extremely large phone photos from causing OCR problems.
            image.thumbnail((2500, 2500))

            # Convert the Pillow image into the format EasyOCR accepts.
            image_array = np.array(image)

        if image_array.size == 0:
            raise ValueError("The uploaded image contains no readable image data.")

        results = reader.readtext(
            image_array,
            detail=0,
            paragraph=False
        )

        return "\n".join(results)

    except UnidentifiedImageError as error:
        raise ValueError(
            f'"{recipe_file.filename}" could not be opened as an image.'
        ) from error

    except OSError as error:
        raise ValueError(
            f'"{recipe_file.filename}" appears to be damaged or unsupported.'
        ) from error
