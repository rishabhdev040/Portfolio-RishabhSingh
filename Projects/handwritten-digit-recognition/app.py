
import streamlit as st
import torch
import torch.nn.functional as F

from PIL import Image, ImageOps
from torchvision import transforms

from model import ConvNet


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Handwritten Digit Recognition",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 Handwritten Digit Recognition")

st.write(
    "Upload an image of a handwritten digit "
    "and let the CNN model predict the digit."
)


# -------------------------------
# Load Trained Model
# -------------------------------

@st.cache_resource
def load_model():

    model = ConvNet()

    state_dict = torch.load(
        "convNet_model.pth",
        map_location="cpu",
        weights_only=True
    )

    # Support common checkpoint dictionaries
    if "state_dict" in state_dict:
        state_dict = state_dict["state_dict"]
    elif "model_state_dict" in state_dict:
        state_dict = state_dict["model_state_dict"]

    # Handle checkpoints saved from DataParallel
    if any(k.startswith("module.") for k in state_dict):
        state_dict = {
            k.replace("module.", "", 1): v
            for k, v in state_dict.items()
        }

    model.load_state_dict(state_dict)
    model.eval()

    return model


# -------------------------------
# Image Preprocessing
# -------------------------------

def preprocess_image(image):

    image = ImageOps.grayscale(image)

    # MNIST uses a black background.
    # Invert images with a bright background.
    border_pixels = [
        image.getpixel((x, y))
        for x, y in [
            (0, 0), (27, 0), (0, 27), (27, 27)
        ]
    ]

    if sum(border_pixels) / len(border_pixels) > 127:
        image = ImageOps.invert(image)

    image = image.resize((28, 28), Image.Resampling.LANCZOS)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    image_tensor = transform(image)

    image_tensor = image_tensor.unsqueeze(0)

    return image_tensor, image


# -------------------------------
# Prediction
# -------------------------------

def predict_digit(model, image):

    image_tensor, processed_image = preprocess_image(image)

    with torch.no_grad():

        outputs = model(image_tensor)

        probabilities = F.softmax(outputs, dim=1)

        confidence, predicted = torch.max(
            probabilities, dim=1
        )

    return (
        predicted.item(),
        confidence.item(),
        probabilities.squeeze().tolist(),
        processed_image
    )


# -------------------------------
# Main Application
# -------------------------------

try:
    model = load_model()
    st.success("CNN Model loaded successfully!")

except Exception as e:
    st.error(f"Unable to load model: {e}")
    st.stop()


# -------------------------------
# Upload Image
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload a handwritten digit image",
    type=["png", "jpg", "jpeg"]
)


if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Uploaded Image")

    st.image(
        image,
        caption="Original Image",
        width=200
    )

    if st.button("Predict Digit", type="primary"):

        with st.spinner("Predicting digit..."):

            try:

                prediction, confidence, probabilities, processed = (
                    predict_digit(model, image)
                )

                st.divider()

                st.subheader("Prediction Result")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Predicted Digit",
                        prediction
                    )

                with col2:
                    st.metric(
                        "Confidence",
                        f"{confidence * 100:.2f}%"
                    )

                st.subheader("Processed Image (28 × 28)")

                st.image(
                    processed,
                    width=150,
                    clamp=True
                )

                st.subheader("Class Probabilities")

                st.bar_chart({
                    str(i): probabilities[i]
                    for i in range(10)
                })

            except Exception as e:
                st.error(f"Prediction failed: {e}")


else:
    st.info("Please upload a handwritten digit image to get started.")

st.divider()

st.caption(
    "Built using PyTorch, CNN, MNIST and Streamlit."
)
