    # Funzione per generare il Code 128 in base64 (con altezza dimezzata)
    def generate_barcode_base64(value):
        if not value or str(value).strip() == "" or str(value).strip().lower() == "nan":
            return None
        try:
            CODE128 = barcode.get_barcode_class('code128')
            rv = io.BytesIO()
            val_str = str(value).split('.')[0].strip()
            code = CODE128(val_str, writer=ImageWriter())
            # Altezza ridotta a 5.0 (metà rispetto a prima)
            code.write(rv, options={"module_height": 5.0, "font_size": 10, "text_distance": 3.0, "quiet_zone": 2.0})
            return base64.b64encode(rv.getvalue()).decode("utf-8")
        except Exception as e:
            return None
            
