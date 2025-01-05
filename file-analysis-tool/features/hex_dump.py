import binascii
import magic
from PIL import Image
import PyPDF2
import docx
import re
import os

# Import the analyze_file_type function from file_type.py
from features.file_type import analyze_file_type

# Function to generate a hex dump of the file and analyze the file header
def hex_dump_and_header_analysis(file_path):
    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Read the first 64 bytes (for preview) to perform a hex dump and header analysis
            file_header = file.read(64)
            
            # Generate the hex dump of the first 64 bytes
            hex_dump = binascii.hexlify(file_header).decode('utf-8')
            
            # Split hex dump into pairs of hex digits for readability
            formatted_hex_dump = ' '.join(hex_dump[i:i+2] for i in range(0, len(hex_dump), 2))
            
            # Convert the hex dump into a preview of ASCII characters (for file preview)
            ascii_preview = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in file_header)

            # Analyze the file type using the function from file_type.py
            file_info = analyze_file_type(file_path)

            # Extract metadata if available using the external metadata functions
            metadata = extract_metadata(file_path)

            # Format output in the desired order
            result = {
                "File Type": file_info.get("File Type", "Unknown"),
                "Description": file_info.get("Description", "No description available"),
                "Suggested Extension": file_info.get("Suggested Extension", "Unknown"),
                "Hex Dump (First 64 Bytes)": formatted_hex_dump,
                "ASCII Preview (First 64 Bytes)": ascii_preview,
                "Metadata": metadata
            }

            return result
    except Exception as e:
        return {"Error in Hex Dump and Header Analysis": str(e)}

# Function to extract file-specific metadata (e.g., image EXIF, PDF info)
def extract_metadata(file_path):
    try:
        # Handling images
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            return extract_image_metadata(file_path)
        
        # Handling PDFs
        elif file_path.lower().endswith('.pdf'):
            return extract_pdf_metadata(file_path)
        
        # Handling Word documents
        elif file_path.lower().endswith('.docx'):
            return extract_word_metadata(file_path)
        
        # Add more file types as needed (e.g., audio, video, etc.)
        else:
            return "No specific metadata extraction implemented for this file type."
    
    except Exception as e:
        return f"Error extracting metadata: {str(e)}"

# Extract EXIF metadata from image files (JPEG, PNG, etc.)
def extract_image_metadata(file_path):
    try:
        img = Image.open(file_path)
        exif_data = img._getexif()
        if exif_data:
            metadata = {k: v for k, v in exif_data.items()}
            return metadata
        else:
            return "No EXIF metadata found."
    except Exception as e:
        return f"Error extracting image metadata: {str(e)}"

# Extract metadata from PDF files using PyPDF2
def extract_pdf_metadata(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            metadata = reader.metadata
            return {k: v for k, v in metadata.items()}
    except Exception as e:
        return f"Error extracting PDF metadata: {str(e)}"

# Extract metadata from Word documents (.docx) using python-docx
def extract_word_metadata(file_path):
    try:
        doc = docx.Document(file_path)
        core_properties = doc.core_properties
        metadata = {
            "Author": core_properties.author,
            "Title": core_properties.title,
            "Subject": core_properties.subject,
            "Created": core_properties.created,
            "Modified": core_properties.modified
        }
        return metadata
    except Exception as e:
        return f"Error extracting Word metadata: {str(e)}"
"""
# Example usage
file_path = input('Enter the file path:')  # Replace with the actual file path
hex_dump_info = hex_dump_and_header_analysis(file_path)

# Print the result in a structured format
for key, value in hex_dump_info.items():
    print(f"{key}: {value}")"""

