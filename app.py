import streamlit as st
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import io
import base64

# Configurazione Pagina
st.set_page_config(page_title="Generatore Barcode Logistics", page_icon="🚚", layout="centered")

# --- CSS DEFINITIVO PER STAMPA PULITA (SOLO DATI IN 1-2 PAGINE) ---
st.markdown("""
    <style>
    @media print {
        /* Nasconde tutto ciò che non fa parte dell'elenco delle linee */
        header, footer, .stSidebar, .stRadio, button, .stButton, .stTextInput, .stAlert, h1, h2 {
            display: none !important;
        }
        body * {
            visibility: hidden;
        }
        .print-container, .print-container * {
            visibility: visible;
        }
        .print-container {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
        }
        body, .stApp {
            background: white !important;
            color: black !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        .print-card {
            page-break-inside: avoid;
            break-inside: avoid;
            margin-bottom: 3px !important;
            padding: 2px !important;
        }
        h3 {
            font-size: 11px !important;
            margin: 2px 0 1px 0 !important;
        }
        p, div, span {
            font-size: 9px !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        hr {
            margin: 2px 0 !important;
            border-color: #ddd !important;
        }
        img {
            max-height: 32px !important;
            width: auto !important;
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

    # --- FUNZIONE GENERAZIONE BARCODE COMPATTO ---
    def generate_barcode_base64(value):
        if not value or str(value).strip() == "" or str(value).strip().lower() == "nan" or str(value).strip() == "none":
            return None
        try:
            CODE128 = barcode.get_barcode_class('code128')
            rv = io.BytesIO()
            val_str = str(value).split('.')[0].strip()
            code = CODE128(val_str, writer=ImageWriter())
            code.write(rv, options={"module_height": 4.0, "font_size": 8, "text_distance": 2.0, "quiet_zone": 1.0})
            return base64.b64encode(rv.getvalue()).decode("utf-8")
        except Exception as e:
            return None

    # --- INTESTAZIONE E SELETTORE MODALITÀ ---
    st.title("🚚 Generatore Barcode Logistics")
    
    with st.sidebar:
        st.subheader("⚙️ Opzioni")
        if st.button("🔒 Blocca / Esci"):
            st.session_state.authenticated = False
            st.rerun()
        st.markdown("---")
        st.info("💡 **Nota Stampa:**\nI menu e le intestazioni vengono nascosti automaticamente in stampa per fare entrare tutte le linee in 1 o 2 pagine A4.")

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
            st.session_state.manual_data = [{"destinazione": "", "targa": "", "linea": ""} for _ in range(12)]

        for idx in range(12):
            st.markdown(f"##### Linea {idx + 1}")
            c1, c2, c3 = st.columns(3)
            
            dest = c1.text_input(f"Destinazione #{idx+1}", value=st.session_state.manual_data[idx]["destinazione"], placeholder="città", key=f"dest_{idx}")
            targa = c2.text_input(f"Targa #{idx+1}", value=st.session_state.manual_data[idx]["targa"], placeholder="Targa", key=f"targa_{idx}")
            linea = c3.text_input(f"Num. Linea #{idx+1}", value=st.session_state.manual_data[idx]["linea"], placeholder="Linea", key=f"linea_{idx}")
            
            st.session_state.manual_data[idx] = {"destinazione": dest, "targa": targa, "linea": linea}

            if linea:
                b64_img = generate_barcode_base64(linea)
                if b64_img:
                    st.image(f"data:image/png;base64,{b64_img}", use_container_width=True)
            st.markdown("---")

    # ==========================================
    # MODALITÀ 2: GOOGLE SHEETS AUTOMATICO
    # ==========================================
    else:
        st.subheader("📊 Google Sheets: città_linea")
        st.caption("Lettura automatica in tempo reale dal foglio Google.")

        SHEET_ID = "1-EM7rpDYaj1VF_JvFCD6rAdwVox_adkJdFkgqmN30Ew"
        CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

        if st.button("🔄 Ricarica Dati"):
            st.cache_data.clear()

        @st.cache_data(ttl=60)
        def load_sheet_data(url):
            return pd.read_csv(url)

        try:
            df = load_sheet_data(CSV_URL)
            
            # Pulizia nomi colonne
            df.columns = [str(col).strip().lower() for col in df.columns]

            # Converte in stringa e rimuove il .0 se presente
            if 'linea' in df.columns:
                df['linea'] = df['linea'].astype(str).str.replace('.0', '', regex=False)
                df_valid = df[df['linea'].str.lower() != 'nan'].copy()
            else:
                df_valid = df.copy()

            if df_valid.empty:
                st.warning("Il foglio Google non contiene righe con numeri di linea compilati.")
            else:
                st.success(f"Caricate {len(df_valid)} linee in ordine dal foglio!")
                
                # Contenitore isolato esclusivamente per la stampa
                st.markdown('<div class="print-container">', unsafe_allow_html=True)
                
                for idx, row in df_valid.reset_index(drop=True).iterrows():
                    citta_val = str(row.get('città', '')).replace('nan', '').strip()
                    linea_val = str(row.get('linea', '')).replace('nan', '').strip()
                    targa_val = str(row.get('targa', '')).replace('nan', '').strip()
                    partenza_val = str(row.get('partenza', '')).replace('nan', '').strip()

                    if not linea_val or linea_val == '':
                        continue

                    st.markdown('<div class="print-card">', unsafe_allow_html=True)
                    
                    st.markdown(f"### 🚚 {citta_val}")
                    
                    info_text = []
                    if targa_val:
                        info_text.append(f"**Targa:** {targa_val}")
                    if partenza_val:
                        info_text.append(f"**Partenza:** {partenza_val}")
                    if info_text:
                        st.write(" | ".join(info_text))
                        
                    st.write(f"**Linea:** `{linea_val}`")

                    b64_img = generate_barcode_base64(linea_val)
                    if b64_img:
                        st.image(f"data:image/png;base64,{b64_img}", use_container_width=True)
                    
                    st.markdown("---")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Errore durante il caricamento del foglio Google: {e}")
            
