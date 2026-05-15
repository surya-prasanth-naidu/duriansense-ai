import json
import base64
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from database import save_prediction
from heatmap_utils import generate_gradcam

MODEL_PATH = "best_durian_model.keras"
CLASS_PATH = "class_names.json"
IMG_SIZE = (224, 224)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

@st.cache_resource
def load_ai_model():
    return tf.keras.models.load_model(MODEL_PATH)

def is_leaf_image(image):
    img = image.resize((224, 224))
    arr = np.array(img)

    green_pixels = np.sum(
        (arr[:, :, 1] > arr[:, :, 0]) &
        (arr[:, :, 1] > arr[:, :, 2])
    )

    total_pixels = arr.shape[0] * arr.shape[1]
    green_ratio = green_pixels / total_pixels

    return green_ratio > 0.20

def get_risk_level(predicted_class):
    high_risk_diseases = [
        "anthracnose_disease",
        "thrips_disease",
        "mealybug_infestation"
    ]

    medium_risk_diseases = [
        "sooty_mold",
        "yellow_leaf"
    ]

    if predicted_class in high_risk_diseases:
        return "High"
    elif predicted_class in medium_risk_diseases:
        return "Medium"
    else:
        return "Low"

def farmer_dashboard():
    bg_image = get_base64_image("assets/smartpredictionbck.png")

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(0,0,0,0.55);
        background-blend-mode: darken;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .prediction-card {{
        background: rgba(10, 15, 12, 0.82);
        padding: 28px;
        border-radius: 24px;
        border: 1px solid rgba(184,234,131,0.22);
        box-shadow: 0 0 35px rgba(132,204,22,0.12);
        backdrop-filter: blur(18px);
        margin-bottom: 24px;
    }}
    </style>
    """, unsafe_allow_html=True)

    model = load_ai_model()

    with open(CLASS_PATH, "r") as f:
        class_names = json.load(f)

    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)

    st.header("📸 Smart Prediction System")
    st.write("Upload or capture a durian leaf image to detect possible diseases using AI.")

    input_method = st.radio(
        "Choose input method:",
        ["Upload Image", "Take Photo"],
        horizontal=True
    )

    uploaded_file = None

    if input_method == "Upload Image":
        uploaded_file = st.file_uploader("Choose a durian leaf image", type=["jpg", "jpeg", "png"])
    else:
        uploaded_file = st.camera_input("Take a durian leaf photo")

    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")

        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.image(image, caption="Selected Image", width=550)

        if not is_leaf_image(image):
            st.error("⚠️ Invalid image detected. Please upload a clear durian leaf image only.")
            st.info("Make sure the leaf occupies most of the camera frame.")
            return

        img = image.resize(IMG_SIZE)
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        predicted_index = np.argmax(prediction)
        predicted_class = class_names[predicted_index]
        confidence = float(prediction[0][predicted_index] * 100)

        risk = get_risk_level(predicted_class)

        if confidence < 50:
            st.error("⚠️ AI could not confidently identify the durian leaf disease. Please retake a clearer leaf image.")
            return

        st.subheader("🔍 Prediction Result")
        st.success(f"Disease Name: {predicted_class}")
        st.info(f"Confidence: {confidence:.2f}%")
        st.warning(f"Risk Level: {risk}")

        st.subheader("🔥 Analysis Visualization")

        heatmap_image = generate_gradcam(model, image)

        if heatmap_image is not None:
            col1, col2 = st.columns(2)

            with col1:
                st.write("Original Image")
                st.image(image, width=420)

            with col2:
                st.write("AI Heatmap Focus")
                st.image(heatmap_image, width=420)

            st.info("Red and yellow areas show where the AI model focused most when making the prediction.")
        else:
            st.warning("Heatmap could not be generated for this model.")

        if confidence < 70:
            st.error("⚠️ Prediction not highly confident. Please retake a clearer image.")

        suggestions = {
            "anthracnose_disease": "Apply suitable fungicide, remove infected leaves, and avoid overhead watering.",
            "yellow_leaf": "Check soil nutrients, improve watering schedule, and inspect root health.",
            "thrips_disease": "Use insect control methods such as neem oil or suitable insecticide and monitor new leaves.",
            "sooty_mold": "Clean affected leaves and control sap-sucking insects such as mealybugs or scale insects.",
            "mealybug_infestation": "Apply neem oil or recommended insecticide and remove heavily infested leaves."
        }

        st.subheader("🌿 Treatment & Prevention Suggestion")
        st.write(suggestions.get(predicted_class, "Please consult an agricultural expert for confirmation."))

        save_prediction(
            user_id=st.session_state.user["id"],
            image_name=uploaded_file.name,
            disease_result=predicted_class,
            confidence=round(confidence, 2),
            risk_level=risk
        )

        st.success("Prediction saved to history.")