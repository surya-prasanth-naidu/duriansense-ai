import streamlit as st

DISEASE_KNOWLEDGE = {
    "anthracnose": {
        "name": "Anthracnose Disease",
        "type": "Fungal disease",
        "keywords": ["anthracnose", "dark spot", "brown spot", "black spot", "yellow halo", "lesion"],
        "cause": "Anthracnose is commonly caused by Colletotrichum fungal species.",
        "why": "It develops easily during rainy, humid conditions, especially when leaves remain wet for long periods.",
        "symptoms": "Dark brown or black spots, irregular lesions, dry patches, and sometimes yellow halos around infected areas.",
        "impact": "It can reduce photosynthesis, weaken leaf health, cause early leaf drop, and reduce overall tree productivity.",
        "natural": "Remove infected leaves, prune for better airflow, avoid overhead watering, and clear fallen diseased leaves.",
        "chemical": "Use a suitable fungicide such as mancozeb or copper-based fungicide if infection is spreading.",
        "fertilizer": "Use balanced NPK. Avoid too much nitrogen because soft new growth is more disease-prone.",
        "prevention": "Improve drainage, prune regularly, remove infected debris, and monitor after rainy periods.",
        "spread": "It can spread through rain splash, contaminated pruning tools, infected leaves, and poor orchard sanitation.",
        "next_action": "Remove infected leaves first, improve airflow, then monitor nearby leaves for 3–5 days."
    },

    "mealybug": {
        "name": "Mealybug Infestation",
        "type": "Pest infestation",
        "keywords": ["mealybug", "mealy bug", "white cotton", "cotton", "sticky", "white insect", "ants"],
        "cause": "Mealybugs are sap-sucking insects that feed on plant fluids.",
        "why": "They increase in warm, humid conditions and often spread faster when ants protect them.",
        "symptoms": "White cotton-like clusters, sticky residue, leaf curling, weak shoots, and sometimes black mold nearby.",
        "impact": "They weaken the plant by sucking sap and can lead to sooty mold because of honeydew secretion.",
        "natural": "Remove visible insects, prune heavy infestation, control ants, and apply neem oil carefully.",
        "chemical": "Use suitable insecticide such as imidacloprid only if infestation is severe and spreading.",
        "fertilizer": "Avoid excess nitrogen. Maintain balanced nutrition to prevent very soft pest-attracting growth.",
        "prevention": "Check leaf undersides weekly, control ants, and treat early before infestation spreads.",
        "spread": "Mealybugs can spread through ants, wind, movement of infected plant material, and close contact between plants.",
        "next_action": "Check the underside of leaves and nearby shoots. If white clusters are present, isolate and treat early."
    },

    "sooty": {
        "name": "Sooty Mold",
        "type": "Secondary fungal growth",
        "keywords": ["sooty", "mold", "mould", "black powder", "black coating", "black layer", "soot"],
        "cause": "Sooty mold grows on honeydew produced by insects such as mealybugs, aphids, or scale insects.",
        "why": "It appears when sap-sucking pests are not controlled and sticky honeydew remains on leaves.",
        "symptoms": "Black powdery or soot-like coating on the leaf surface.",
        "impact": "It blocks sunlight, reduces photosynthesis, and weakens the leaf if severe.",
        "natural": "Control insects first, gently clean affected leaves, prune dense canopy, and improve airflow.",
        "chemical": "A mild fungicide may help, but pest control is more important because mold returns if insects remain.",
        "fertilizer": "Support plant health with balanced nutrients and avoid stress from poor watering.",
        "prevention": "Monitor for mealybugs, aphids, and scale insects. Control pests early.",
        "spread": "It can spread through fungal spores, but the main cause is honeydew from insects.",
        "next_action": "Look for insects under the leaves. Treat the pest source first before focusing on the black mold."
    },

    "yellow": {
        "name": "Yellow Leaf",
        "type": "Nutrient disorder / plant stress symptom",
        "keywords": ["yellow", "yellowing", "pale", "chlorosis", "nutrient", "magnesium", "iron"],
        "cause": "Yellow leaf is often caused by nutrient deficiency, root stress, poor soil condition, or water imbalance.",
        "why": "It happens when the tree cannot absorb nutrients properly due to poor soil fertility, waterlogging, drought, or weak roots.",
        "symptoms": "Leaves become yellow or pale green. Growth may also look weak or slow.",
        "impact": "Yellowing reduces photosynthesis and may indicate poor soil, poor root health, or nutrient imbalance.",
        "natural": "Improve soil organic matter, correct watering, and ensure good drainage.",
        "chemical": "Pesticide is usually not needed unless another disease or pest is confirmed.",
        "fertilizer": "Use balanced NPK. Magnesium or iron support may help if deficiency symptoms match.",
        "prevention": "Maintain soil fertility, avoid waterlogging, and follow a consistent fertilization plan.",
        "spread": "Yellow leaf is usually not infectious and does not spread like fungal diseases. However, the same soil or watering issue can affect many trees.",
        "next_action": "Check watering and soil condition first. If many leaves are yellow, consider soil testing."
    },

    "thrips": {
        "name": "Thrips Damage",
        "type": "Pest damage",
        "keywords": ["thrips", "thrip", "silver", "silvery", "streak", "scar", "distorted", "tiny insect"],
        "cause": "Thrips are tiny insects that scrape and suck plant tissue, especially on young leaves.",
        "why": "They often increase during dry and warm conditions and attack young leaf flushes.",
        "symptoms": "Silvery streaks, scarring, distorted young leaves, rough surface, and small black specks.",
        "impact": "Thrips can damage young leaves, reduce leaf quality, and affect healthy canopy growth.",
        "natural": "Use neem oil, remove heavily damaged leaves, monitor young shoots, and encourage natural predators.",
        "chemical": "Spinosad or another suitable insecticide may be used if infestation is severe.",
        "fertilizer": "Use balanced nutrients and avoid excessive nitrogen because soft flushes attract pests.",
        "prevention": "Monitor young shoots frequently and control early before pest numbers increase.",
        "spread": "Thrips can spread by wind, movement between plants, and movement of infested plant material.",
        "next_action": "Inspect young leaves closely. If silver streaks and tiny insects are seen, start early pest control."
    }
}

