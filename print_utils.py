# --- print_utils.py ---

def get_print_styles():
    return """
    <style>
    .top-main-header {
        text-align: center;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #444;
    }
    .top-main-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 6px;
    }
    .stat77-header-block {
        text-align: center;
        margin-top: 6px;
    }
    .stat77-header-block img {
        max-height: 42px;
        width: auto;
    }

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

    .info-line {
        font-size: 14px;
        margin-bottom: 4px;
    }

    .line-code-highlight {
        font-weight: bold;
        color: #4f46e5;
    }

    .line-barcode {
        max-height: 50px;
        width: auto;
        margin-top: 4px;
    }

    @media print {
        /* Nasconde la scritta e il blocco di Google Sheets solo in stampa */
        div:has(> h3) {
            display: none !important;
        }

        [data-testid="stSidebar"], [data-testid="stHeader"], header, footer, .stButton, .stRadio, .stTextInput, .stAlert {
            display: none !important;
        }
        body {
            background: white !important;
            color: black !important;
        }
        .print-card {
            page-break-inside: avoid;
            background: white !important;
            border: 1.5px solid #999 !important;
        }
        .print-card-title, .info-line, .line-code-highlight, .top-main-title {
            color: black !important;
        }
    }
    </style>
    """

def render_stat77_header(stat77_img_tag):
    if not stat77_img_tag:
        return ""
    return f"""
    <div class="top-main-header">
        <div class="top-main-title">🚚 Generatore Barcode Logistics</div>
        <div class="stat77-header-block">
            <div style="font-weight: bold; font-size: 12px; margin-bottom: 2px; letter-spacing: 1px;">STAT77</div>
            {stat77_img_tag}
        </div>
    </div>
    """

def render_logistics_card(citta_val, info_str, linea_val, linea_img_tag):
    return f"""
    <div class="print-card">
        <div class="print-card-title">Destinazione: {citta_val}</div>
        <div class="info-line">{info_str}<b>Linea:</b> <span class="line-code-highlight">{linea_val}</span></div>
        <div style="text-align: center;">{linea_img_tag}</div>
    </div>
    """
    
