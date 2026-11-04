import streamlit as st
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import io
import base64

from print_utils import get_print_styles, render_stat77_header, render_logistics_card

st.set_page_config(page_title="Generatore Barcode Logistics", page_icon="🚚", layout="centered")

st.markdown(get_print_styles(), unsafe_allow_html=True)

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

    stat77_b64 = generate_barcode_base64("STAT77")
    stat77_img_tag = f'<img src="data:image/png;base64,{stat77_b64}">' if stat77_b64 else ''
    st.markdown(render_stat77_header(stat77_img_tag), unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("⚙️ Opzioni")
        if st.button("🔒 Blocca / Esci"):
            st.session_state.authenticated = False
            st.rerun()

    mode = st.radio(
        "Seleziona la modalità di lavoro:",
        [
            "📋 Modalità 1: Inserimento Manuale", 
            "📊 Modalità 2: Google Sheets (città_linea)"
        ],
        horizontal=True
    )

    st.markdown("---")

    if "Modalità 1" in mode:
        st.subheader("📋 Inserimento Manuale")

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

    else:
        st.subheader("📊 Google Sheets: città_linea")

        SHEET_ID = "1-EM7rpDYaj1VF_JvFCD6rAdwVox_adkJdFkgqmN30Ew"
        CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

        if st.button("🔄 Ricarica Dati"):
            st.cache_data.clear()

        @st.cache_data(ttl=60)
        def load_sheet_data(url):
            return pd.read_csv(url)

        try:
            df = load_sheet_data(CSV_URL)
            df.columns = [str(col).strip().lower() for col in df.columns]

            if 'linea' in df.columns:
                df['linea'] = df['linea'].astype(str).str.replace('.0', '', regex=False)
                df_valid = df[df['linea'].str.lower() != 'nan'].copy()
            else:
                df_valid = df.copy()

            if df_valid.empty:
                st.warning("Il foglio Google non contiene righe con numeri di linea compilati.")
            else:
                st.success(f"Caricate {len(df_valid)} linee dal foglio!")
                
                for idx, row in df_valid.reset_index(drop=True).iterrows():
                    citta_val = str(row.get('città', '')).replace('nan', '').strip()
                    linea_val = str(row.get('linea', '')).replace('nan', '').strip()
                    targa_val = str(row.get('targa', '')).replace('nan', '').strip()
                    partenza_val = str(row.get('partenza', '')).replace('nan', '').strip()

                    if not linea_val or linea_val == '':
                        continue

                    info_parts = []
                    if targa_val and targa_val.lower() != 'nan':
                        info_parts.append(f"Targa: {targa_val}")
                    if partenza_val and partenza_val.lower() != 'nan':
                        info_parts.append(f"Partenza: {partenza_val}")
                    
                    info_str = " | ".join(info_parts)
                    if info_str:
                        info_str += " &nbsp;|&nbsp; "

                    b64_img = generate_barcode_base64(linea_val)
                    linea_img_tag = f'<img src="data:image/png;base64,{b64_img}" class="line-barcode">' if b64_img else ''

                    st.markdown(render_logistics_card(citta_val, info_str, linea_val, linea_img_tag), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Errore durante il caricamento del foglio Google: {e}")
            
