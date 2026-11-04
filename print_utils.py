# --- print_utils.py ---

def get_print_styles():
    """Restituisce CSS elegante e ad alta visibilità per titolo, card e stampa."""
    return """
    <style>
    .info-line {
        font-size: 15px !important;
        margin-bottom: 4px !important;
    }
    
    /* Intestazione principale con camioncino ed effetto elegante */
    .top-main-header {
        text-align: center;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #444;
    }
    .top-main-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 8px;
        color: #ffffff;
    }
    .stat77-subblock {
        margin-top: 8px;
    }
    .stat77-subblock img {
        max-height: 45px;
        width: auto;
    }

    /* Card singole */
    .print-card {
        margin-bottom: 12px;
        padding: 10px;
        border: 1.5px solid #ccc;
        border-radius: 6px;
    }
    
    .print-card-title {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 4px;
    }

    .line-code-highlight {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #4f46e5 !important;
    }

    .line-barcode {
        max-height: 52px;
        width: auto;
        margin-top: 6px;
    }

    @media print {
        [data-testid="stSidebar"], [data-testid="stHeader"], header, footer, .stButton, .stRadio, .stTextInput, .stAlert {
            display: none !important;
        }
        body {
            background: white !important;
            color: black !important;
        }
        /* Colore nero pieno e nitido per la stampa */
        .top-main-title {
            color: #000000 !important;
            font-size: 22px !important;
        }
        .top-main-header {
            border-bottom: 1.5px solid #000 !important;
            margin-bottom: 15px !important;
        }
        .print-card {
            background: white !important;
            border: 1px solid #999 !important;
        }
        .line-code-highlight {
            color: black !important;
        }
    }
    </style>
    """

def render_stat77_header(stat77_img_tag):
    """Genera l'intestazione elegante con il camioncino, il nome dell'app e STAT77."""
    if not stat77_img_tag:
        return ""
    return f"""
    <div class="top-main-header">
        <div class="top-main-title">🚚 Generatore Barcode Logistics</div>
        <div class="stat77-subblock">
            <div style="font-weight: bold; font-size: 13px; margin-bottom: 2px; letter-spacing: 1px;">STAT77</div>
            {stat77_img_tag}
        </div>
    </div>
    """

def render_logistics_card(citta_val, info_str, linea_val, linea_img_tag):
    """Genera la card pulita con risalto sul numero linea."""
    return f"""
    <div class="print-card">
        <div class="print-card-title">Destinazione: {citta_val}</div>
        <div class="info-line">{info_str}<b>Linea:</b> <span class="line-code-highlight">{linea_val}</span></div>
        <div style="text-align: center;">{linea_img_tag}</div>
    </div>
    """
    
