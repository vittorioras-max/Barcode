import streamlit as st
from utils.barcode_utils import generate_barcode_image

st.set_page_config(
    page_title="Generatore Codici a Barre in Sequenza",
    page_icon="🏷️",
    layout="wide"
)

st.title("🏷️ Generatore di Codici a Barre")
st.markdown("Inserisci i dati nei campi sottostanti. Puoi associare un'etichetta/nome a ciascun codice a barre.")

codes = []

# Creiamo i 12 moduli di input
for i in range(1, 13):
    st.markdown(f"##### 📍 Elemento {i}")
    col_label, col_code = st.columns([1, 2])
    
    with col_label:
        label_val = st.text_input(
            f"destination {i}", 
            key=f"label_{i}", 
            placeholder=f"Es. City"
        )
    
    with col_code:
        code_val = st.text_input(
            f"Numero {i}", 
            key=f"code_{i}", 
            placeholder=f"Es. 12345{i}"
        )
    
    # Se l'utente inserisce un'etichetta la usiamo, altrimenti usiamo "Posizione X"
    final_label = label_val.strip() if label_val and label_val.strip() else f"Posizione {i}"
    codes.append((final_label, code_val))

st.divider()
st.subheader("📋 Sequenza Codici a Barre Generati")

has_any_code = False

# Visualizzazione in sequenza
for label, code_val in codes:
    if code_val and code_val.strip():
        has_any_code = True
        
        with st.container():
            st.markdown(f"### 🏷️ {label} — Valore: `{code_val.strip()}`")
            
            img_bytes = generate_barcode_image(code_val)
            
            if img_bytes:
                st.image(img_bytes, width=350)
            else:
                st.error(f"Errore nella generazione per il valore '{code_val}'. Verifica che contenga caratteri validi.")
            
            st.markdown("---")

if not has_any_code:
    st.info("ℹ️ Nessun numero inserito. Compila almeno un campo sopra per visualizzare il codice a barre corrispondente.")
  
