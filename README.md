AI Powered Medical HealtCare

This repository provides a comprehensive solution for recognizing text from medical prescriptions and predicting the corresponding medicines along with their compositions using advanced machine learning models. The repository consists of three main components: Frontend, Backend, and Machine Learning Model files.

Table of Contents
Overview
Frontend
Backend
Machine Learning Model

"The AI-Powered-Medical-HealthCare project is structured into three key parts:"

Frontend: Implements a basic user interface using Streamlit, allowing users to upload their prescriptions and view the extracted text using Optical Character Recognition (OCR).
Backend: Connects the frontend components with the Google API and the machine learning model to predict and return the correct medicines along with their compositions.
Machine Learning Model Files: Contains the machine learning models and scripts used to predict the medicines, providing clarity on the models used and their implementation.
Frontend
The frontend is developed using Streamlit, which allows for an interactive and user-friendly interface. Users can upload their prescriptions, and the interface will display the scanned text from the OCR.

Features
Upload prescription images
Display scanned text from OCR
Simple and intuitive user interface
Files
app.py: Main file for the Streamlit app
components/: Directory containing UI components
Backend
The backend handles the interaction between the frontend, Google API, and the machine learning model. It processes the uploaded images, extracts text using OCR, and predicts the medicines along with their compositions.

Features
Integrates with Google API for OCR
Connects to the machine learning model for predictions
Handles data processing and API interactions
Files
backend/ocr.py: Script for handling OCR using Google API
backend/predict.py: Script for handling model predictions
backend/utils.py: Utility functions for data processing
Machine Learning Model
The machine learning model files include the models and scripts used for predicting medicines. Detailed explanations and documentation are provided to help users understand the models and their implementation.

Features
Predicts medicines from extracted text
Provides medicine compositions
