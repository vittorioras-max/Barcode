# --- print_utils.py ---
# Modulo esterno per la gestione della grafica, dei CSS di stampa e dei layout delle card

def get_print_styles():
    """Restituisce il blocco CSS ottimizzato per la stampa e la schermata."""
    return """
    <style>
    /* Stile testi informativi a schermo */
    .info-line {
        font-size: 14px !important;
        color: #d1d5db !important;
        margin-bottom: 3px !important;
    }

    @media print {
        /* Nasconde intestazioni globali, titoli, descrizioni e comandi in stampa */
        [data-testid="stSidebar"], [data-testid="stHeader"], header, footer, 
        .stButton, .stRadio, .stTextInput, .stAlert, button, h1, h2, p {
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

        /* Card singole ottimizzate con STAT77 integrato in cima ad ognuna */
        .print-card {
            page-break-inside: avoid;
            break-inside: avoid;
            margin-bottom: 8px !important;
            padding: 8px !important;
            border: 1.5px solid #999 !important;
            border-radius: 4px !important;
            background: white !important;
            width: 100% !important;
        }
        
        /* Sezione STAT77 interna alla card */
        .card-stat77-container {
            text-align: center !important;
            border-bottom: 1px dashed #bbb !important;
            padding-bottom: 4px !important;
            margin-bottom: 6px !important;
        }
        .card-stat77-title {
            font-weight: bold !important;
            font-size: 12px !important;
            margin-bottom: 1px !important;
            color: #000 !important;
        }
        .card-stat77-container img {
            max-height: 36px !important;
            width: auto !important;
        }
        
        /* Testi interni alla card */
        .print-card-title {
            font-weight: bold !important;
            font-size: 18px !important;
            margin-bottom: 4px !important;
            color: #000 !important;
        }
        
        .info-line {
            color: #000 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
        }
        
        code {
            background: none !important;
            color: #000 !important;
            border: none !important;
            padding: 0 !important;
            font-size: 15px !important;
            font-weight: bold !important;
        }
        
        /* Barcode principale della linea */
        .line-barcode {
            max-height: 48px !important;
            max-width: 100% !important;
            width: auto !important;
            margin-top: 4px !important;
        }
    }
    </style>
    """

def render_logistics_card(citta_val, info_str, linea_val, linea_img_tag, stat77_img_tag):
    """Genera l'HTML di una singola card logistica con STAT77 incorporato in alto."""
    return f"""
    <div class="print-card">
        <div class="card-stat77-container">
            <div class="card-stat77-title">STAT77</div>
            {stat77_img_tag}
        </div>
        <div class="print-card-title">🚚 {citta_val}</div>
        <div class="info-line">{info_str}<b>Linea:</b> <code>{linea_val}</code></div>
        <div style="text-align: center;">{linea_img_tag}</div>
    </div>
    """
    
