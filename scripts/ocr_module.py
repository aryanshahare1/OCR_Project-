import cv2
import pytesseract
import easyocr
import os

# Set Tesseract path (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to preprocess image for better OCR accuracy
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # Thresholding
    return thresh

# Extract text using Tesseract OCR
def extract_text_tesseract(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image)
    return text.strip()

# Extract text using EasyOCR
def extract_text_easyocr(image_path):
    result = reader.readtext(image_path, detail=0)
    return " ".join(result)

if __name__ == "__main__":
    # Path to the sample image
    image_path = "patient_form/sample.jpg"

    # Check if the image exists
    if not os.path.exists(image_path):
        print(f"Sample image not found! Please add an image to '{image_path}'.")
    else:
        print("Tesseract OCR Output:\n", extract_text_tesseract(image_path))
        print("\nEasyOCR Output:\n", extract_text_easyocr(image_path))
