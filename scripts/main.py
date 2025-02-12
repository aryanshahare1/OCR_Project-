from db_module import insert_data
from ocr_module import extract_text_tesseract



if __name__ == "__main__":
    image_path = "patient_form/sample.jpg"
    insert_data(image_path)
    print("OCR, JSON conversion, and Database insertion completed successfully!")
