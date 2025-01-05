import os
from PIL import Image
from features.lsb.mode import detect_image_mode  # Import the mode detection function

def extract_lsb(pixel_value):
    """Extract the least significant bit from the pixel value."""
    return pixel_value & 1

def extract_hidden_data_by_channel(image_path):
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Get the mode of the image using detect_image_mode from mode.py
        img_mode = detect_image_mode(image_path)
        print(f"Analyzing LSB for image mode: {img_mode}")
        
        # Ensure the image is in a supported mode
        if img_mode not in ['RGB', 'RGBA']:
            raise ValueError("This script only supports images in RGB or RGBA mode.")
        
        # Load pixel data
        pixels = img.load()
        width, height = img.size

        # Initialize bitstreams for each channel
        bitstream_red = []
        bitstream_green = []
        bitstream_blue = []
        bitstream_alpha = []  # For RGBA mode only

        # Extract LSBs from each channel
        for x in range(width):
            for y in range(height):
                pixel = pixels[x, y]
                bitstream_red.append(extract_lsb(pixel[0]))    # Red channel
                bitstream_green.append(extract_lsb(pixel[1]))  # Green channel
                bitstream_blue.append(extract_lsb(pixel[2]))   # Blue channel
                if img_mode == 'RGBA':  # Alpha channel for RGBA mode
                    bitstream_alpha.append(extract_lsb(pixel[3]))

        # Convert bitstreams to text
        hidden_data_red = bits_to_text(bitstream_red)
        hidden_data_green = bits_to_text(bitstream_green)
        hidden_data_blue = bits_to_text(bitstream_blue)
        hidden_data_alpha = bits_to_text(bitstream_alpha) if img_mode == 'RGBA' else None

        return hidden_data_red, hidden_data_green, hidden_data_blue, hidden_data_alpha

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None

def bits_to_text(bitstream):
    """Convert a list of bits to text (ASCII-encoded characters)."""
    byte_stream = []
    for i in range(0, len(bitstream), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bitstream):
                byte = (byte << 1) | bitstream[i + j]
        byte_stream.append(byte)
    return ''.join(chr(byte) for byte in byte_stream if 32 <= byte <= 126)

def save_hidden_data_to_files(image_path, hidden_data_red, hidden_data_green, hidden_data_blue, hidden_data_alpha):
    try:
        # Get the original file name without extension
        base_name = os.path.basename(image_path)
        name_without_ext, _ = os.path.splitext(base_name)

        # File names for each channel
        red_file_name = f"{name_without_ext}_Red_hidden_data.txt"
        green_file_name = f"{name_without_ext}_Green_hidden_data.txt"
        blue_file_name = f"{name_without_ext}_Blue_hidden_data.txt"
        alpha_file_name = f"{name_without_ext}_Alpha_hidden_data.txt" if hidden_data_alpha else None

        # Save data for Red, Green, and Blue channels
        with open(red_file_name, 'w') as red_file:
            red_file.write("Hidden Data from Red Channel:\n")
            red_file.write(hidden_data_red)
        with open(green_file_name, 'w') as green_file:
            green_file.write("Hidden Data from Green Channel:\n")
            green_file.write(hidden_data_green)
        with open(blue_file_name, 'w') as blue_file:
            blue_file.write("Hidden Data from Blue Channel:\n")
            blue_file.write(hidden_data_blue)

        # Save data for Alpha channel if present
        if hidden_data_alpha:
            with open(alpha_file_name, 'w') as alpha_file:
                alpha_file.write("Hidden Data from Alpha Channel:\n")
                alpha_file.write(hidden_data_alpha)

        print(f"Hidden data successfully extracted and saved to:")
        print(f"  - {red_file_name}")
        print(f"  - {green_file_name}")
        print(f"  - {blue_file_name}")
        if alpha_file_name:
            print(f"  - {alpha_file_name}")

    except Exception as e:
        print(f"An error occurred while saving hidden data: {e}")

# Main logic
"""def main():
    image_path = input("Enter the image path: ")  # Get the image path from user
    hidden_data_red, hidden_data_green, hidden_data_blue, hidden_data_alpha = extract_hidden_data_by_channel(image_path)

    # Save extracted data to files if extraction was successful
    if hidden_data_red or hidden_data_green or hidden_data_blue or hidden_data_alpha:
        save_hidden_data_to_files(image_path, hidden_data_red, hidden_data_green, hidden_data_blue, hidden_data_alpha)
    else:
        print("No hidden data found or an error occurred.")

# Run the main function
if __name__ == "__main__":
    main()"""

