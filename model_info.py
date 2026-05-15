import streamlit as st

def model_info_page():
    st.markdown("""
    <style>
    .model-hero {
        background: rgba(10, 15, 12, 0.78);
        padding: 30px;
        border-radius: 26px;
        border: 1px solid rgba(184,234,131,0.25);
        box-shadow: 0 0 35px rgba(132,204,22,0.12);
        backdrop-filter: blur(18px);
        margin-bottom: 25px;
    }

    .model-title {
        font-size: 42px;
        font-weight: 900;
        color: white;
        margin-bottom: 8px;
    }

    .model-subtitle {
        color: #e5e7eb;
        font-size: 17px;
        line-height: 1.6;
    }

    .glass-card {
        background: rgba(10, 15, 12, 0.72);
        padding: 24px;
        border-radius: 22px;
        border: 1px solid rgba(184,234,131,0.18);
        box-shadow: 0 0 25px rgba(132,204,22,0.08);
        backdrop-filter: blur(14px);
        margin-bottom: 22px;
    }

    .section-title {
        color: #b8ea83;
        font-size: 24px;
        font-weight: 900;
        margin-bottom: 15px;
    }

    .step-box {
        padding: 14px 16px;
        margin-bottom: 10px;
        border-radius: 15px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.10);
        color: #f8fafc;
        font-weight: 600;
    }

    .disease-pill {
        display: inline-block;
        padding: 10px 16px;
        margin: 6px;
        border-radius: 999px;
        background: rgba(184,234,131,0.16);
        border: 1px solid rgba(184,234,131,0.28);
        color: #f8fafc;
        font-weight: 700;
    }

    .warning-box {
        background: rgba(255,193,7,0.12);
        border: 1px solid rgba(255,193,7,0.28);
        padding: 18px;
        border-radius: 18px;
        color: #fff7ed;
        margin-bottom: 14px;
    }

    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.76);
        padding: 22px;
        border-radius: 20px;
        border: 1px solid rgba(184,234,131,0.18);
        box-shadow: 0 0 20px rgba(132,204,22,0.08);
    }

    [data-testid="stMetricValue"] {
        color: #b8ea83;
        font-weight: 900;
    }
    </style>
    """, unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)
    col1.metric("Model Architecture", "EfficientNetB0")
    col2.metric("Test Accuracy", "87%")
    col3.metric("Supported Classes", "5")

    st.markdown("""
    <div class="glass-card">
        <div class="section-title">🌿 Supported Disease Classes</div>
        <span class="disease-pill">Anthracnose Disease</span>
        <span class="disease-pill">Yellow Leaf</span>
        <span class="disease-pill">Thrips Disease</span>
        <span class="disease-pill">Sooty Mold</span>
        <span class="disease-pill">Mealybug Infestation</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><div class="section-title">🧠 How the AI Prediction Works</div>', unsafe_allow_html=True)

    steps = [
        "User uploads or captures a durian leaf image.",
        "The system checks whether the image appears to contain leaf-like content.",
        "The image is resized to 224 × 224 pixels.",
        "EfficientNetB0 extracts important visual patterns from the image.",
        "The model predicts the most likely disease class.",
        "The system displays disease name, confidence percentage, risk level, and treatment suggestion."
    ]

    for i, step in enumerate(steps, start=1):
        st.markdown(f'<div class="step-box">{i}. {step}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div class="section-title">🛡️ Confidence Safety System</div>
        <div class="step-box">✅ Above 80%: High confidence prediction</div>
        <div class="step-box">⚠️ 60% to 79%: Moderate confidence prediction</div>
        <div class="step-box">🔁 Below 70%: User is advised to retake a clearer image</div>
        <div class="step-box">⛔ Below 50%: Prediction is rejected as unreliable</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div class="section-title">📷 Recommended Image Capture Guidelines</div>
        <div class="step-box">Capture one clear durian leaf at a time.</div>
        <div class="step-box">Make sure the leaf fills most of the image.</div>
        <div class="step-box">Use good lighting and avoid strong shadows.</div>
        <div class="step-box">Avoid blurry photos.</div>
        <div class="step-box">Avoid including faces, hands, soil, or background objects.</div>
    </div>
    """, unsafe_allow_html=True)