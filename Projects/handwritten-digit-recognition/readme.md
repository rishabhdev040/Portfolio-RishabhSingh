# Handwritten Digit Recognition using CNN

## Project Overview

This project implements a Handwritten Digit Recognition System using a Convolutional Neural Network (CNN) built with PyTorch. Trained on the MNIST dataset, the model classifies handwritten digit images into one of ten classes (0–9).

A Streamlit web interface allows users to upload handwritten digit images, view predictions, and explore class-wise confidence scores. The trained model is saved as a `.pth` checkpoint and reused for real-time inference without retraining.

## Features
- CNN-based handwritten digit classification.
- Pre-trained PyTorch model (`convNet_model.pth`).
- Upload handwritten digit images (PNG, JPG, JPEG).
- Image preprocessing and normalization.
- Displays predicted digit and confidence score.
- Visualizes class-wise prediction probabilities.

## Tech Stack
- Python
- PyTorch
- CNN
- MNIST Dataset
- Streamlit
- NumPy
- Pillow

## Project Structure

```text
Handwritten-Digit-Recognition/
│
├── app.py
├── model.py
├── convNet_model.pth
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd Handwritten-Digit-Recognition
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Usage
1. Upload a handwritten digit image.
2. Click **Predict Digit**.
3. View the predicted digit and confidence score.
4. Explore class-wise prediction probabilities.
