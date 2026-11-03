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

        /* Card singole ottimizzate per la stampa con font più grandi e leggibili */
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
        
        /* Testi interni alla card ingranditi per evitare l'effetto "piccolo" in stampa */
        .print-card-title {
            font-weight: bold !important;
            font-size: 20px !important;
            margin-bottom: 4px !important;
            color: #000 !important;
        }
        
        .info-line {
            color: #000 !important;
            font-size: 15px !important;
            font-weight: 500 !important;
        }
        
        code {
            background: none !important;
            color: #000 !important;
            border: none !important;
            padding: 0 !important;
            font-size: 16px !important;
            font-weight: bold !important;
        }
        
        /* Barcode stampabile ben proporzionato */
        img {
            max-height: 52px !important;
            max-width: 100% !important;
            width: auto !important;
            margin-top: 4px !important;
        }
    }
    </style>
    """

def render_stat77_header(stat77_img_tag):
    """Restituisce l'intestazione STAT77 per la stampa."""
    return f"""
        <div class="print-header-stat77">
            <div style="font-weight: bold; font-size: 15px; margin-bottom: 2px;">STAT77</div>
            {stat77_img_tag}
        </div>
    """

def render_logistics_card(citta_val, info_str, linea_val, img_tag):
    """Genera l'HTML di una singola card logistica pulita e con font ingranditi per la stampa."""
    return f"""
    <div class="print-card">
        <div class="print-card-title">🚚 {citta_val}</div>
        <div class="info-line">{info_str}<b>Linea:</b> <code>{linea_val}</code></div>
        {img_tag}
    </div>
    """
