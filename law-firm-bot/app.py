import streamlit as st
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Law & Energy AI",
    page_icon="⚖️",
    layout="wide"
)

# --- 2. FORCE THEME & LOGO (CSS INJECTION) ---
# This forces the Navy Blue theme and handles the logo sizing
st.markdown("""
<style>
    /* Force the main headers to Navy Blue */
    h1, h2, h3 {
        color: #002B5C !important;
    }
    
    /* Style the sidebar to match the firm's professional look */
    section[data-testid="stSidebar"] {
        background-color: #f5f5f5;
        border-right: 2px solid #002B5C;
    }

    /* Change the chat input border to Navy Blue */
    .stChatInput {
        border-color: #002B5C !important;
    }

    /* Add a professional border to the top */
    header {
        border-bottom: 2px solid #002B5C;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGO SETUP ---
# We use the uploaded file instead of the URL
logo_path = "logo.png"

# Display Logo in Sidebar
with st.sidebar:
    try:
        st.image(logo_path, use_container_width=True)
    except:
        st.error("Logo not found. Please upload logo.png to GitHub.")

# Display Logo in Sidebar
with st.sidebar:
    try:
        st.image(logo_url, use_container_width=True)
    except:
        # Fallback if the image link breaks
        st.header("Law & Energy")
        st.caption("Consultants, LLC")
    
    st.markdown("---")
    
    # Language Selector
    st.header("Language / Idioma")
    selected_lang = st.radio("Select:", ["English", "Español"])
    
    st.markdown("---")
    st.caption("📍 San Juan, Puerto Rico")
    st.caption("📞 (787) 354-5033")

# --- 4. KNOWLEDGE BASE & TRANSLATIONS ---
content = {
    "English": {
        "title": "Law & Energy Consultants",
        "subtitle": "AI Digital Assistant",
        "welcome": "Ask about: **LUMA Permitting**, **Solar Design**, **Substations**, or **Legal Representation**.",
        "placeholder": "How can we help with your energy project?",
        "thinking": "Consulting firm database...",
        "responses": {
            "permits": "We specialize in permitting with **LUMA Energy** to obtain net metering certifications. We can also assist with endorsements from the OGPe and other regulatory bodies.",
            "renewable": "Our team offers engineering design for **renewable energy systems** (both battery-backed and grid-tied). We can handle the full technical and legal design for residential or commercial projects.",
            "electrical": "We provide design services for **electrical substations**, transmission lines, and distribution lines. Do you need assistance with a specific voltage level?",
            "legal": "As a firm specializing in **Energy Law**, we represent clients in administrative forums and courts. We also handle civil litigation, contracts, and property law.",
            "contact": "You can reach us at **(787) 354-5033**. Would you like to schedule a consultation regarding a specific project?",
            "fallback": "I understand you have an inquiry. As an AI assistant, I can help with general information about our Engineering and Legal services. For specific advice, please contact our office directly."
        }
    },
    "Español": {
        "title": "Law & Energy Consultants",
        "subtitle": "Asistente Digital IA",
        "welcome": "Pregunte sobre: **Permisos LUMA**, **Diseño Solar**, **Subestaciones**, o **Representación Legal**.",
        "placeholder": "¿En qué podemos ayudarle con su proyecto energético?",
        "thinking": "Consultando base de datos...",
        "responses": {
            "permits": "Nos especializamos en la permisología con **LUMA Energy** para certificaciones de medición neta. También asistimos con endosos de la **OGPe** y otros entes reguladores.",
            "renewable": "Nuestro equipo ofrece diseño de ingeniería para **sistemas de energía renovable** (con baterías o conectados a la red). Manejamos el diseño técnico y legal para proyectos residenciales o comerciales.",
            "electrical": "Proveemos servicios de diseño para **subestaciones eléctricas**, líneas de transmisión y distribución. ¿Necesita asistencia con algún voltaje específico?",
            "legal": "Como firma especializada en **Derecho Energético**, representamos a clientes en foros administrativos y tribunales. También manejamos litigios civiles, contratos y leyes de propiedad.",
            "contact": "Puede contactarnos al **(787) 354-5033**. ¿Le gustaría coordinar una consulta sobre un proyecto específico?",
            "fallback": "Entiendo su consulta. Como asistente de IA, puedo ayudarle con información general sobre nuestros servicios de Ingeniería y Leyes. Para asesoría legal específica, por favor contacte nuestra oficina."
        }
    }
}

# --- 5. LOGIC ENGINE ---
def get_bot_response(user_input, lang_code):
    user_input = user_input.lower()
    resp = content[lang_code]["responses"]
    
    # Spanish Logic
    if lang_code == "Español":
        if any(x in user_input for x in ["luma", "permiso", "medición neta", "ogpe"]): return resp["permits"]
        elif any(x in user_input for x in ["solar", "renovable", "bateria", "batería"]): return resp["renewable"]
        elif any(x in user_input for x in ["subestacion", "transmision", "diseño", "voltaje"]): return resp["electrical"]
        elif any(x in user_input for x in ["ley", "legal", "tribunal", "derecho", "corte"]): return resp["legal"]
        elif any(x in user_input for x in ["cita", "telefono", "teléfono", "llamar", "contacto"]): return resp["contact"]
        else: return resp["fallback"]
    # English Logic
    else:
        if any(x in user_input for x in ["luma", "permit", "net metering", "ogpe"]): return resp["permits"]
        elif any(x in user_input for x in ["solar", "renewable", "battery"]): return resp["renewable"]
        elif any(x in user_input for x in ["substation", "transmission", "design"]): return resp["electrical"]
        elif any(x in user_input for x in ["law", "legal", "court", "litigation"]): return resp["legal"]
        elif any(x in user_input for x in ["appointment", "schedule", "call", "contact"]): return resp["contact"]
        else: return resp["fallback"]

# --- 6. USER INTERFACE ---
current_text = content[selected_lang]

st.title(current_text["title"])
st.subheader(current_text["subtitle"])
st.markdown(current_text["welcome"])

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input(current_text["placeholder"]):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with st.spinner(current_text["thinking"]):
            time.sleep(0.7)
            assistant_response = get_bot_response(prompt, selected_lang)

        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})




