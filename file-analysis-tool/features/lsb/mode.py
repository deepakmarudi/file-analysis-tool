from PIL import Image

def detect_image_mode(image_path):
    # Open the image using Pillow
    img = Image.open(image_path)
    
    # Get the mode of the image
    img_mode = img.mode
    
    # Return the mode of the image
    return img_mode

