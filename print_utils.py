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
    
    /* Intestazione STAT77 visibile a schermo sopra le card */
    .stat77-header-block {
        text-align: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #333;
    }
    .stat77-header-block img {
        max-height: 45px;
        width: auto;
    }

    @media print {
        /* Nasconde elementi superflui dell'interfaccia, i bottoni e i sottotitoli delle sezioni */
        [data-testid="stSidebar"], [data-testid="stHeader"], header, footer, 
        .stButton, .stRadio, .stTextInput, .stAlert, button, h2, h3, p, caption {
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
        
        /* Titolo principale in cima alla pagina stampata con font più piccolo */
        h1 {
            font-size: 18px !important;
            text-align: center !important;
            margin-bottom: 5px !important;
            color: black !important;
        }

        /* Layout dello STAT77 in cima alla pagina stampata */
        .stat77-header-block {
            display: block !important;
            text-align: center !important;
            margin-top: 2px !important;
            margin-bottom: 10px !important;
            padding-bottom: 5px !important;
            border-bottom: 1.5px solid #000 !important;
            page-break-after: avoid !important;
            break-after: avoid !important;
        }
        .stat77-header-block img {
            max-height: 40px !important;
            width: auto !important;
        }

        /* Card singole pulite (senza STAT77 interno) */
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
        
        /* Barcode della linea */
        .line-barcode {
            max-height: 48px !important;
            max-width: 100% !important;
            width: auto !important;
            margin-top: 4px !important;
        }
    }
    </style>
    """

def render_stat77_header(stat77_img_tag):
    """Genera il blocco unico STAT77 in cima alla pagina."""
    if not stat77_img_tag:
        return ""
    return f"""
    <div class="stat77-header-block">
        <div style="font-weight: bold; font-size: 13px; margin-bottom: 2px;">STAT77</div>
        {stat77_img_tag}
    </div>
    """

def render_logistics_card(citta_val, info_str, linea_val, linea_img_tag):
    """Genera l'HTML di una singola card logistica pulita."""
    return f"""
    <div class="print-card">
        <div class="print-card-title">🚚 {citta_val}</div>
        <div class="info-line">{info_str}<b>Linea:</b> <code>{linea_val}</code></div>
        <div style="text-align: center;">{linea_img_tag}</div>
    </div>
    """
    
