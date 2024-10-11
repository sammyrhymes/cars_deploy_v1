from PIL import Image

def check_image_properties(image_path):
    # Open the image using Pillow
    with Image.open(image_path) as img:
        # Get image size
        width, height = img.size
        print(f"Image Size: {width} x {height} pixels")

        # Get image format
        print(f"Image Format: {img.format}")

        # Get image mode (e.g., 'RGB', 'L' for grayscale, etc.)
        print(f"Image Mode: {img.mode}")

        # Display additional details
        if img.format in ['JPEG', 'PNG']:
            print(f"Image Quality: Usually 85 for JPEG, 100 for PNG (lossless)")

# Example usage
check_image_properties('static/assets/img/photo_2024-10-09_13-04-37.jpg')
