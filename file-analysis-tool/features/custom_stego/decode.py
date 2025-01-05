# decode.py

import numpy as np
from PIL import Image
import random
import os
from poly import polyalphabetic_decrypt

# Function to decode data from an image and decrypt it
def decode_image(image_path, key):
    # Load the image
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = np.array(img)
    
    # Flatten the pixel array and prepare it for extracting binary data
    pixel_indices = [(i, j) for i in range(pixels.shape[0]) for j in range(pixels.shape[1])]
    random.seed(sum(ord(c) for c in key))  # Use the key to generate a deterministic random sequence
    random.shuffle(pixel_indices)  # Re-randomize the pixel indices based on the key
    
    binary_data = []
    
    # Extract the binary data from the LSB of each pixel
    for i, j in pixel_indices:
        pixel = list(pixels[i, j])  # Get the RGB values as a list
        for k in range(3):  # For each channel (R, G, B)
            binary_data.append(str(pixel[k] & 1))  # Get the LSB of the pixel
    
    # Join the binary data into a single string
    binary_data = ''.join(binary_data)
    
    # Debugging: Check if the binary data is a multiple of 8 bits (valid for text conversion)
    print(f"Binary data length: {len(binary_data)}")
    if len(binary_data) % 8 != 0:
        print("Warning: Binary data length is not a multiple of 8 bits. This may indicate a problem with the data embedding process.")
    
    # Convert the binary data back to text (8 bits per character)
    extracted_data = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
    
    # Debugging: Check the extracted text before decryption
    print(f"Extracted Data (before decryption): {extracted_data[:100]}...")  # Preview the first 100 characters
    
    # Decrypt the extracted data using polyalphabetic decryption
    decrypted_data = polyalphabetic_decrypt(extracted_data, key)
    
    # Debugging: Check the decrypted data
    print(f"Decrypted Data: {decrypted_data[:100]}...")  # Preview the first 100 characters of decrypted data
    
    # Generate output file name by removing extension from the input image name
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = f"{base_name}_decoded.txt"  # Add "_decoded" to the original file name for output
    
    # Save the decrypted data to a text file
    with open(output_path, "w") as output_file:
        output_file.write(decrypted_data)
    
    print(f"Decoded and Decrypted Data saved as: {output_path}")
    return decrypted_data


# Example Usage
if __name__ == "__main__":
    image_path = input("Enter the image path:")  # Image with hidden data
    key = input("Enter the key:")  # Key used during encoding and randomization
    
    # Decode and decrypt the data
    decoded_data = decode_image(image_path, key)

