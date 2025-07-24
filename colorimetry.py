# colorimetry.py

from Conocimientos import TONOS_DE_PIEL, COLORES_DE_OJOS, COLORES_DE_CABELLO, NEUTROS_UNIVERSALES, PALETAS_POR_ESTACION, ATRIBUTOS_DE_COLOR

# --- 2. LÓGICA DE ANÁLISIS DE COLORIMETRÍA (MÁS COMPLEJA) ---

# Mapeo de atributos a subtonos (Cálido/Frío) y niveles de contraste (Claro/Oscuro)
# Esta es la "inteligencia" que alimenta la función de determinación.


# --- FUNCIONES DE COLORIMETRÍA ---

def determinar_estacion_colorimetria(tono_piel, color_ojos, color_pelo):
    """
    Determina la estación de colorimetría del usuario.
    Analiza el subtono dominante (frío/cálido) y el contraste entre piel y cabello.
    Usa ATRIBUTOS_DE_COLOR para puntuar y decide entre Invierno, Verano, Otoño o Primavera.
    """
    puntuacion_calido = 0
    puntuacion_frio = 0

    # 1. Analizar subtono de la piel
    if tono_piel in ATRIBUTOS_DE_COLOR['piel']['Cálido']:
        puntuacion_calido += 2
    elif tono_piel in ATRIBUTOS_DE_COLOR['piel']['Frío']:
        puntuacion_frio += 2
    else: # Neutro
        puntuacion_calido += 1
        puntuacion_frio += 1

    # 2. Analizar subtono del cabello
    if color_pelo in ATRIBUTOS_DE_COLOR['cabello']['Cálido']:
        puntuacion_calido += 1
    elif color_pelo in ATRIBUTOS_DE_COLOR['cabello']['Frío']:
        puntuacion_frio += 1
    
    # 3. Determinar el subtono dominante
    subtono_dominante = 'Cálido' if puntuacion_calido > puntuacion_frio else 'Frío'

    # 4. Determinar el nivel de contraste
    es_pelo_claro = color_pelo in ATRIBUTOS_DE_COLOR['cabello']['Claro']
    es_pelo_oscuro = color_pelo in ATRIBUTOS_DE_COLOR['cabello']['Oscuro']
    
    # El contraste es alto si hay una diferencia clara entre pelo y piel.
    # Por simplicidad, consideramos "oscuro vs. no oscuro" como alto contraste.
    alto_contraste = es_pelo_oscuro and tono_piel not in ['Chestnut', 'Bronze', 'Espresso']

    # 5. Asignar la estación final
    if subtono_dominante == 'Frío':
        return 'Invierno' if alto_contraste else 'Verano'
    else: # subtono_dominante == 'Cálido'
        # La primavera suele tener un contraste más "brillante", el otoño más "suave".
        # Usamos el mismo proxy de contraste claro/oscuro.
        return 'Primavera' if alto_contraste else 'Otoño'


def obtener_paleta_recomendada(estacion, colores_favoritos_usuario=[]):
    """
    Construye la paleta de colores recomendada para el usuario.
    Combina la paleta de la estación, los neutros universales y los colores favoritos del usuario.
    Devuelve una lista única de colores.
    """
    # --- Validación de Entrada ---
    # Si la estación no es válida, devolvemos una paleta segura de neutros y los favoritos del usuario.
    if estacion not in PALETAS_POR_ESTACION:
        # Usamos un set para evitar duplicados automáticamente
        paleta_segura = set(NEUTROS_UNIVERSALES)
        if colores_favoritos_usuario:
            paleta_segura.update(colores_favoritos_usuario)
        return list(paleta_segura)

    # --- Lógica de Construcción de Paleta ---
    
    # 1. Empezar con la base de la estación del usuario.
    paleta_base = set(PALETAS_POR_ESTACION[estacion])
    
    # 2. Añadir siempre los neutros universales, ya que son la base de cualquier armario cápsula.
    paleta_final = paleta_base.union(NEUTROS_UNIVERSALES)
    
    # 3. Integrar los colores favoritos del usuario.
    # La filosofía aquí es que el usuario debe disfrutar de su ropa. Si un color favorito
    # no está en su paleta "ideal", se incluye de todas formas. El objetivo es construir
    # un armario que ame, no uno rígidamente teórico.
    if colores_favoritos_usuario:
        paleta_final.update(colores_favoritos_usuario)
        
    return list(paleta_final)

