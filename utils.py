# utils.py
from PIL import Image
import pillow_avif # Para soportar .avif
import os
import matplotlib.pyplot as plt
from Conocimientos import COLOR_PALETTES

# --- NUEVA FUNCIÓN PARA REESCALAR IMÁGENES GRANDES ---
def reescale_image_if_needed(image_path, max_size=(800, 800), output_folder='imagenes_temp'):
    """
    Reescala la imagen si es más grande que max_size y guarda la versión reescalada en output_folder.
    Devuelve la ruta de la imagen reescalada (o la original si no fue necesario).
    """
    if not os.path.exists(image_path):
        return image_path
    try:
        img = Image.open(image_path)
        if img.width > max_size[0] or img.height > max_size[1]:
            os.makedirs(output_folder, exist_ok=True)
            new_path = os.path.join(output_folder, os.path.basename(image_path))
            img.thumbnail(max_size)
            img.save(new_path)
            return new_path
        else:
            return image_path
    except Exception:
        return image_path


def get_color_category(color):
    """
    Devuelve la categoría de un color (Neutro, Cálido, Frío) según COLOR_PALETTES.
    Si el color no está clasificado, retorna 'Otro'.
    """
    for category, colors in COLOR_PALETTES.items():
        if color in colors:
            return category
    return 'Otro' # Para colores no clasificados como Multicolor

# --- FUNCIONES EXISTENTES (con una pequeña modificación en graficar_evolucion) ---

def crear_mood_board(armario_df, output_path, img_folder='imagenes'):
    """
    Crea un collage (mood board) de imágenes de prendas.
    Si no hay imágenes, genera un placeholder blanco.
    Guarda el resultado en output_path.
    El collage se adapta dinámicamente para mostrar todas las prendas, haciéndose más ancho si es necesario.
    """
    image_paths = [os.path.join(img_folder, fname) for fname in armario_df['Imagen']]
    # Reescalar imágenes si es necesario
    images = [Image.open(reescale_image_if_needed(p)) for p in image_paths if os.path.exists(p)]

    if not images:
        print("No se encontraron imágenes para crear el mood board.")
        # Crear una imagen en blanco como placeholder si no hay imágenes
        placeholder = Image.new('RGB', (200, 200), 'white')
        placeholder.save(output_path)
        return

    num_images = len(images)
    # Permitir hasta 8 columnas para moodboards grandes
    max_cols = 8
    cols = min(max_cols, num_images) if num_images > 0 else 1
    rows = (num_images + cols - 1) // cols if cols > 0 else 1

    # Ajustar el tamaño de las miniaturas según la cantidad de prendas
    if num_images <= 8:
        thumb_width = thumb_height = 200
    elif num_images <= 16:
        thumb_width = thumb_height = 150
    elif num_images <= 32:
        thumb_width = thumb_height = 100
    else:
        thumb_width = thumb_height = 80

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
    Grafica la evolución del mejor fitness por generación.
    Devuelve el objeto figure de Matplotlib para su uso en Streamlit.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(historial)
    ax.set_title('Evolución del Mejor Fitness por Generación')
    ax.set_xlabel('Generación')
    ax.set_ylabel('Mejor Fitness')
    ax.grid(True)
    return fig