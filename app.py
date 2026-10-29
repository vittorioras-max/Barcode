import streamlit as st
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import io
import base64

# Configurazione Pagina
st.set_page_config(page_title="Generatore Barcode Logistics", page_icon="🚚", layout="wide")

# Controllo Password (Se presente nei secrets)
def check_password():
    if "password" not in st.secrets:
        return True
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔒 Accesso Riservato")
        pwd = st.text_input("Inserisci la password:", type="password")
        if st.button("Accedi"):
            if pwd == st.secrets["password"]:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Password errata!")
        return False
    return True

if check_password():

    # Funzione per generare il Code 128 in base64 (con altezza dimezzata a 5.0)
    def generate_barcode_base64(value):
        if not value or str(value).strip() == "" or str(value).strip().lower() == "nan":
            return None
        try:
            CODE128 = barcode.get_barcode_class('code128')
            rv = io.BytesIO()
            val_str = str(value).split('.')[0].strip()
            code = CODE128(val_str, writer=ImageWriter())
            code.write(rv, options={"module_height": 5.0, "font_size": 10, "text_distance": 3.0, "quiet_zone": 2.0})
            return base64.b64encode(rv.getvalue()).decode("utf-8")
        except Exception as e:
            return None

    # SELETTORE MODALITÀ IN ALTO
    st.title("🚚 Generatore Barcode Logistics")
    
    mode = st.radio(
        "Seleziona la modalità di lavoro:",
        [
            "📋 Modalità 1: Inserimento Manuale (Modulo Singolo)", 
            "📊 Modalità 2: Caricamento Automatico da Google Sheets (città_linea)"
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

        cols = st.columns(2)
        
        for idx in range(12):
            with cols[idx % 2]:
                st.markdown(f"##### Linea {idx + 1}")
                c1, c2, c3 = st.columns([2, 2, 2])
                
                dest = c1.text_input(f"Destinazione #{idx+1}", value=st.session_state.manual_data[idx]["destinazione"], placeholder="città", key=f"dest_{idx}")
                targa = c2.text_input(f"Targa #{idx+1}", value=st.session_state.manual_data[idx]["targa"], placeholder="Targa", key=f"targa_{idx}")
                linea = c3.text_input(f"Numero Linea #{idx+1}", value=st.session_state.manual_data[idx]["linea"], placeholder="Num. Linea", key=f"linea_{idx}")
                
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
        st.subheader("📊 Caricamento Automatico da Google Sheets")
        st.caption("I dati vengono letti direttamente dal foglio online `città_linea` rispettando l'ordine delle righe.")

        SHEET_ID = "1-EM7rpDYaj1VF_JvFCD6rAdwVox_adkJdFkgqmN30Ew"
        CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

        if st.button("🔄 Ricarica Dati da Google Sheets"):
            st.cache_data.clear()

        @st.cache_data(ttl=60)
        def load_sheet_data(url):
            return pd.read_csv(url)

        try:
            df = load_sheet_data(CSV_URL)
            
            # Pulizia nomi colonne
            df.columns = [str(col).strip().lower() for col in df.columns]

            # Mantiene l'ordine esatto del file rimuovendo solo le righe completamente vuote o senza linea
            if 'linea' in df.columns:
                df_valid = df.dropna(subset=['linea']).copy()
            else:
                df_valid = df.copy()

            if df_valid.empty:
                st.warning("Il foglio Google è collegato ma non contiene righe con numeri di linea compilati.")
            else:
                st.success(f"Caricate con successo {len(df_valid)} linee dal foglio Google!")
                
                grid_cols = st.columns(2)
                
                for idx, row in df_valid.reset_index(drop=True).iterrows():
                    citta_val = str(row.get('città', '')).replace('nan', '')
                    linea_val = str(row.get('linea', '')).replace('nan', '')
                    targa_val = str(row.get('targa', '')).replace('nan', '')
                    partenza_val = str(row.get('partenza', '')).replace('nan', '')

                    if not linea_val:
                        continue

                    col_target = grid_cols[idx % 2]
                    
                    with col_target:
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

        except Exception as e:
            st.error(f"Errore durante il caricamento del foglio Google: {e}")
            st.info("Verifica che il foglio sia condiviso pubblicamente in modalità visualizzazione.")
            