GENERAL_OVERVIEW = """
### 🌿 Common Durian Leaf Problems

Durian leaves can be affected by several disease, pest, and nutrient-related problems:

1. **Anthracnose Disease**  
   A fungal disease that causes dark spots, lesions, and yellow halos.

2. **Mealybug Infestation**  
   A pest issue where white cotton-like insects suck sap from leaves and shoots.

3. **Sooty Mold**  
   A black fungal coating that usually grows because insects produce sticky honeydew.

4. **Yellow Leaf**  
   Usually related to nutrient deficiency, poor soil, water stress, or root problems.

5. **Thrips Damage**  
   A pest problem that causes silvery streaks, scars, and distorted young leaves.

You can ask:
- What is mealybug?
- What causes anthracnose?
- How to treat sooty mold naturally?
- What fertilizer helps yellow leaf?
- How do thrips spread?
"""

def detect_disease(question):
    q = question.lower()
    best_key = None
    best_score = 0

    for key, data in DISEASE_KNOWLEDGE.items():
        score = 0
        for word in data["keywords"]:
            if word in q:
                score += 1

        if score > best_score:
            best_score = score
            best_key = key

    return best_key

def detect_intent(question):
    q = question.lower()

    if any(w in q for w in ["what is", "explain", "tell me about", "describe", "information about", "meaning of"]):
        return "full"

    if any(w in q for w in ["cause", "why", "happen", "reason"]):
        return "cause"

    if any(w in q for w in ["symptom", "look", "sign", "identify", "detect"]):
        return "symptoms"

    if any(w in q for w in ["natural", "organic", "home remedy", "without chemical"]):
        return "natural"

    if any(w in q for w in ["chemical", "fungicide", "insecticide", "spray", "medicine"]):
        return "chemical"

    if any(w in q for w in ["fertilizer", "fertiliser", "nutrient", "npk", "magnesium", "iron"]):
        return "fertilizer"

    if any(w in q for w in ["prevent", "avoid", "stop", "control"]):
        return "prevention"

    if any(w in q for w in ["spread", "infect", "transfer"]):
        return "spread"

    if any(w in q for w in ["impact", "effect", "damage", "danger"]):
        return "impact"

    if any(w in q for w in ["next", "what should i do", "action", "recommend"]):
        return "next_action"

    if any(w in q for w in ["disease", "problem", "durian leaf", "types"]):
        return "overview"

    return "full"

def format_response(key, intent):
    d = DISEASE_KNOWLEDGE[key]

    if intent == "cause":
        return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}** affecting durian leaves.

**Cause:**  
{d['cause']}

**Why it happens:**  
{d['why']}

