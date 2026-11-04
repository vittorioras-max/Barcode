# --- print_utils.py ---
import re


def get_print_styles():
    return """
    <style>
    .top-main-header { text-align:center; padding-bottom:10px; border-bottom:2px solid #444; width:100%; margin-bottom:10px; }
    .top-main-title { font-size:34px; font-weight:bold; margin-bottom:6px; }
    .stat77-label { font-weight:bold; font-size:22px; letter-spacing:2px; margin-bottom:4px; }
    .stat77-header-block { text-align:center; margin-top:4px; }
    .stat77-header-block img { max-height:38px; width:auto; }

    .print-card { padding:8px 10px; border:1.5px solid #ccc; border-radius:6px; }
    .print-card-title, .info-line, .line-code-highlight, .top-main-title, .stat77-label { color:black !important; }
    .info-line { font-size:13px; margin-bottom:3px; }
    .line-code-highlight { font-weight:bold; color:#4f46e5; }
    .line-barcode { max-height:45px; width:auto; margin-top:2px; }

    .print-table { width:100%; border-collapse:collapse; border:none; }
    .print-table td { border:none; padding:0 0 8px 0; }
    /* a video l'header è già in cima alla pagina: nascondo quello della tabella */
    .print-table thead { display:none; }

    @media print {
        @page { size:A4; margin:10mm; }

        body { background:white !important; color:black !important; }

        [data-testid="stSidebar"], [data-testid="stHeader"], header, footer {
            display:none !important;
        }

        /* nasconde TUTTI i blocchi Streamlit tranne quello con la tabella:
           elimina lo spazio vuoto in cima */
        [data-testid="stElementContainer"]:not(:has(.print-table)),
        [data-testid="element-container"]:not(:has(.print-table)) {
            display:none !important;
        }
        [data-testid="stVerticalBlock"] { gap:0 !important; }
        .block-container, [data-testid="stMainBlockContainer"] { padding-top:0 !important; }

        .print-table thead { display:table-header-group !important; }
        .print-table tr { break-inside:avoid; page-break-inside:avoid; }

        .print-card { background:white !important; border:1.5px solid #999 !important; }
        .print-card-title, .info-line, .line-code-highlight, .top-main-title { color:black !important; }
    }
    </style>
    """


def _flat(html):
    # Streamlit/markdown rompe l'HTML con righe indentate o vuote
    return re.sub(r"\n\s*", "", html)


def _header_inner(stat77_img_tag):
    stat = ""
    if stat77_img_tag:
        stat = f"""<div class="stat77-header-block">
    <div class="stat77-label">STAT77</div>
    {stat77_img_tag}</div>"""
    return f"""<div class="top-main-header">
        <div class="top-main-title">🚛 Generatore Barcode</div>{stat}</div>"""


def render_stat77_header(stat77_img_tag):
    """Header singolo, usato a video (e in Modalità 1)."""
    return _flat(_header_inner(stat77_img_tag))


def render_logistics_card(citta_val, info_str, linea_val, linea_img_tag):
    return _flat(f"""
    <div class="print-card">
        <div class="print-card-title">Destinazione: {citta_val}</div>
        <div class="info-line">{info_str}<b>Linea:</b> <span class="line-code-highlight">{linea_val}</span></div>
        <div style="text-align:center;">{linea_img_tag}</div>
    </div>""")


def render_print_table(stat77_img_tag, cards):
    """Tabella unica: thead (ripetuto a ogni pagina) + una riga per card."""
    rows = "".join(f"<tr><td>{c}</td></tr>" for c in cards)
    return _flat(f"""
    <table class="print-table">
        <thead><tr><td>{_header_inner(stat77_img_tag)}</td></tr></thead>
        <tbody>{rows}</tbody>
    </table>""")
    
