import streamlit as st
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import io
import base64

# Configurazione Pagina
st.set_page_config(page_title="Generatore Barcode Logistics", page_icon="🚚", layout="centered")

# --- CSS PULITO E DEFINITIVO (SINGOLA COLONNA ORDINATA E STAT77) ---
st.markdown("""
    <style>
    /* Stile testi informativi a schermo */
    .info-line {
        font-size: 13px !important;
        color: #d1d5db !important;
        margin-bottom: 2px !important;
    }
    
    /* Nascosto a schermo normale, visibile solo in stampa */
    .print-header-stat77 {
        display: none;
    }

    @media print {
        /* Nasconde elementi superflui dell'interfaccia in stampa */
        [data-testid="stSidebar"], [data-testid="stHeader"], header, footer, 
        .stButton, .stRadio, .stTextInput, .stAlert, button {
            display: none !important;
        }
        body, .stApp {
            background: white !important;
            color: black !important;
            margin: 0 !important;
            padding: 2mm !important;
        }
        div[data-testid="stVerticalBlock"] {
            gap: 0px !important;
        }
        
        /* Barcode STAT77 in cima alla stampa sotto il titolo */
        .print-header-stat77 {
            display: block !important;
            width: 100% !important;
            text-align: center !important;
            margin-top: 5px !important;
            margin-bottom: 12px !important;
            padding-bottom: 5px !important;
            border-bottom: 2px solid #000 !important;
            page-break-after: avoid !important;
            break-after: avoid !important;
        }

        /* Card singole pulite, ordinate e racchiuse in un box */
        .print-card {
            page-break-inside: avoid;
            break-inside: avoid;
            margin-bottom: 6px !important;
            padding: 6px !important;
            border: 1px solid #bbb !important;
            border-radius: 4px !important;
            background: white !important;
            width: 100% !important;
        }
        .info-line {
            color: #000 !important;
            font-size: 13px !important;
        }
        code {
            background: none !important;
            color: #000 !important;
            border: none !important;
            padding: 0 !important;
            font-weight: bold !important;
        }
        /* Barcode stampabile ingrandito del 20% */
        img {
            max-height: 46px !important;
            max-width: 100% !important;
            width: auto !important;
            margin-top: 2px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DI ACCESSO CON PIN / PASSWORD ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🔒 Accesso Riservato</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Inserisci la password di accesso:</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            pwd = st.text_input("Password", type="password", key="login_pin_input", label_visibility="collapsed", placeholder="Inserisci password...")
            
            if st.button("Accedi", use_container_width=True):
                correct_pwd = st.secrets["password"] if "password" in st.secrets else "Wilson"
                
                if pwd.strip() == str(correct_pwd).strip():
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Password errata!")
        return False
    return True

if check_password():

    # --- FUNZIONE GENERAZIONE BARCODE ---
    def generate_barcode_base64(value):
        if not value or str(value).strip() == "" or str(value).strip().lower() == "nan" or str(value).strip() == "none":
            return None
        try:
            CODE128 = barcode.get_barcode_class('code128')
            rv = io.BytesIO()
            val_str = str(value).split('.')[0].strip()
            code = CODE128(val_str, writer=ImageWriter())
            code.write(rv, options={"module_height": 7.0, "module_width": 0.4, "font_size": 4, "text_distance": 1.5, "quiet_zone": 1.0})
            return base64.b64encode(rv.getvalue()).decode("utf-8")
        except Exception as e:
            return None

    # --- INTESTAZIONE E SELETTORE MODALITÀ ---
    st.title("🚚 Generatore Barcode Logistics")
    
    # Generazione STAT77 sotto il titolo (visibile solo in stampa)
    stat77_b64 = generate_barcode_base64("STAT77")
    stat77_img_tag = f'<img src="data:image/png;base64,{stat77_b64}">' if stat77_b64 else ''
    
    st.markdown(f"""
        <div class="print-header-stat77">
            <div style="font-weight: bold; font-size: 14px; margin-bottom: 2px;">STAT77</div>
            {stat77_img_tag}
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("⚙️ Opzioni")
        if st.button("🔒 Blocca / Esci"):
            st.session_state.authenticated = False
            st.rerun()
        st.markdown("---")
        st.info("💡 **Nota Stampa:**\nLayout a singola colonna con box ordinati e barcode STAT77 in cima.")

    mode = st.radio(
        "Seleziona la modalità di lavoro:",
        [
            "📋 Modalità 1: Inserimento Manuale", 
            "📊 Modalità 2: Google Sheets (città_linea)"
        ],
        horizontal=True
    )

    st.markdown("---")

    # ==========================================
    # MODALITÀ 1: INSERIMENTO MANUALE
    # ==========================================
    if "Modalità 1" in mode:
        st.subheader("📋 Inserimento Manuale")
        st.caption("Inserisci manualmente i dati per fino a 12 linee.")

        if "manual_data" not in st.session_state:
            
