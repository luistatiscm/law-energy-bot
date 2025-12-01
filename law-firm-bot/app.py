import streamlit as st
import time

# --- 1. CONFIGURATION & TRANSLATIONS ---
# Configure the page and adding the Logo
st.set_page_config(page_title="Law & Energy AI", page_icon="⚖️")

# --- LOGO SETUP ---
# We use the direct link to their website logo so you don't have to upload a file
logo_url = "https://lawenergyconsultants.com/wp-content/uploads/2019/12/logo-law-energy-consultants-header-retina.png"

# This puts the logo at the top of the Sidebar (big and visible)
st.sidebar.image(logo_url, use_container_width=True)

content = {
    "English": {
        "title": "Law & Energy Consultants",
        "subtitle": "AI Digital Assistant",
        "welcome": "Ask about: **LUMA Permitting**, **Solar Design**, **Substations**, or **Legal Representation**.",
        "placeholder": "How can we help with your energy project?",
        "thinking": "Consulting firm database...",
        "responses": {
            "permits": (
                "We specialize in permitting with **LUMA Energy** to obtain net metering "
                "certifications. We can also assist with endorsements from the OGPe "
                "and other regulatory bodies."
            ),
            "renewable": (
                "Our team offers engineering design for **renewable energy systems** "
                "(both battery-backed and grid-tied). We can handle the full technical "
                "and legal design for residential or commercial projects."
            ),
            "electrical": (
                "We provide design services for **electrical substations**, transmission lines, "
                "and distribution lines. Do you need assistance with a specific voltage level?"
            ),
            "legal": (
                "As a firm specializing in **Energy Law**, we represent "
                "clients in administrative forums and courts. We also handle civil litigation, "
                "contracts, and property law."
            ),
            "contact": (
                "You can reach us at **(787) 354-5033**. "
                "Would you like to schedule a consultation regarding a specific project?"
            ),
            "fallback": (
                "I understand you have an inquiry. As an AI assistant, I can help with general "
                "information about our Engineering and Legal services. For specific advice, "
                "please contact our office directly."
            )
        }
    },
    "Español": {
        "title": "Law & Energy Consultants",
        "subtitle": "Asistente Digital IA",
        "welcome": "Pregunte sobre: **Permisos LUMA**, **Diseño Solar**, **Subestaciones**, o **Representación Legal**.",
        "placeholder": "¿En qué podemos ayudarle con su proyecto energético?",
        "thinking": "Consultando base de datos...",
        "responses": {
            "permits": (
                "Nos especializamos en la permisología con **LUMA Energy** para certificaciones "
                "de medición neta. También asistimos con endosos de la **OGPe** "
                "y otros entes reguladores."
            ),
            "renewable": (
                "Nuestro equipo ofrece diseño de ingeniería para **sistemas de energía renovable** "
                "(con baterías o conectados a la red). Manejamos el diseño técnico "
                "y legal para proyectos residenciales o comerciales."
            ),
            "electrical": (
                "Proveemos servicios de diseño para **subestaciones eléctricas**, líneas de transmisión "
                "y distribución. ¿Necesita asistencia con algún voltaje específico?"
            ),
            "legal": (
                "Como firma especializada en **Derecho Energético**, representamos a clientes "
                "en foros administrativos y tribunales. También manejamos litigios civiles, "
                "contratos y leyes de propiedad."
            ),
            "contact": (
                "Puede contactarnos al **(787) 354-5033**. "
                "¿Le gustaría coordinar una consulta sobre un proyecto específico?"
            ),
            "fallback": (
                "Entiendo su consulta. Como asistente de IA, puedo ayudarle con información "
                "general sobre nuestros servicios de Ingeniería y Leyes. Para asesoría legal específica, "
                "por favor contacte nuestra oficina."
            )
        }
    }
}

# --- 2. LOGIC ---
def get_bot_response(user_input, lang_code):
    """Checks keywords in the user's language and returns the correct response."""
    user_input = user_input.lower()
    resp = content[lang_code]["responses"]
    
    # Spanish Keywords
    if lang_code == "Español":
        if any(x in user_input for x in ["luma", "permiso", "medición neta", "ogpe"]):
            return resp["permits"]
        elif any(x in user_input for x in ["solar", "renovable", "bateria", "batería"]):
            return resp["renewable"]
        elif any(x in user_input for x in ["subestacion", "transmision", "diseño", "voltaje"]):
            return resp["electrical"]
        elif any(x in user_input for x in ["ley", "legal", "tribunal", "derecho", "corte"]):
            return resp["legal"]
        elif any(x in user_input for x in ["cita", "telefono", "teléfono", "llamar", "contacto"]):
            return resp["contact"]
        else:
            return resp["fallback"]
            
    # English Keywords
    else:
        if any(x in user_input for x in ["luma", "permit", "net metering", "ogpe"]):
            return resp["permits"]
        elif any(x in user_input for x in ["solar", "renewable", "battery"]):
            return resp["renewable"]
        elif any(x in user_input for x in ["substation", "transmission", "design"]):
            return resp["electrical"]
        elif any(x in user_input for x in ["law", "legal", "court", "litigation"]):
            return resp["legal"]
        elif any(x in user_input for x in ["appointment", "schedule", "call", "contact"]):
            return resp["contact"]
        else:
            return resp["fallback"]

# --- 3. UI SETUP ---

# Custom CSS to force the firm's branding on the headers
st.markdown("""
<style>
    /* Change the title color to Navy Blue */
    h1 {
        color: #002B5C;
        font-family: 'Helvetica', sans-serif;
    }
    /* Style the chat input box */
    .stChatInput {
        border-color: #002B5C;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for Language Selection
with st.sidebar:
    st.header("Language / Idioma")
    selected_lang = st.radio("Select:", ["English", "Español"])
    
    st.markdown("---")
    st.markdown(f"**{content['English']['title']}**")
    st.caption("San Juan, Puerto Rico")

# Load text based on selection
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



