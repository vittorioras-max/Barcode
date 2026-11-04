# --- print_utils.py ---

def get_print_styles():
    """Restituisce CSS semplice e lineare senza elementi fissi pesanti."""
    return """
    <style>
    .info-line {
        font-size: 14px !important;
        color: #d1d5db !important;
        margin-bottom: 3px !important;
    }
    
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

    .print-card {
        margin-bottom: 10px;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    .print-card-title {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 4px;
    }

    .line-barcode {
        max-height: 48px;
        width: auto;
        margin-top: 4px;
    }

    @media print {
        [data-testid="stSidebar"], [data-testid="stHeader"], header, footer, .stButton, .stRadio, .stTextInput, .stAlert {
            display: none !important;
        }
        body {
            background: white !important;
            color: black !important;
        }
    }
    </style>
    """

def render_stat77_header(stat77_img_tag):
    if not stat77_img_tag:
        return ""
    return f"""
    <div class="stat77-header-block">
        <div style="font-weight: bold; font-size: 13px; margin-bottom: 2px;">STAT77</div>
        {stat77_img_tag}
    </div>
    """

def render_logistics_card(citta_val, info_str, linea_val, linea_img_tag):
    return f"""
    <div class="print-card">
        <div class="print-card-title">🚚 {citta_val}</div>
        <div class="info-line">{info_str}<b>Linea:</b> <code>{linea_val}</code></div>
        <div style="text-align: center;">{linea_img_tag}</div>
    </div>
    """
    
