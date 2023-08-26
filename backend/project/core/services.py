from PIL import Image


def image_to_rectangle(image_path):
    image = Image.open(image_path)
    width, height = image.size
    new_size = min(width, height)
    left = (width - new_size) // 2
    top = (height - new_size) // 2
    right = (width + new_size) // 2
    bottom = (height + new_size) // 2
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image
