import os
from PIL import Image
from features.lsb.mode import detect_image_mode  # Import the function from mode.py

def extract_lsb(pixel_value, num_bits=1):
    """
    Extract the least significant bits from the pixel value.
    By default, it extracts 1 bit, but can be configured for 2-bit extraction.
    """
    return pixel_value & ((1 << num_bits) - 1)

def extract_hidden_data(image_path, num_bits=1):
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Get the mode of the image using detect_image_mode from mode.py
        img_mode = detect_image_mode(image_path)
        print(f"Analyzing LSB for image mode: {img_mode}")
        
        # Convert the image to a list of pixel values
        pixels = img.load()
        
        # Initialize a list to store extracted bits
        bitstream = []
        
        # Perform LSB extraction based on the image mode
        width, height = img.size
        for x in range(width):
            for y in range(height):
                pixel = pixels[x, y]
                if img_mode in ['RGB', 'P', 'RGBA']:  # RGB or RGBA mode
                    # Extract LSB from RGB channels
                    for color in pixel[:3]:  # Only RGB channels (skip Alpha in RGBA)
                        bitstream.append(extract_lsb(color, num_bits))
                elif img_mode in ['RGBA', 'CMYK', 'I', 'F']:  # Non-RGB (Alpha, CMYK, Grayscale)
                    if img_mode == 'RGBA':
                        # Extract LSB from Alpha channel
                        alpha = pixel[3]
                        bitstream.append(extract_lsb(alpha, num_bits))
                    elif img_mode == 'CMYK':
                        # Extract LSB from each CMYK channel
                        for color in pixel:
                            bitstream.append(extract_lsb(color, num_bits))
                    else:  # Grayscale modes (I, F)
                        bitstream.append(extract_lsb(pixel, num_bits))
                else:
                    continue
        
        # Now, let's convert the bitstream to bytes and then to text
        # Group the bits into bytes
        byte_stream = []
        for i in range(0, len(bitstream), 8):
            byte = 0
            for j in range(8):
                if i + j < len(bitstream):
                    byte = (byte << 1) | bitstream[i + j]
            byte_stream.append(byte)
        
        # Convert byte stream to text (assuming the hidden data is ASCII encoded)
        hidden_data = ''.join(chr(byte) for byte in byte_stream if 32 <= byte <= 126)  # Printable characters

        # Return the extracted hidden data (as text)
        return hidden_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_hidden_data_to_file(image_path, hidden_data, num_bits=1):
    try:
        # Get the mode and original file name using detect_image_mode
        img_mode = detect_image_mode(image_path)
        base_name = os.path.basename(image_path)  # Get the base name of the image (without path)
        
        # Generate the new file name based on the mode and the original file name
        name_without_ext, _ = os.path.splitext(base_name)
        new_file_name = f"{name_without_ext}_{img_mode}_{num_bits}_bit_LSB_hidden_data.txt"
        
        # Save the hidden data to a new file
        with open(new_file_name, 'w') as f:
            f.write(hidden_data)
        
        print(f"Hidden data successfully extracted and saved to: {new_file_name}")
    
    except Exception as e:
        print(f"An error occurred while saving the hidden data: {e}")

# Main logic
def main():
    image_path = input("Enter the image path: ")  # Only ask once for the image path
    
    # Extract and save hidden data for 1-bit LSB
    hidden_data_1bit = extract_hidden_data(image_path, num_bits=1)
    if hidden_data_1bit:
        save_hidden_data_to_file(image_path, hidden_data_1bit, num_bits=1)
    else:
        print("No hidden data found or an error occurred during 1-bit extraction.")
    
    # Extract and save hidden data for 2-bit LSB
    hidden_data_2bit = extract_hidden_data(image_path, num_bits=2)
    if hidden_data_2bit:
        save_hidden_data_to_file(image_path, hidden_data_2bit, num_bits=2)
    else:
        print("No hidden data found or an error occurred during 2-bit extraction.")

# Run the main function
if __name__ == "__main__":
    main()

