import streamlit as st
from utils.barcode_utils import generate_barcode_image

st.set_page_config(
    page_title="Generatore Codici a Barre in Sequenza",
    page_icon="🏷️",
    layout="wide"
)

st.title("🏷️ Generatore di Codici a Barre")
st.markdown("Inserisci i dati nei campi sottostanti. I codici a barre compatti in altezza ma larghi verranno generati per Targa e Numero.")

codes = []

# Creiamo i 12 moduli di input
for i in range(1, 13):
    st.markdown(f"##### 📍 Elemento {i}")
    col_dest, col_plate, col_code = st.columns([1, 1, 2])
    
    with col_dest:
        dest_val = st.text_input(
            f"Destinazione {i}", 
            key=f"dest_{i}", 
            placeholder=f"Es. city"
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
    
    final_dest = dest_val.strip() if dest_val and dest_val.strip() else f"Posizione {i}"
    final_plate = plate_val.strip() if plate_val and plate_val.strip() else ""
    final_code = code_val.strip() if code_val and code_val.strip() else ""
    
    codes.append((i, final_dest, final_plate, final_code))

st.divider()
st.subheader("📋 Sequenza Codici a Barre Generati")

has_any_code = False

# Visualizzazione in sequenza
for index, dest, plate, code_val in codes:
    if plate or code_val:
        has_any_code = True
        
        with st.container():
            # Codici a barre larghi ma bassi
            col_bc_plate, col_bc_num = st.columns(2)
            
            with col_bc_plate:
                if plate:
                    st.markdown(f"**Targa:** `{plate}`")
                    img_plate = generate_barcode_image(plate)
                    if img_plate:
                        st.image(img_plate, use_container_width=True)
                    else:
                        st.error("Errore generazione barcode targa.")
            
            with col_bc_num:
                if code_val:
                    st.markdown(f"**Numero:** `{code_val}`")
                    img_code = generate_barcode_image(code_val)
                    if img_code:
                        st.image(img_code, use_container_width=True)
                    else:
                        st.error("Errore generazione barcode numero.")

            # Dettagli della linea sotto
            plate_info = f" | 🚛 Targa: `{plate}`" if plate else ""
            code_info = f" | 🔢 Numero: `{code_val}`" if code_val else ""
            st.markdown(f"#### 📍 Linea {index}: **{dest}**{plate_info}{code_info}")
            
            st.markdown("---")

if not has_any_code:
    st.info("ℹ️ Nessun dato inserito. Compila Targa o Numero in almeno un campo sopra.")
    
