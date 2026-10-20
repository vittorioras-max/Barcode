import io
import barcode
from barcode.writer import ImageWriter

def generate_barcode_image(number_str):
    """
    Genera un'immagine di un codice a barre (formato Code 128) 
    in memoria e restituisce i byte dell'immagine PNG.
    """
    try:
        if not number_str or not number_str.strip():
            return None
        
        # Usiamo il Code 128 che è versatile per qualsiasi sequenza numerica o alfanumerica
        Code128 = barcode.get_barcode_class('code128')
        
        # Generiamo il barcode con il writer per immagini (Pillow)
        barcode_instance = Code128(number_str.strip(), writer=ImageWriter())
        
        buffer = io.BytesIO()
        # Salviamo l'immagine nel buffer con il testo leggibile sotto
        barcode_instance.write(buffer, options={'write_text': True, 'dpi': 300, 'font_size': 10, 'text_distance': 5.0})
        buffer.seek(0)
        
        return buffer.getvalue()
    except Exception as e:
        return None
      