**Recommended next action:**  
{d['next_action']}
"""

    if intent == "symptoms":
        return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}**.

**Visual symptoms:**  
{d['symptoms']}

**Tip:**  
Check both the upper and lower leaf surfaces because some pests hide underneath leaves.
"""

    if intent == "natural":
        return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}**.

**Natural / cultural control:**  
{d['natural']}

**How to stop it spreading:**  
{d['prevention']}

**Recommended next action:**  
{d['next_action']}
"""

    if intent == "chemical":
        return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}**.

**Chemical control:**  
{d['chemical']}

**How to stop it spreading:**  
{d['prevention']}

⚠️ **Safety note:**  
Always follow local label registration, dosage, pre-harvest interval, PPE, and agricultural officer advice.
"""

    if intent == "fertilizer":
        return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}**.

**Fertilizer support:**  
{d['fertilizer']}

**Important note:**  
Fertilizer supports recovery, but it does not replace proper disease or pest control.
"""

    if intent == "prevention":
        return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}**.

**How it spreads:**  
{d['spread']}

**Prevention / how to stop spreading:**  
{d['prevention']}

**Recommended next action:**  
{d['next_action']}
"""

    if intent == "spread":
        return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}**.

**How it spreads:**  
{d['spread']}

**How to stop it spreading:**  
{d['prevention']}

**Recommended next action:**  
{d['next_action']}
"""

    if intent == "impact":
        return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}**.

**Impact on tree:**  
{d['impact']}

**Recommended next action:**  
{d['next_action']}
"""

    if intent == "next_action":
        return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}**.

**Recommended next action:**  
{d['next_action']}

**Natural control:**  
{d['natural']}

**Chemical control:**  
{d['chemical']}

If symptoms spread quickly or the tree looks weak, contact an agricultural officer.
"""

    return f"""
### {d['name']}

**What it is:**  
{d['name']} is a **{d['type']}** affecting durian plant health.

**Cause:**  
{d['cause']}

**Why it happens:**  
{d['why']}

**Visual symptoms:**  
{d['symptoms']}

**Impact on tree:**  
{d['impact']}

**How it spreads:**  
{d['spread']}

**Natural / cultural control:**  
{d['natural']}

**Chemical control:**  
{d['chemical']}

**Fertilizer support:**  
{d['fertilizer']}

**How to stop it spreading / prevention:**  
{d['prevention']}

**Recommended next action:**  
{d['next_action']}

⚠️ **Safety note:**  
Chemical usage must follow local agricultural label instructions, PPE requirements, correct dosage, and expert advice.
"""

def quick_answer_buttons():
    st.write("### Quick Disease Guide")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Anthracnose"):
            st.session_state.chatbot_question = "What is anthracnose disease?"
        if st.button("Mealybug"):
            st.session_state.chatbot_question = "What is mealybug infestation?"

    with col2:
        if st.button("Sooty Mold"):
            st.session_state.chatbot_question = "What is sooty mold?"
        if st.button("Yellow Leaf"):
            st.session_state.chatbot_question = "What is yellow leaf?"

    with col3:
        if st.button("Thrips"):
            st.session_state.chatbot_question = "What is thrips damage?"
        if st.button("General Durian Leaf Problems"):
            st.session_state.chatbot_question = "What diseases in a durian plant leaf?"

def chatbot_page():
    st.header("🤖 AI Chatbot Assistant")
    st.write("Ask about durian leaf diseases, symptoms, causes, treatment, prevention, fertilizer support, or pest control.")

    st.info(
        "Examples: 'What is mealybug?', 'white cotton on leaf', 'black powder on leaf', "
        "'what fertilizer for yellow leaf?', 'how to treat thrips naturally?'"
    )

    if "chatbot_question" not in st.session_state:
        st.session_state.chatbot_question = ""

    quick_answer_buttons()

    user_question = st.text_input(
        "Ask your question:",
        value=st.session_state.chatbot_question
    )

    if st.button("Ask Chatbot"):
        if not user_question.strip():
            st.warning("Please type a question first.")
            return

        disease_key = detect_disease(user_question)
        intent = detect_intent(user_question)

        if intent == "overview" and disease_key is None:
            st.markdown(GENERAL_OVERVIEW)
            return

        if disease_key:
            response = format_response(disease_key, intent)
            st.markdown(response)
        else:
            st.markdown(GENERAL_OVERVIEW)
            st.warning(
                "I could not identify a specific disease from your question. "
                "Try describing the symptom, such as 'white cotton', 'black powder', "
                "'yellow leaf', 'silver streaks', or 'dark spots'."
            )