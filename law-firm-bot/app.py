import streamlit as st
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Law & Energy AI",
    page_icon="⚖️",
    layout="wide"
)

# --- 2. ESTILOS (TEMA NAVY BLUE) ---
st.markdown("""
<style>
    /* Títulos en Azul Navy */
    h1, h2, h3 { color: #002B5C !important; }
    
    /* Barra lateral estilo profesional */
    section[data-testid="stSidebar"] {
        background-color: #f5f5f5;
        border-right: 2px solid #002B5C;
    }

    /* Borde del chat input */
    .stChatInput { border-color: #002B5C !important; }

    /* Línea superior decorativa */
    header { border-bottom: 2px solid #002B5C; }
</style>
""", unsafe_allow_html=True)

# --- 3. BARRA LATERAL (SIDEBAR) BILINGÜE ---
# Ruta del logo (asegúrese de que la carpeta law-firm-bot existe en GitHub)
logo_path = "law-firm-bot/logo.png"

with st.sidebar:
    # Intentar cargar el logo
    try:
        st.image(logo_path, use_container_width=True)
    except:
        st.header("Law & Energy")
        st.caption("Consultants, LLC")
    
    st.markdown("---")
    
    # Selector de Idioma
    st.header("Idioma / Language")
    selected_lang = st.radio("Seleccione / Select:", ["Español", "English"])
    
    st.markdown("---")
    
    # LÓGICA DE TRADUCCIÓN PARA LA BARRA LATERAL
    if selected_lang == "Español":
        st.caption("📍 **Ubicación:**")
        st.markdown("1913 Ave. Las Americas,\nSan Antonio, Ponce, PR")
        
        st.caption("📧 **Correo Electrónico:**")
        st.markdown("vera@lawenergyconsultants.com")
        
        st.caption("🕒 **Horario Operacional:**")
        st.markdown("Lunes a Viernes:\n9:00 am – 6:00 pm\n*(Cita previa / Zoom)*")
        
    else: # English Version
        st.caption("📍 **Location:**")
        st.markdown("1913 Ave. Las Americas,\nSan Antonio, Ponce, PR")
        
        st.caption("📧 **Email Address:**")
        st.markdown("vera@lawenergyconsultants.com")
        
        st.caption("🕒 **Business Hours:**")
        st.markdown("Monday to Friday:\n9:00 am – 6:00 pm\n*(By appointment / Zoom)*")

# --- 4. BASE DE CONOCIMIENTO (DICCIONARIO BILINGÜE) ---
content = {
    "English": {
        "title": "Law & Energy Consultants",
        "subtitle": "AI Digital Assistant",
        "welcome": "Ask about: **Net Metering**, **Solar Design**, **Location**, or **Legal Representation**.",
        "placeholder": "How can we help with your energy project?",
        "thinking": "Consulting firm database...",
        "responses": {
            "permits": "We specialize in permitting with **LUMA Energy** to obtain net metering certifications. We can also assist with endorsements from the OGPe and other regulatory bodies.",
            "renewable": "Our team offers engineering design for **renewable energy systems** (both battery-backed and grid-tied). We can handle the full technical and legal design for residential or commercial projects.",
            "electrical": "We provide design services for **electrical substations**, transmission lines, and distribution lines. Do you need assistance with a specific voltage level?",
            "legal": "As a firm specializing in **Energy Law**, we represent clients in administrative forums and courts. We also handle civil litigation, contracts, and property law.",
            "contact": (
                "You can find us at **1913 Ave. Las Americas, San Antonio, Ponce, PR**. "
                "Our hours are Mon-Fri 9am-6pm (by appointment/Zoom). "
                "Please email **vera@lawenergyconsultants.com** to schedule."
            ),
            "fallback": "I understand your inquiry. As an AI assistant, I provide general info on Engineering & Law. For specific legal advice, please contact our office directly."
        }
    },
    "Español": {
        "title": "Law & Energy Consultants",
        "subtitle": "Asistente Digital IA",
        "welcome": "Pregunte sobre: **Medición Neta**, **Diseño Solar**, **Ubicación**, o **Representación Legal**.",
        "placeholder": "¿En qué podemos ayudarle con su proyecto energético?",
        "thinking": "Consultando base de datos...",
        "responses": {
            "permits": "Nos especializamos en la permisología con **LUMA Energy** para certificaciones de medición neta. También asistimos con endosos de la **OGPe** y otros entes reguladores.",
            "renewable": "Nuestro equipo ofrece diseño de ingeniería para **sistemas de energía renovable** (con baterías o conectados a la red). Manejamos el diseño técnico y legal para proyectos residenciales o comerciales.",
            "electrical": "Proveemos servicios de diseño para **subestaciones eléctricas**, líneas de transmisión y distribución. ¿Necesita asistencia con algún voltaje específico?",
            "legal": "Como firma especializada en **Derecho Energético**, representamos a clientes en foros administrativos y tribunales. También manejamos litigios civiles, contratos y leyes de propiedad.",
            "contact": (
                "Estamos ubicados en **1913 Ave. Las Americas, San Antonio, Ponce, PR**. "
                "Nuestro horario es **Lunes a Viernes de 9:00 am – 6:00 pm** (por cita previa o Zoom). "
                "Puede escribir a **vera@lawenergyconsultants.com** para coordinar."
            ),
            "fallback": "Entiendo su consulta. Como asistente de IA, ofrezco información general sobre nuestros servicios. Para asesoría legal específica, por favor contacte nuestra oficina."
        }
    }
}

# --- 5. MOTOR LÓGICO (KEYWORD MATCHING) ---
def get_bot_response(user_input, lang_code):
    user_input = user_input.lower()
    resp = content[lang_code]["responses"]
    
    # Lógica Español
    if lang_code == "Español":
        if any(x in user_input for x in ["luma", "permiso", "medición neta", "ogpe", "endoso"]): return resp["permits"]
        elif any(x in user_input for x in ["solar", "renovable", "bateria", "batería", "placa"]): return resp["renewable"]
        elif any(x in user_input for x in ["subestacion", "transmision", "diseño", "voltaje", "ingenieria"]): return resp["electrical"]
        elif any(x in user_input for x in ["ley", "legal", "tribunal", "derecho", "corte", "caso", "demanda"]): return resp["legal"]
        elif any(x in user_input for x in ["cita", "correo", "email", "donde", "ubicacion", "ubicación", "horario", "hora", "abierto", "direccion", "ponce"]): return resp["contact"]
        else: return resp["fallback"]
        
    # Lógica English
    else:
        if any(x in user_input for x in ["luma", "permit", "net metering", "ogpe"]): return resp["permits"]
        elif any(x in user_input for x in ["solar", "renewable", "battery", "panel"]): return resp["renewable"]
        elif any(x in user_input for x in ["substation", "transmission", "design", "engineering"]): return resp["electrical"]
        elif any(x in user_input for x in ["law", "legal", "court", "litigation", "case"]): return resp["legal"]
        elif any(x in user_input for x in ["appointment", "email", "where", "location", "address", "hours", "open", "schedule", "ponce"]): return resp["contact"]
        else: return resp["fallback"]

# --- 6. INTERFAZ PRINCIPAL ---
current_text = content[selected_lang]

st.title(current_text["title"])
st.subheader(current_text["subtitle"])
st.markdown(current_text["welcome"])

# Mostrar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input(current_text["placeholder"]):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with st.spinner(current_text["thinking"]):
            time.sleep(0.5)
            assistant_response = get_bot_response(prompt, selected_lang)

        # Efecto de escritura
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})






