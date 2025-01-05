import re
import chardet
import PyPDF2
import docx
import pytesseract
from PIL import Image
import os

# Import the analyze_file_type function from file_type.py
from features.file_type import analyze_file_type


def extract_text_from_file(file_path):
    """
    Extracts text from a file based on its type.
    :param file_path: Path to the file
    :return: Extracted text or an error message
    """
    try:
        # Analyze the file type
        file_info = analyze_file_type(file_path)
        
        if "Error" in file_info:
            return file_info  # Return error message if file type analysis failed
        
        # Extract file type and extension info
        file_type = file_info.get("File Type", "")
        file_extension = file_info.get("Suggested Extension", "").lower()

        if file_type.startswith("text") or file_extension in [".txt", ".log", ".csv"]:
            return extract_text_from_generic_file(file_path)
        elif file_type == "application/pdf" or file_extension == ".pdf":
            return extract_text_from_pdf(file_path)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file_extension == ".docx":
            return extract_text_from_word(file_path)
        elif file_type.startswith("image"):
            return extract_text_from_image(file_path)
        else:
            return extract_text_from_generic_file(file_path)

    except Exception as e:
        return f"Error extracting text from {file_path}: {e}"


def extract_text_from_generic_file(file_path):
    """
    Extract text from generic text-based or binary files.
    :param file_path: Path to the file
    :return: Extracted text
    """
    try:
        with open(file_path, "rb") as file:
            raw_data = file.read()

        result = chardet.detect(raw_data)
        encoding = result.get("encoding", "utf-8")

        try:
            text = raw_data.decode(encoding)
        except (UnicodeDecodeError, TypeError):
            text = raw_data.decode("latin-1", errors="ignore")

        readable_text = re.sub(r"[^\x20-\x7E\u00A0-\uFFFF\n\r\t]", "", text)
        return readable_text.strip() or "No readable text found."
    except Exception as e:
        return f"Error extracting text from {file_path}: {e}"


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF files.
    :param file_path: Path to the PDF file
    :return: Extracted text
    """
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    page_text = re.sub(r"[^\x20-\x7E\u00A0-\uFFFF\n\r\t]", "", page_text)
                    text += page_text
        return text.strip() or "No readable text found in the PDF."
    except Exception as e:
        return f"Error extracting text from PDF: {e}"


def extract_text_from_word(file_path):
    """
    Extract text from Word documents (.docx).
    :param file_path: Path to the Word file
    :return: Extracted text
    """
    try:
        doc = docx.Document(file_path)
        text = ""
        for para in doc.paragraphs:
            para_text = re.sub(r"[^\x20-\x7E\u00A0-\uFFFF\n\r\t]", "", para.text)
            text += para_text + "\n"
        return text.strip() or "No readable text found in the Word document."
    except Exception as e:
        return f"Error extracting text from Word document: {e}"


def extract_text_from_image(file_path):
    """
    Extract text from images using OCR (pytesseract).
    :param file_path: Path to the image file
    :return: Extracted text
    """
    try:
        img = Image.open(file_path)
        raw_text = pytesseract.image_to_string(img)
        readable_text = re.sub(r"[^\x20-\x7E\u00A0-\uFFFF\n\r\t]", "", raw_text)
        return readable_text.strip() or "No readable text found in the image."
    except Exception as e:
        return f"Error extracting text from image: {e}"

"""
# Example usage:
if __name__ == "__main__":
    file_path = input("Enter the file path: ")  # Replace with the actual file path
    extracted_text = extract_text_from_file(file_path)
    print(extracted_text)"""

