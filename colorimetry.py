# colorimetry.py

# Paletas de colores simplificadas para cada estación.
# Estas listas deben coincidir con los valores de la columna 'Color' de tu CSV.
PALETAS_POR_ESTACION = {
    'Invierno': ['Negro', 'Blanco', 'Gris', 'Plata', 'Azul Marino', 'Rojo', 'Fucsia', 'Verde Esmeralda'],
    'Verano': ['Blanco', 'Gris', 'Azul Cielo', 'Lavanda', 'Rosa Palo', 'Menta', 'Beige'],
    'Otoño': ['Marrón', 'Beige', 'Camel', 'Naranja', 'Dorado', 'Verde Oliva', 'Terracota', 'Mostaza'],
    'Primavera': ['Beige', 'Camel', 'Azul Cielo', 'Verde Manzana', 'Coral', 'Amarillo', 'Dorado']
}

# Paleta de colores neutros universal que funciona bien con todas las estaciones
NEUTROS_UNIVERSALES = ['Gris', 'Beige', 'Blanco']

def determinar_estacion_colorimetria(tono_piel, color_ojos, color_pelo):
    """
    Determina la estación de colorimetría basada en reglas simples.
    Esto es una simplificación para el proyecto; los sistemas reales son más complejos.
    """
    # Lógica de decisión simplificada
    if tono_piel in ['Frío (rosado)', 'Oliva']:
        if color_pelo in ['Castaño oscuro', 'Negro']:
            return 'Invierno'
        else: # Castaño claro, Rubio, Pelirrojo
            return 'Verano'
    elif tono_piel in ['Cálido (dorado)', 'Neutro']:
        if color_pelo in ['Castaño oscuro', 'Pelirrojo']:
            return 'Otoño'
        else: # Castaño claro, Rubio, Negro (con matiz cálido)
            return 'Primavera'
    return 'Otoño' # Un default razonable

def obtener_paleta_recomendada(estacion):
    """Devuelve la paleta de colores para una estación dada, incluyendo neutros."""
    if estacion not in PALETAS_POR_ESTACION:
        return []
    
    paleta_base = PALETAS_POR_ESTACION[estacion]
    # Añadir neutros universales para asegurar que siempre haya opciones
    paleta_completa = list(set(paleta_base + NEUTROS_UNIVERSALES))
    return paleta_completa