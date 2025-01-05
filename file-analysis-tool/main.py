import os
from features.file_type import analyze_file_type
from features.text_extraction import extract_text_from_file
from features.hex_dump import hex_dump_and_header_analysis
from features.lsb_analysis import analyze_lsb  # Correct path to lsb_analysis.py

def main(file_path):
    result = {}

    # File Type Analysis
    print("Analyzing file type...")
    file_type_info = analyze_file_type(file_path)
    result['File Type Analysis'] = file_type_info

    # Text Extraction
    print("Extracting text from file...")
    extracted_text = extract_text_from_file(file_path)
    result['Text Extraction'] = extracted_text

    # Hex Dump and Header Analysis
    print("Generating hex dump and analyzing header...")
    hex_dump_info = hex_dump_and_header_analysis(file_path)
    result['Hex Dump and Header Analysis'] = hex_dump_info

    # LSB Analysis
    print("Performing LSB Analysis...")
    lsb_analysis_info = analyze_lsb(file_path)
    result['LSB Analysis'] = lsb_analysis_info

    return result

# Example usage:
if __name__ == "__main__":
    file_path = input("Enter the file path for analysis: ")
    
    if os.path.isfile(file_path):
        results = main(file_path)
        for key, value in results.items():
            print(f"\n{key}:\n{value}\n")
    else:
        print("Invalid file path.")

