# outfit_visualizer.py
import os
from PIL import Image, ImageDraw, ImageFont
import rembg
from utils import reescale_image_if_needed

# Definir carpetas para las imágenes procesadas
IMG_FOLDER = 'imagenes'
TRANSPARENT_FOLDER = 'imagenes_transparentes'
OUTFIT_FOLDER = 'outfits_generados'

# Crear las carpetas si no existen
os.makedirs(TRANSPARENT_FOLDER, exist_ok=True)
os.makedirs(OUTFIT_FOLDER, exist_ok=True)

def remove_background(image_name):
    """
    Quita el fondo de una imagen y la guarda en la carpeta de transparentes.
    Si ya existe, simplemente devuelve la ruta.
    """
    original_path = os.path.join(IMG_FOLDER, image_name)
    transparent_path = os.path.join(TRANSPARENT_FOLDER, image_name)

    if os.path.exists(transparent_path):
        return transparent_path
    
    if not os.path.exists(original_path):
        return None

    try:
        with open(original_path, 'rb') as i:
            with open(transparent_path, 'wb') as o:
                input_data = i.read()
                output_data = rembg.remove(input_data)
                o.write(output_data)
        return transparent_path
    except Exception:
        return None

def create_outfit_image(outfit_prendas, outfit_filename):
    """
    Crea una imagen compuesta de un atuendo, apilando las prendas verticalmente.
    """
    # Orden de visualización: Exterior > Top/Vestido > Pantalón/Falda > Calzado
    layer_order = {'Exterior': 0, 'Top': 1, 'Vestido': 1, 'Pantalón': 2, 'Falda': 2, 'Calzado': 3}
    prendas_ordenadas = sorted(
        [row for _, row in outfit_prendas.iterrows()],
        key=lambda p: layer_order.get(p['Tipo'], 99)
    )

    num_items = len(prendas_ordenadas)
    if num_items == 0:
        return None
    
    # Ajustar el tamaño del lienzo según el número de prendas
    canvas_width = 350
    slot_height = 200 # Altura para cada prenda
    canvas_height = num_items * slot_height
    
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (240, 242, 246, 255))
    draw = ImageDraw.Draw(canvas)
    
    try:
        # Usar una fuente por defecto si está disponible, si no, usar la de PIL
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default(size=20)

    for i, prenda in enumerate(prendas_ordenadas):
        img_path = remove_background(prenda['Imagen'])
        if not img_path:
            continue

        # Reescalar la imagen si es muy grande
        img_path = reescale_image_if_needed(img_path)
        try:
            img = Image.open(img_path)
            
            # Redimensionar la imagen para que quepa en su "slot"
            img.thumbnail((canvas_width - 50, slot_height - 60))
            
            # Calcular la posición para centrar la imagen en su slot vertical
            y_slot_start = i * slot_height
            x_center = canvas_width // 2
            y_center = y_slot_start + (slot_height // 2)

            paste_x = x_center - (img.width // 2)
            paste_y = y_center - (img.height // 2) - 10 # Un poco más arriba para dejar espacio al texto
            
            # Dibujar la etiqueta del tipo de prenda
            bbox = draw.textbbox((0, 0), prenda['Tipo'], font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text(
                (x_center - (text_width // 2), y_center + (slot_height // 2) - 40), 
                prenda['Tipo'], 
                font=font, 
                fill=(50, 50, 50)
            )
            
            # Pegar la imagen de la prenda
            canvas.paste(img, (paste_x, paste_y), img)

        except Exception as e:
            print(f"Error al procesar la prenda {prenda['Nombre']}: {e}")

    output_path = os.path.join(OUTFIT_FOLDER, outfit_filename)
    canvas.save(output_path, 'PNG')
    return output_path