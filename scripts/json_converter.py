import re
import json
from ocr_module import extract_text_easyocr


# Function to parse key data points
def extract_key_data(text):
    data = {}

    # Regex patterns for extracting specific fields
    name_pattern = re.search(r"Name[:\-]?\s*([A-Za-z ]+)", text)
    dob_pattern = re.search(r"DOB[:\-]?\s*(\d{2}/\d{2}/\d{4})", text)
    date_pattern = re.search(r"Date[:\-]?\s*(\d{2}/\d{2}/\d{4})", text)
    injection_pattern = re.search(r"Injection[:\-]?\s*(Yes|No)", text, re.IGNORECASE)
    therapy_pattern = re.search(r"Exercise Therapy[:\-]?\s*(Yes|No)", text, re.IGNORECASE)
    
    # Extracting values
    data["patient_name"] = name_pattern.group(1) if name_pattern else "Unknown"
    data["dob"] = dob_pattern.group(1) if dob_pattern else "Unknown"
    data["date"] = date_pattern.group(1) if date_pattern else "Unknown"
    data["injection"] = injection_pattern.group(1) if injection_pattern else "Unknown"
    data["exercise_therapy"] = therapy_pattern.group(1) if therapy_pattern else "Unknown"

    # Extract difficulty ratings (0-5)
    difficulties = ["bending", "putting on shoes", "sleeping"]
    data["difficulty_ratings"] = {d: int(re.search(fr"{d}[:\-]?\s*(\d)", text).group(1)) if re.search(fr"{d}[:\-]?\s*(\d)", text) else 0 for d in difficulties}

    # Extract pain symptoms (0-10)
    symptoms = ["pain", "numbness", "tingling", "burning", "tightness"]
    data["pain_symptoms"] = {s: int(re.search(fr"{s}[:\-]?\s*(\d+)", text).group(1)) if re.search(fr"{s}[:\-]?\s*(\d+)", text) else 0 for s in symptoms}

    # Convert extracted data to JSON
    json_data = json.dumps(data, indent=4)
    
    return json_data

if __name__ == "__main__":
    text = extract_text_easyocr("patient_form/sample.jpg")
    structured_json = extract_key_data(text)
    print("\nExtracted JSON Data:\n", structured_json)

    # Save JSON to file
    with open("result.json", "w") as json_file:
        json_file.write(structured_json)
