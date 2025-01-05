import magic
import mimetypes

def analyze_file_type(file_path):
    


    try:
    
        mime_detector = magic.Magic(mime=True)
        
        detailed_magic = magic.Magic()  

        
        
        file_type = mime_detector.from_file(file_path)
        
        description = detailed_magic.from_file(file_path)
        
        extension = mimetypes.guess_extension(file_type) or "unknown"

        return {
            "File Type": file_type,
            "Description": description,
            "Suggested Extension": extension
        }
    except Exception as e:
        return {"Error in File Type Analysis": str(e)}

