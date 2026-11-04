# --- print_utils.py ---

def get_print_styles():
    return """
    <style>
    .top-main-header {
        text-align: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #444;
        width: 100%;
    }
    .top-main-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 4px;
    }
    .stat77-header-block {
        text-align: center;
        margin-top: 4px;
    }
    .stat77-header-block img {
        max-height: 38px;
        width: auto;
    }

    .print-card {
        margin-bottom: 10px;
        padding: 8px 10px;
        border: 1.5px solid #ccc;
        border-radius: 6px;
    }
    
    .print-card-title {
        font-weight: bold;
        font-size: 15px;
        margin-bottom: 3px;
    }

    .info-line {
        font-size: 13px;
        margin-bottom: 3px;
    }

    .line-code-highlight {
        font-weight: bold;
        color: #4f46e5;
    }

    .line-barcode {
        max-height: 45px;
        width: auto;
        margin-top: 2px;
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

        /* Regola nativa paged media per i margini di stampa */
        @page {
            size: A4;
            margin: 10mm;
        }

        /* Sfrutta il comportamento nativo di ripetizione del thead */
        thead {
            display: table-header-group !important;
        }

        .print-card {
            page-break-inside: avoid;
            break-inside: avoid;
            background: white !important;
            border: 1.5px solid #999 !important;
            margin-bottom: 8px !important;
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
    # Soluzione nativa HTML table + thead: il browser ripeterà questo blocco su ogni pagina stampata
    return f"""
    <table style="width: 100%; border-collapse: collapse; border: none;">
        <thead>
            <tr>
                <td style="border: none; padding: 0;">
                    <div class="top-main-header">
                        <div class="top-main-title">🚛 Generatore Barcode</div>
                        <div class="stat77-header-block">
                            <div style="font-weight: bold; font-size: 11px; margin-bottom: 1px; letter-spacing: 1px;">STAT77</div>
                            {stat77_img_tag}
                        </div>
                    </div>
                </td>
            </tr>
        </thead>
    </table>
    """

def render_logistics_card(citta_val, info_str, linea_val, linea_img_tag):
    return f"""
    <div class="print-card">
        <div class="print-card-title">Destinazione: {citta_val}</div>
        <div class="info-line">{info_str}<b>Linea:</b> <span class="line-code-highlight">{linea_val}</span></div>
        <div style="text-align: center;">{linea_img_tag}</div>
    </div>
    """
  
