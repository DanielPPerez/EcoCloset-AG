# colorimetry.py

# --- 1. BASES DE DATOS DE ATRIBUTOS EXPANDIDAS ---

# Lista de tonos de piel adaptada para ser más comprensible en Latinoamérica.
# Se utilizan descriptores comunes en lugar de traducciones literales.
TONOS_DE_PIEL = [
    # Tonos Claros
    'Marfil',           # (Ivory)
    'Porcelana',        # (Porcelain)
    'Marfil Pálido',    # (Pale Ivory)
    'Marfil Cálido',    # (Warm Ivory)
    'Arena',            # (Sand)
    'Beige Rosado',     # (Rose Beige)
    
    # Tonos Medios
    'Beige Neutro',     # (Limestone)
    'Beige',            # (Beige)
    'Canela',           # (Sienna)
    'Miel',             # (Honey)
    'Trigueño',         # (Band - término muy común en LATAM)
    'Almendra',         # (Almond)

    # Tonos Oscuros
    'Castaño',          # (Chestnut)
    'Bronce',           # (Bronze)
    'Café Oscuro',      # (Umber)
    'Dorado',           # (Golden)
    'Expresso'          # (Espresso)
]

# Lista expandida con 20 colores de ojos comunes y sus variaciones.
COLORES_DE_OJOS = [
    'Marrón oscuro', 'Marrón café', 'Marrón claro', 'Marrón miel', 'Avellana', 
    'Ámbar', 'Verde', 'Verde oliva', 'Verde esmeralda', 'Verde grisáceo',
    'Azul oscuro', 'Azul rey', 'Azul claro', 'Azul grisáceo', 'Azul verdoso',
    'Gris', 'Gris claro', 'Gris oscuro', 'Negro', 'Violeta'
]

# Lista expandida con 20 colores de cabello comunes, incluyendo tonos naturales y de fantasía.
COLORES_DE_CABELLO = [
    'Negro azabache', 'Negro natural', 'Castaño oscuro', 'Castaño medio', 'Castaño claro',
    'Castaño ceniza', 'Castaño rojizo (Caoba)', 'Pelirrojo cobrizo', 'Pelirrojo natural', 'Borgoña',
    'Rubio platino', 'Rubio ceniza', 'Rubio dorado', 'Rubio fresa', 'Rubio oscuro',
    'Gris plata', 'Blanco', 'Azul fantasía', 'Rosa fantasía', 'Violeta fantasía'
]

# Lista expandida de colores neutros universales (más de 10).
NEUTROS_UNIVERSALES = [
    'Negro', 'Blanco', 'Gris carbón', 'Gris perla', 'Azul marino', 
    'Beige', 'Camel', 'Marfil', 'Crema', 'Marrón café', 'Nude'
]

# Paletas de colores expandidas para cada estación (más de 20 por estación).
PALETAS_POR_ESTACION = {
    'Invierno': [ # Colores fríos, intensos y de alto contraste
        'Negro', 'Blanco óptico', 'Rojo rubí', 'Azul rey', 'Verde esmeralda', 
        'Fucsia', 'Magenta', 'Violeta intenso', 'Plata', 'Gris carbón', 
        'Azul marino', 'Verde botella', 'Cereza', 'Hielo azul', 'Hielo rosa',
        'Amarillo limón', 'Borgoña', 'Verde pino', 'Azul cobalto', 'Púrpura'
    ],
    'Verano': [ # Colores fríos, suaves y de bajo contraste
        'Blanco roto', 'Gris perla', 'Azul polvo', 'Lavanda', 'Rosa palo', 
        'Menta', 'Frambuesa suave', 'Verde salvia', 'Azul cielo', 'Gris topo',
        'Nude rosado', 'Malva', 'Verde agua', 'Amarillo pastel', 'Azul marino suave',
        'Ciruela suave', 'Cacao', 'Verde jade', 'Orquídea', 'Celeste'
    ],
    'Otoño': [ # Colores cálidos, terrosos y de bajo contraste
        'Marrón chocolate', 'Beige', 'Camel', 'Verde oliva', 'Terracota', 
        'Mostaza', 'Naranja quemado', 'Dorado', 'Bronce', 'Verde musgo',
        'Marfil', 'Crema', 'Rojo ladrillo', 'Salmón', 'Verde militar',
        'Pimentón', 'Calabaza', 'Ocre', 'Cobre', 'Turquesa oscuro'
    ],
    'Primavera': [ # Colores cálidos, brillantes y de alto contraste
        'Marfil', 'Coral', 'Turquesa', 'Amarillo brillante', 'Verde césped', 
        'Azul aciano', 'Melocotón', 'Rojo amapola', 'Dorado claro', 'Camel claro',
        'Verde lima', 'Rosa intenso', 'Salmón brillante', 'Violeta claro', 'Aguamarina',
        'Mandarina', 'Fresa', 'Verde menta brillante', 'Azul cielo brillante', 'Tangerina'
    ]
}


# --- 2. LÓGICA DE ANÁLISIS DE COLORIMETRÍA (MÁS COMPLEJA) ---

# Mapeo de atributos a subtonos (Cálido/Frío) y niveles de contraste (Claro/Oscuro)
# Esta es la "inteligencia" que alimenta la función de determinación.
ATRIBUTOS_DE_COLOR = {
    'piel': {
        'Frío': ['Porcelain', 'Pale Ivory', 'Rose Beige', 'Band', 'Umber'],
        'Cálido': ['Warm Ivory', 'Sand', 'Sienna', 'Honey', 'Golden', 'Chestnut', 'Bronze', 'Espresso'],
        'Neutro': ['Ivory', 'Limestone', 'Beige', 'Almond']
    },
    'cabello': {
        'Claro': ['Rubio platino', 'Rubio ceniza', 'Rubio dorado', 'Rubio fresa', 'Blanco'],
        'Oscuro': ['Negro azabache', 'Negro natural', 'Castaño oscuro', 'Castaño rojizo (Caoba)', 'Borgoña'],
        'Frío': ['Negro azabache', 'Castaño ceniza', 'Rubio platino', 'Rubio ceniza', 'Gris plata', 'Azul fantasía'],
        'Cálido': ['Castaño rojizo (Caoba)', 'Pelirrojo cobrizo', 'Rubio dorado', 'Rubio fresa', 'Castaño medio']
    }
}


def determinar_estacion_colorimetria(tono_piel, color_ojos, color_pelo):
    """
    Determina la estación de colorimetría con una lógica más robusta basada en un sistema de puntuación.
    Analiza el subtono dominante (frío vs. cálido) y el nivel de contraste.

    Args:
        tono_piel (str): El tono de piel del usuario.
        color_ojos (str): El color de ojos del usuario.
        color_pelo (str): El color de pelo del usuario.

    Returns:
        str: La estación de colorimetría sugerida ('Invierno', 'Verano', 'Otoño', 'Primavera').
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
    Construye la paleta de colores final para el usuario, combinando la paleta de su estación,
    los neutros universales y sus colores favoritos personales.

    Args:
        estacion (str): La estación de colorimetría calculada.
        colores_favoritos_usuario (list, optional): Una lista de los colores favoritos del usuario. 
                                                     Defaults to [].

    Returns:
        list: Una lista única de colores recomendados.
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

