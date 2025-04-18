# utils/model_utils.py

import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import json

# # Path to dataset
# DATASET_PATH = r"C:\Users\manas\Documents\PlantVillage\Plant_leave_diseases_dataset_without_augmentation"
# Use relative path instead of absolute Windows path
DATASET_PATH = os.path.join("data", "Plant_leave_diseases_dataset_without_augmentation")
SOLUTIONS_PATH = os.path.join(os.path.dirname(__file__), "solutions.json")

# # Get class names from the dataset folder
# def get_class_names():
#     return sorted(os.listdir(DATASET_PATH))

def get_class_names():
    return sorted([
        'Apple___Apple_scab',
        'Apple___Black_rot',
        'Apple___Cedar_apple_rust',
        'Apple___healthy',
        'Corn___Cercospora_leaf_spot Gray_leaf_spot',
        'Corn___Common_rust',
        'Corn___healthy',
        'Corn___Northern_Leaf_Blight',
        # Add all the other class labels used during training
    ])


# Load the trained model
def load_trained_model(model_path):
    model = load_model(model_path)
    class_names = get_class_names()
    return model, class_names

# Preprocess the image to feed into the model
def preprocess_image(image_path):
    try:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        img = cv2.resize(img, (128, 128))           # Resize to model's expected size
        img = img.astype('float32') / 255.0         # Normalize to [0, 1]
        img = np.expand_dims(img, axis=0)           # Add batch dimension -> (1, 128, 128, 3)
        return img
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None

# Predict the disease class and return the solution
def predict_disease(model, img_array, class_names):
    predictions = model.predict(img_array)
    confidence = np.max(predictions)
    predicted_class = class_names[np.argmax(predictions)]

    # Load solutions
    try:
        with open(SOLUTIONS_PATH, "r") as f:
            solutions = json.load(f)
        
        solution_entry = solutions.get(predicted_class, {"solution": "Solution not found."})
        solution = solution_entry["solution"]


    except Exception as e:
        print(f"Error loading solutions: {e}")
        solution = "Solution file missing or unreadable."

    return predicted_class, confidence, solution
