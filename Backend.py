from fastapi import FastAPI, File, UploadFile
from google.cloud import vision
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process
import re


app = FastAPI()

# Set the credentials path for Google Cloud Vision API
credentials_path = r'path\user\credentials'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Load medicine data
data = pd.read_csv("your_data.csv")
data.fillna('', inplace=True)

# Create and train KNN model
vectorizer = CountVectorizer()
composition_vectors = vectorizer.fit_transform(data['example_composition'])
knn_model = NearestNeighbors(n_neighbors=5, metric='euclidean')
knn_model.fit(composition_vectors)

def detect_text_from_image(image_bytes):
    """Detects text in an image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        detected_text = texts[0].description
        return detected_text
    else:
        return None

def extract_medicine_names(detected_text):
    """Extracts medicine names from detected text using regular expressions."""
    pattern = r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+[IVXLCDM]+)?(?:\s+\d{1,4}(?:\.\d{1,2})?(?:mg|g|ml|mcg)?)?"
    matches = re.findall(pattern, detected_text)
    medicine_names = [match.strip() for match in matches if len(match.strip().split()) > 1]
    return medicine_names

def find_composition_and_alternatives(input_med_names, knn_model, vectorizer, data):
    """Finds the composition of the input medicines and their alternative medicines."""
    results = []
    for input_med_name in input_med_names:
        matched_name = process.extractOne(input_med_name, data['name'])[0]
        input_composition = data.loc[data['name'] == matched_name, 'short_composition1'].values[0]
        input_vector = vectorizer.transform([input_composition])
        distances, indices = knn_model.kneighbors(input_vector)
        alternative_medicines = data.iloc[indices[0]][data.columns[0]].tolist()
        results.append((matched_name, input_composition, alternative_medicines))
    return results

@app.post("/perform_ocr")
async def perform_ocr(image: UploadFile = File(...)):
    """Endpoint to perform OCR on an image and extract medicine information."""
    # Read image file content
    image_content = await image.read()

    # Perform OCR on the image
    detected_text = detect_text_from_image(image_content)

    if detected_text:
        # Extract medicine names from detected text
        extracted_medicine_names = extract_medicine_names(detected_text)

        # Find matched medicine names, compositions, and alternative medicines
        results = find_composition_and_alternatives(extracted_medicine_names, knn_model, vectorizer, data)

        # Format results
        formatted_results = ""
        for idx, (matched_name, composition, alternative_medicines) in enumerate(results, start=1):
            formatted_results += f"Matched medicine name: {matched_name}"
            formatted_results += f"Composition of matched medicine: {composition}"
            formatted_results += f"Alternative medicines for matched medicine:"
            formatted_results += "\n".join(alternative_medicines)

        return formatted_results
    else:
        return "No text detected in the image"
