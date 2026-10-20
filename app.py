import streamlit as st
from utils.barcode_utils import generate_barcode_image

st.set_page_config(
    page_title="Generatore Codici a Barre in Sequenza",
    page_icon="🏷️",
    layout="wide"
)

st.title("🏷️ Generatore di Codici a Barre")
st.markdown("Inserisci i dati nei campi sottostanti. Puoi associare Destinazione, Targa e linea a ciascun codice a barre.")

codes = []

# Creiamo i 12 moduli di input
for i in range(1, 13):
    st.markdown(f"##### 📍 Elemento {i}")
    col_dest, col_plate, col_code = st.columns([1, 1, 2])
    
    with col_dest:
        dest_val = st.text_input(
            f"Destinazione {i}", 
            key=f"dest_{i}", 
            placeholder=f"Es. City"
        )
    
    with col_plate:
        plate_val = st.text_input(
            f"Targa {i}", 
            key=f"plate_{i}", 
            placeholder=f"Es. AB123CD"
        )
    
    with col_code:
        code_val = st.text_input(
            f"Numero linea {i}", 
            key=f"code_{i}", 
            placeholder=f"Es. 12345{i}"
        )
    
    # Gestione etichetta di destinazione default se lasciata vuota
    final_dest = dest_val.strip() if dest_val and dest_val.strip() else f"Posizione {i}"
    final_plate = plate_val.strip() if plate_val and plate_val.strip() else ""
    
    codes.append((final_dest, final_plate, code_val))

st.divider()
st.subheader("📋 Sequenza Codici a Barre Generati")

has_any_code = False

# Visualizzazione in sequenza
for dest, plate, code_val in codes:
    if code_val and code_val.strip():
        has_any_code = True
        
        with st.container():
            # Mostra la destinazione e la targa (se inserita)
            plate_info = f" | 🚛 Targa: `{plate}`" if plate else ""
            st.markdown(f"### 🏷️ {dest}{plate_info} — Valore: `{code_val.strip()}`")
            
            img_bytes = generate_barcode_image(code_val)
            
            if img_bytes:
                st.image(img_bytes, width=350)
            else:
                st.error(f"Errore nella generazione per il valore '{code_val}'. Verifica che contenga caratteri validi.")
            
            st.markdown("---")

if not has_any_code:
    st.info("ℹ️ Nessun numero inserito. Compila almeno un campo sopra per visualizzare il codice a barre corrispondente.")
    
