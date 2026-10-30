import streamlit as st
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import io
import base64

# Configurazione Pagina
st.set_page_config(page_title="Generatore Barcode Logistics", page_icon="🚚", layout="centered")

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

# Generiamo l'immagine fissa per STAT77 in MAIUSCOLO
stat77_b64 = generate_barcode_base64("STAT77")
stat77_img_tag = f'<img src="data:image/png;base64,{stat77_b64}">' if stat77_b64 else ''

# --- CSS CON STAMPA A 2 COLONNE E BARCODE STAT77 IN CIMA ---
st.markdown(f"""
    <style>
    /* Colore chiaro per i testi informativi a schermo scuro */
    .info-line {{
        font-size: 13px !important;
        color: #d1d5db !important;
        margin-bottom: 2px !important;
    }}
    @media print {{
        [data-testid="stSidebar"], [data-testid="stHeader"], header, footer, 
        .stButton, .stRadio, .stTextInput, .stAlert, button {{
            display: none !important;
        }}
        body, .stApp {{
            background: white !important;
            color: black !important;
            margin: 0 !important;
            padding: 2mm !important;
        }}
        div[data-testid="stVerticalBlock"] {{
            gap: 0px !important;
        }}
        
        /* Sezione STAT77 visibile SOLO in stampa in cima alla pagina */
        .print-header-stat77 {{
            display: block !important;
            width: 100% !important;
            text-align: center !important;
            margin-bottom: 10px !important;
            padding-bottom: 5px !important;
            border-bottom: 2px solid #000 !important;
            page-break-after: avoid !important;
            break-after: avoid !important;
        }}

        /* Utilizzo di column-count per le 2 colonne reali in stampa */
        .print-grid {{
            column-count: 2 !important;
            column-gap: 8px !important;
            width: 100% !important;
        }}
        .print-card {{
            page-break-inside: avoid;
            break-inside: avoid;
            margin-bottom: 4px !important;
            padding: 2px !important;
            border-bottom: 1px solid #ddd !important;
            display: inline-block !important;
            width: 100% !important;
        }}
        .info-line {{
            color: #000 !important;
            font-size: 13px !important;
        }}
        code {{
            background: none !important;
            color: #000 !important;
            border: none !important;
            padding: 0 !important;
            font-weight: bold !important;
        }}
        img {{
            max-height: 38px !important;
            max-width: 100% !important;
            width: auto !important;
            margin-top: 1px !important;
        }}
    }}
    /* Nascosto a schermo normale, visibile solo durante la stampa */
    .print-header-stat77 {{
        display: none;
    }}
    </style>

    <!-- Header STAT77 in MAIUSCOLO che comparirà in cima alla pagina stampata/PDF -->
    <div class="print-header-stat77">
        <div style="font-weight: bold; font-size: 14px; margin-bottom: 2px;">STAT77</div>
        {stat77_img_tag}
    </div>
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

    # --- INTESTAZIONE E SELETTORE MODALITÀ ---
    st.title("🚚 Generatore Barcode Logistics")
    
    with st.sidebar:
        st.subheader("⚙️ Opzioni")
        if st.button("🔒 Blocca / Esci"):
            st.session_state.authenticated = False
            st.rerun()
        st.markdown("---")
        st.info("💡 **Nota Stampa:**\nInclude il barcode STAT77 in cima e le linee disposte su 2 colonne.")

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
            st.session_state.manual_data = [{"destinazione": "", "targa": "", "partenza": "", "linea": ""} for _ in range(12)]

        for idx in range(12):
            st.markdown(f"##### Linea {idx + 1}")
            c1, c2, c3, c4 = st.columns(4)
            
            dest = c1.text_input(f"Destinazione #{idx+1}", value=st.session_state.manual_data[idx]["destinazione"], placeholder="città", key=f"dest_{idx}")
            targa = c2.text_input(f"Targa #{idx+1}", value=st.session_state.manual_data[idx]["targa"], placeholder="Targa", key=f"targa_{idx}")
            partenza = c3.text_input(f"Partenza #{idx+1}", value=st.session_state.manual_data[idx]["partenza"], placeholder="Orario", key=f"partenza_{idx}")
            linea = c4.text_input(f"Num. Linea #{idx+1}", value=st.session_state.manual_data[idx]["linea"], placeholder="Linea", key=f"linea_{idx}")
            
            st.session_state.manual_data[idx] = {"destinazione": dest, "targa": targa, "partenza": partenza, "linea": linea}

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
                
                # Wrapper per la stampa a 2 colonne basato su column-count
                st.markdown('<div class="print-grid">', unsafe_allow_html=True)
                
                for idx, row in df_valid.reset_index(drop=True).iterrows():
                    citta_val = str(row.get('città', '')).replace('nan', '').strip()
                    linea_val = str(row.get('linea', '')).replace('nan', '').strip()
                    targa_val = str(row.get('targa', '')).replace('nan', '').strip()
                    partenza_val = str(row.get('partenza', '')).replace('nan', '').strip()

                    if not linea_val or linea_val == '':
                        continue

                    # Prepariamo la stringa con targa e orario di partenza
                    info_parts = []
                    if targa_val:
                        info_parts.append(f"Targa: {targa_val}")
                    if partenza_val:
                        info_parts.append(f"Partenza: {partenza_val}")
                    info_str = " | ".join(info_parts)
                    if info_str:
                        info_str += " &nbsp;|&nbsp; "

                    b64_img = generate_barcode_base64(linea_val)
                    img_tag = f'<img src="data:image/png;base64,{b64_img}">' if b64_img else ''

                    st.markdown(f"""
                    <div class="print-card">
                        <div style="font-weight: bold; font-size: 18px; margin-bottom: 2px;">🚚 {citta_val}</div>
                        <div class="info-line">{info_str}<b>Linea:</b> <code>{linea_val}</code></div>
                        {img_tag}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Errore durante il caricamento del foglio Google: {e}")
            
