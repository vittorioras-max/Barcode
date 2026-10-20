import streamlit as st
from utils.barcode_utils import generate_barcode_image

st.set_page_config(
    page_title="Generatore Codici a Barre in Sequenza",
    page_icon="🏷️",
    layout="wide"
)

st.title("🏷️ Generatore di Codici a Barre")
st.markdown("Inserisci i numeri nei campi sottostanti. I codici a barre verranno generati automaticamente in sequenza solo per i campi compilati.")

# Organizziamo i 12 campi di input in 2 colonne per un layout pulito
col_input_1, col_input_2 = st.columns(2)

codes = []
for i in range(1, 13):
    # Distribuiamo i 12 campi equamente tra le due colonne
    target_col = col_input_1 if i <= 6 else col_input_2
    with target_col:
        val = st.text_input(
            f"Numero {i}", 
            key=f"code_{i}", 
            placeholder=f"Es. 12345{i}"
        )
        codes.append((i, val))

st.divider()
st.subheader("📋 Sequenza Codici a Barre Generati")

# Sezione di visualizzazione in sequenza
has_any_code = False

for index, code_val in codes:
    if code_val and code_val.strip():
        has_any_code = True
        
        # Contenitore visivo per ogni elemento
        with st.container():
            st.markdown(f"**Posizione {index}** — Valore: `{code_val.strip()}`")
            
            # Generazione immagine
            img_bytes = generate_barcode_image(code_val)
            
            if img_bytes:
                st.image(img_bytes, width=350)
            else:
                st.error(f"Errore nella generazione per il valore '{code_val}'. Verifica che contenga caratteri validi.")
            
            st.markdown("---")

if not has_any_code:
    st.info("ℹ️ Nessun numero inserito. Compila almeno un campo sopra per visualizzare il codice a barre corrispondente.")
  
