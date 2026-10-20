import io
import barcode
from barcode.writer import ImageWriter

def generate_barcode_image(number_str):
    """
    Genera un'immagine di un codice a barre (formato Code 128) 
    basso ma ben steso in larghezza.
    """
    try:
        if not number_str or not number_str.strip():
            return None
        
        Code128 = barcode.get_barcode_class('code128')
        barcode_instance = Code128(number_str.strip(), writer=ImageWriter())
        
        buffer = io.BytesIO()
        barcode_instance.write(
            buffer, 
            options={
                'write_text': True, 
                'dpi': 300, 
                'font_size': 8, 
                'text_distance': 2.0,
                'module_height': 8.0,  # Mantiene l'altezza ridotta/bassa
                'module_width': 0.35   # Aumenta la larghezza delle singole barre
            }
        )
        buffer.seek(0)
        
        return buffer.getvalue()
    except Exception as e:
        return None
        
