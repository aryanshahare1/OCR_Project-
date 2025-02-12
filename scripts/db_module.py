import psycopg2
import json
from json_converter import extract_key_data, extract_text_easyocr

conn = psycopg2.connect(
    dbname="ocr_project",
    user="postgres",
    password="aryanshahare9",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# Insert patient and form data into database
def insert_data(image_path):
    text = extract_text_easyocr(image_path)
    json_data = extract_key_data(text)
    data = json.loads(json_data)

    # Insert patient
    cursor.execute("INSERT INTO patients (name, dob) VALUES (%s, %s) RETURNING id", (data["patient_name"], data["dob"]))
    patient_id = cursor.fetchone()[0]

    # Insert form data
    cursor.execute("INSERT INTO forms_data (patient_id, form_json) VALUES (%s, %s)", (patient_id, json.dumps(data)))

    conn.commit()
    print("Data inserted successfully!")

if __name__ == "__main__":
    insert_data("patient_form/sample.jpg")

    # Close connection
    cursor.close()
    conn.close()
