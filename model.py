import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process
import re

# Load medicine data
data = pd.read_csv("your_data.csv") 
data.fillna('', inplace=True)

# Create and train KNN model
vectorizer = CountVectorizer()
composition_vectors = vectorizer.fit_transform(data['example_composition1'])
knn_model = NearestNeighbors(n_neighbors=5, metric='euclidean')
knn_model.fit(composition_vectors)

def split_medicine_name(medicine_name):
    """
    Splits the medicine name into name and dosage.

    Args:
        medicine_name (str): The medicine name.

    Returns:
        tuple: A tuple containing the medicine name and dosage.
    """
    # Define regular expression pattern to split medicine name
    pattern = r'(?P<name>[a-zA-Z\s-]+)\s*(?P<dosage>\d+\s?(?:mg|g|ml)?|\bTablet\b|\bCapsule\b)?'
    match = re.match(pattern, medicine_name)
    if match:
        name = match.group('name').strip()
        dosage = match.group('dosage').strip() if match.group('dosage') else None
        return name, dosage
    else:
        return None, None

def find_composition_and_alternatives(input_med_names, knn_model, vectorizer, data):
    """
    Finds the composition of the input medicines and their alternative medicines.

    Args:
        input_med_names (list): A list of input medicine names.
        knn_model: The trained KNN model.
        vectorizer: The CountVectorizer used for vectorization.
        data: A pandas DataFrame containing medicine information.

    Returns:
        list: A list of tuples containing the matched medicine name, the composition of the input medicine,
              and a list of alternative medicines for each input medicine.
    """
    results = []
    for input_med_name in input_med_names:
        # Split medicine name into name and dosage
        name, dosage = split_medicine_name(input_med_name)

        if name:
            # Use fuzzy matching to find closest match in the dataset
            matched_name = process.extractOne(name, data['name'])[0]

            # Find composition of matched medicine
            input_composition = data.loc[data['name'] == matched_name, 'short_composition1'].values[0]

            # Find nearest neighbors using KNN
            input_vector = vectorizer.transform([input_composition])
            distances, indices = knn_model.kneighbors(input_vector)

            # Get names of alternative medicines
            alternative_medicines = data.iloc[indices[0]][data.columns[0]].tolist()

            results.append((matched_name, input_composition, alternative_medicines))
        else:
            # Handle case where medicine name couldn't be split
            results.append((input_med_name, "N/A", []))

    return results

# Example medicine names (list of strings)
input_med_names = ["Cetapin XR 500mg", "Met XL 50 Tablet"]

# Find matched medicine names, compositions, and alternative medicines
results = find_composition_and_alternatives(input_med_names, knn_model, vectorizer, data)

# Print the results
for idx, (matched_name, composition, alternative_medicines) in enumerate(results, start=1):
    print(f"Result {idx}:")
    print(f"Matched medicine name: {matched_name}")
    print(f"Composition of {matched_name}: {composition}")
    print(f"Alternative medicines for {matched_name}:")
    for medicine in alternative_medicines:
        print(medicine)
    print()
