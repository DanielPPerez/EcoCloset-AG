# utils.py
from PIL import Image
import pillow_avif # Para soportar .avif
import os
import matplotlib.pyplot as plt

# --- NUEVA LÓGICA DE COLORES ---
# Mapeo simple de colores a paletas. Puedes expandir esto.
# Los colores en el CSV deben coincidir con estas claves.
COLOR_PALETTES = {
    'Neutro': ['Blanco', 'Negro', 'Gris', 'Beige', 'Marrón'],
    'Cálido': ['Rojo', 'Naranja', 'Amarillo', 'Dorado', 'Camel'],
    'Frío': ['Azul', 'Verde', 'Morado', 'Plata']
}

def get_color_category(color):
    """Devuelve la categoría de un color (Neutro, Cálido, Frío)."""
    for category, colors in COLOR_PALETTES.items():
        if color in colors:
            return category
    return 'Otro' # Para colores no clasificados como Multicolor

# --- FUNCIONES EXISTENTES (con una pequeña modificación en graficar_evolucion) ---

def crear_mood_board(armario_df, output_path, img_folder='imagenes'):
    # (El código de esta función se mantiene igual que antes)
    image_paths = [os.path.join(img_folder, fname) for fname in armario_df['Imagen']]
    images = [Image.open(p) for p in image_paths if os.path.exists(p)]

    if not images:
        print("No se encontraron imágenes para crear el mood board.")
        # Crear una imagen en blanco como placeholder si no hay imágenes
        placeholder = Image.new('RGB', (200, 200), 'white')
        placeholder.save(output_path)
        return

    num_images = len(images)
    cols = int(num_images**0.5) if num_images > 0 else 1
    rows = (num_images + cols - 1) // cols if cols > 0 else 1
    
    thumb_width = 200
    thumb_height = 200
    
    collage_width = cols * thumb_width
    collage_height = rows * thumb_height
    collage = Image.new('RGB', (collage_width, collage_height), 'white')

    for i, img in enumerate(images):
        img.thumbnail((thumb_width, thumb_height))
        x = (i % cols) * thumb_width
        y = (i // cols) * thumb_height
        collage.paste(img, (x, y))

    collage.save(output_path)
    print(f"Mood board guardado en: {output_path}")


def graficar_evolucion_fitness(historial):
    """
    MODIFICADO: Devuelve el objeto 'figure' de Matplotlib para usarlo en Streamlit.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(historial)
    ax.set_title('Evolución del Mejor Fitness por Generación')
    ax.set_xlabel('Generación')
    ax.set_ylabel('Mejor Fitness')
    ax.grid(True)
    return fig