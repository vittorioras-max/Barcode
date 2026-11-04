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
        @page {
            margin-top: 25mm;
            margin-bottom: 15mm;
            margin-left: 10mm;
            margin-right: 10mm;
        }

        [data-testid="stSidebar"], [data-testid="stHeader"], header, footer, .stButton, .stRadio, .stTextInput, .stAlert {
            display: none !important;
        }
        body {
            background: white !important;
            color: black !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .top-main-header {
            border-bottom: none !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        .top-main-title {
            font-size: 18px !important;
            color: black !important;
            margin-bottom: 4px !important;
        }

        /* STAT77 fisso e ripetuto in cima a OGNI pagina stampata */
        .stat77-header-block {
            display: block !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            background: white !important;
            padding-bottom: 6px !important;
            border-bottom: 1.5px solid #000 !important;
            z-index: 9999 !important;
        }
        .stat77-header-block img {
            max-height: 38px !important;
            width: auto !important;
        }

        .print-card {
            page-break-inside: avoid;
            break-inside: avoid;
            background: white !important;
            border: 1.5px solid #999 !important;
            margin-bottom: 8px !important;
            padding: 8px !important;
        }
        .print-card-title {
            color: black !important;
            font-size: 16px !important;
        }
        .info-line {
            color: black !important;
        }
        .line-code-highlight {
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
    
