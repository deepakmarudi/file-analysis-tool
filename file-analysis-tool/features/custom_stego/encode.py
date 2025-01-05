# encode.py

import numpy as np
from PIL import Image
import random
import os
from poly import polyalphabetic_encrypt

# Function to embed data into an image using LSB and encrypt it with polyalphabetic cipher
def embed_data_in_image(image_path, data, key):
    # Encrypt the data using polyalphabetic cipher
    encrypted_data = polyalphabetic_encrypt(data, key)
    
    # Convert encrypted data to binary format
    binary_data = ''.join(format(ord(char), '08b') for char in encrypted_data)
    
    # Load the image
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = np.array(img)
    
    # Flatten the pixel array and prepare it for embedding binary data
    pixel_indices = [(i, j) for i in range(pixels.shape[0]) for j in range(pixels.shape[1])]
    random.seed(sum(ord(c) for c in key))  # Use the key to generate a deterministic random sequence
    random.shuffle(pixel_indices)  # Re-randomize the pixel indices based on the key
    
    # Embed the binary data into the LSB of the image
    data_index = 0
    for i, j in pixel_indices:
        if data_index >= len(binary_data):
            break
        pixel = list(pixels[i, j])  # Get the RGB values as a list
        for k in range(3):  # For each channel (R, G, B)
            if data_index < len(binary_data):
                # Replace the LSB with the binary data bit
                pixel[k] = (pixel[k] & ~1) | int(binary_data[data_index])
                data_index += 1
        pixels[i, j] = tuple(pixel)  # Update the pixel with the modified value
    
    # Save the modified image
    output_image_path = os.path.splitext(image_path)[0] + "_encoded.png"  # Add "_encoded" to the original file name
    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_image_path)
    
    print(f"Data successfully encoded and saved to: {output_image_path}")
    return output_image_path


# Example Usage
if __name__ == "__main__":
    image_path = input("Enter the image path:")  # Image to hide data in
    data = input("give the data to hide:")  # Data to hide in the image
    key = input("Enter the key:")  # Key used for encryption and randomization
    
    # Embed data and encrypt it in the image
    encoded_image_path = embed_data_in_image(image_path, data, key)

