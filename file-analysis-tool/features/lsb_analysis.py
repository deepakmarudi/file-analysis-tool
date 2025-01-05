import os
from features.lsb.lsb_line_analysis import extract_hidden_data, save_hidden_data_to_file
from features.lsb.lsb_each_colour import extract_hidden_data_by_channel, save_hidden_data_to_files

def analyze_lsb(image_path):
    # Ensure the image file exists
    if not os.path.isfile(image_path):
        print("The specified file does not exist. Please try again.")
        return None

    output_files = []

    # Perform Line-based LSB Analysis
    print("\nStarting 1-bit LSB extraction...")
    try:
        hidden_data_1bit = extract_hidden_data(image_path, num_bits=1)
        if hidden_data_1bit:
            file_name1 = save_hidden_data_to_file(image_path, hidden_data_1bit, num_bits=1)
            output_files.append(file_name1)
        else:
            print("No hidden data found or an error occurred during 1-bit extraction.")

    except Exception as e:
        print(f"An error occurred during Line-based LSB analysis: {e}")
    # Extract and save hidden data for 2-bit LSB
    print("Starting 2-bit LSB extraction...")
    try:
        hidden_data_2bit = extract_hidden_data(image_path, num_bits=2)
        if hidden_data_2bit:
            file_name2 = save_hidden_data_to_file(image_path, hidden_data_2bit, num_bits=2)
            output_files.append(file_name2)
        else:
            print("No hidden data found or an error occurred during 2-bit extraction.")
    except Exception as e:
        print(f"An error occurred during Line-based LSB analysis: {e}")

    # Perform Channel-based LSB Analysis (RGB/Alpha)
    print("\nPerforming Channel-based LSB Analysis...")
    try:
        hidden_data_red, hidden_data_green, hidden_data_blue, hidden_data_alpha = extract_hidden_data_by_channel(image_path)
        if hidden_data_red or hidden_data_green or hidden_data_blue or hidden_data_alpha:
            files = save_hidden_data_to_files(image_path, hidden_data_red, hidden_data_green, hidden_data_blue, hidden_data_alpha)
            output_files.extend(files)
        else:
            print("No hidden data found during Channel-based LSB analysis.")
    except Exception as e:
        print(f"An error occurred during Channel-based LSB analysis: {e}")

    return output_files

