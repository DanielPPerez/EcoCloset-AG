# Conocimientos.py
# Archivo centralizado de la base de conocimientos para EcoCloset AG

# --- COLORIMETRÍA Y ATRIBUTOS PERSONALES ---
TONOS_DE_PIEL = [
    'Marfil', 'Porcelana', 'Marfil Pálido', 'Marfil Cálido', 'Arena', 'Beige Rosado',
    'Beige Neutro', 'Beige', 'Canela', 'Miel', 'Trigueño', 'Almendra',
    'Castaño', 'Bronce', 'Café Oscuro', 'Dorado', 'Expresso'
]

COLORES_DE_OJOS = [
    'Marrón oscuro', 'Marrón café', 'Marrón claro', 'Marrón miel', 'Avellana',
    'Ámbar', 'Verde', 'Verde oliva', 'Verde esmeralda', 'Verde grisáceo',
    'Azul oscuro', 'Azul rey', 'Azul claro', 'Azul grisáceo', 'Azul verdoso',
    'Gris', 'Gris claro', 'Gris oscuro', 'Negro', 'Violeta'
]

COLORES_DE_CABELLO = [
    'Negro azabache', 'Negro natural', 'Castaño oscuro', 'Castaño medio', 'Castaño claro',
    'Castaño ceniza', 'Castaño rojizo (Caoba)', 'Pelirrojo cobrizo', 'Pelirrojo natural', 'Borgoña',
    'Rubio platino', 'Rubio ceniza', 'Rubio dorado', 'Rubio fresa', 'Rubio oscuro',
    'Gris plata', 'Blanco', 'Azul fantasía', 'Rosa fantasía', 'Violeta fantasía'
]

NEUTROS_UNIVERSALES = [
    'Negro', 'Blanco', 'Gris carbón', 'Gris perla', 'Azul marino',
    'Beige', 'Camel', 'Marfil', 'Crema', 'Marrón café', 'Nude'
]

PALETAS_POR_ESTACION = {
    'Invierno': [
        'Negro', 'Blanco óptico', 'Rojo rubí', 'Azul rey', 'Verde esmeralda',
        'Fucsia', 'Magenta', 'Violeta intenso', 'Plata', 'Gris carbón',
        'Azul marino', 'Verde botella', 'Cereza', 'Hielo azul', 'Hielo rosa',
        'Amarillo limón', 'Borgoña', 'Verde pino', 'Azul cobalto', 'Púrpura'
    ],
    'Verano': [
        'Blanco roto', 'Gris perla', 'Azul polvo', 'Lavanda', 'Rosa palo',
        'Menta', 'Frambuesa suave', 'Verde salvia', 'Azul cielo', 'Gris topo',
        'Nude rosado', 'Malva', 'Verde agua', 'Amarillo pastel', 'Azul marino suave',
        'Ciruela suave', 'Cacao', 'Verde jade', 'Orquídea', 'Celeste'
    ],
    'Otoño': [
        'Marrón chocolate', 'Beige', 'Camel', 'Verde oliva', 'Terracota',
        'Mostaza', 'Naranja quemado', 'Dorado', 'Bronce', 'Verde musgo',
        'Marfil', 'Crema', 'Rojo ladrillo', 'Salmón', 'Verde militar',
        'Pimentón', 'Calabaza', 'Ocre', 'Cobre', 'Turquesa oscuro'
    ],
    'Primavera': [
        'Marfil', 'Coral', 'Turquesa', 'Amarillo brillante', 'Verde césped',
        'Azul aciano', 'Melocotón', 'Rojo amapola', 'Dorado claro', 'Camel claro',
        'Verde lima', 'Rosa intenso', 'Salmón brillante', 'Violeta claro', 'Aguamarina',
        'Mandarina', 'Fresa', 'Verde menta brillante', 'Azul cielo brillante', 'Tangerina'
    ]
}

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

# --- ESTILOS Y COMPATIBILIDAD ---
ESTILOS_ROPA = [
    'Casual', 'Clásico', 'Deportivo', 'Elegante', 'Minimalista', 'Bohemio',
    'Romántico', 'Vintage', 'Preppy', 'Streetwear', 'Grunge', 'Rockero',
    'Glam', 'Creativo', 'Smart Casual'
]

REGLAS_COMBINACION_ESTILO = {
    'Casual':       {'Casual': 1.0, 'Deportivo': 0.9, 'Streetwear': 0.9, 'Bohemio': 0.7, 'Minimalista': 0.7, 'Clásico': 0.6, 'Preppy': 0.6},
    'Clásico':      {'Clásico': 1.0, 'Minimalista': 0.9, 'Elegante': 0.9, 'Preppy': 0.8, 'Smart Casual': 0.8, 'Casual': 0.6},
    'Deportivo':    {'Deportivo': 1.0, 'Casual': 0.9, 'Streetwear': 0.8, 'Comfy': 1.0},
    'Elegante':     {'Elegante': 1.0, 'Clásico': 0.9, 'Minimalista': 0.8, 'Romántico': 0.7, 'Glam': 0.8, 'Smart Casual': 0.9},
    'Minimalista':  {'Minimalista': 1.0, 'Clásico': 0.9, 'Elegante': 0.8, 'Casual': 0.7, 'Streetwear': 0.6},
    'Bohemio':      {'Bohemio': 1.0, 'Romántico': 0.8, 'Vintage': 0.7, 'Creativo': 0.7, 'Casual': 0.7},
    'Romántico':    {'Romántico': 1.0, 'Bohemio': 0.8, 'Elegante': 0.7, 'Vintage': 0.6},
    'Vintage':      {'Vintage': 1.0, 'Bohemio': 0.7, 'Creativo': 0.6, 'Romántico': 0.6},
    'Preppy':       {'Preppy': 1.0, 'Clásico': 0.8, 'Smart Casual': 0.7, 'Casual': 0.6},
    'Streetwear':   {'Streetwear': 1.0, 'Casual': 0.9, 'Deportivo': 0.8, 'Grunge': 0.6, 'Creativo': 0.7},
    'Grunge':       {'Grunge': 1.0, 'Rockero': 0.9, 'Streetwear': 0.6, 'Vintage': 0.5},
    'Rockero':      {'Rockero': 1.0, 'Grunge': 0.9, 'Glam': 0.7, 'Streetwear': 0.5},
    'Glam':         {'Glam': 1.0, 'Elegante': 0.8, 'Rockero': 0.7, 'Creativo': 0.6},
    'Creativo':     {'Creativo': 1.0, 'Bohemio': 0.7, 'Streetwear': 0.7, 'Vintage': 0.6, 'Glam': 0.6},
    'Smart Casual': {'Smart Casual': 1.0, 'Clásico': 0.8, 'Elegante': 0.9, 'Minimalista': 0.7, 'Preppy': 0.7},
}

REGLAS_COMBINACION_MATERIAL = {
    'Algodón':   {'Algodón': 1.0, 'Jean': 1.0, 'Lana': 0.8, 'Lino': 0.9, 'Poliéster': 0.7, 'Seda': 0.6, 'Cuero': 0.7, 'Sintético': 0.7},
    'Jean':      {'Jean': 0.8, 'Algodón': 1.0, 'Lana': 0.7, 'Cuero': 0.9, 'Sintético': 0.6, 'Seda': 0.5},
    'Lana':      {'Lana': 0.8, 'Algodón': 0.8, 'Jean': 0.7, 'Seda': 0.9, 'Cuero': 0.8, 'Poliéster': 0.6},
    'Lino':      {'Lino': 1.0, 'Algodón': 0.9, 'Seda': 0.7},
    'Poliéster': {'Poliéster': 0.7, 'Algodón': 0.7, 'Lana': 0.6},
    'Seda':      {'Seda': 0.7, 'Algodón': 0.6, 'Lana': 0.9, 'Cuero': 0.7, 'Jean': 0.5},
    'Cuero':     {'Cuero': 0.7, 'Jean': 0.9, 'Algodón': 0.7, 'Lana': 0.8, 'Seda': 0.7, 'Sintético': 0.6},
    'Sintético': {'Sintético': 0.8, 'Algodón': 0.7, 'Jean': 0.6, 'Poliéster': 0.9},
}

# --- PALETAS Y MAPEOS DE COLORES ---
COLOR_PALETTES = {
    'Neutro': ['Blanco', 'Negro', 'Gris', 'Beige', 'Marrón'],
    'Cálido': ['Rojo', 'Naranja', 'Amarillo', 'Dorado', 'Camel'],
    'Frío': ['Azul', 'Verde', 'Morado', 'Plata']
}

COLOR_MAP = {
    'Marfil': '#F5F5DC', 'Porcelana': '#F2E9E4', 'Marfil Pálido': '#F3EADF', 'Marfil Cálido': '#F5ECCE',
    'Arena': '#E3CBA7', 'Beige Rosado': '#E0C5B6', 'Beige Neutro': '#DDCDBB', 'Beige': '#D8BBA2',
    'Canela': '#C68F6F', 'Miel': '#D4A77E', 'Trigueño': '#B99B83', 'Almendra': '#AD8C76',
    'Castaño': '#8B4513', 'Bronce': '#9C6F44', 'Café Oscuro': '#825A44', 'Dorado': '#B6864B', 'Expresso': '#4B3020',
    'Marrón oscuro': '#4B3020', 'Marrón café': '#6F4E37', 'Marrón claro': '#A0785A', 'Marrón miel': '#C68E17',
    'Avellana': '#9B7653', 'Ámbar': '#FFBF00', 'Verde': '#3A8F53', 'Verde oliva': '#808000', 'Verde esmeralda': '#50C878', 'Verde grisáceo': '#8c9b90',
    'Azul oscuro': '#00008B', 'Azul rey': '#4169E1', 'Azul claro': '#ADD8E6', 'Azul grisáceo': '#6699CC', 'Azul verdoso': '#0d98ba',
    'Gris': '#808080', 'Gris claro': '#D3D3D3', 'Gris oscuro': '#A9A9A9', 'Negro': '#000000', 'Negro azabache': '#0A0A0A',
    'Castaño oscuro': '#3B2A23', 'Castaño medio': '#5C4033', 'Castaño claro': '#795548', 'Castaño ceniza': '#6D615A',
    'Pelirrojo cobrizo': '#B87333', 'Borgoña': '#800020', 'Rubio platino': '#E2DDC7', 'Rubio ceniza': '#C6C1B1',
    'Rubio dorado': '#F0D47D', 'Rubio fresa': '#d4a190', 'Rubio oscuro': '#A89975', 'Blanco': '#FFFFFF', 'Gris plata': '#C0C0C0',
    'Violeta': '#EE82EE', 'Negro natural': '#1C1C1C', 'Castaño rojizo (Caoba)': '#622A22', 'Pelirrojo natural': '#AF4D33',
    'Azul fantasía': '#4D64E4', 'Rosa fantasía': '#E573B7', 'Violeta fantasía': '#A463D8',
    'Blanco óptico': '#FDFFFC', 'Rojo rubí': '#9B111E', 'Fucsia': '#FF00FF', 'Magenta': '#FF00FF',
    'Violeta intenso': '#4F2B9D', 'Plata': '#C0C0C0', 'Gris carbón': '#36454F', 'Azul marino': '#000080',
    'Verde botella': '#006A4E', 'Amarillo limón': '#FFF44F', 'Azul cobalto': '#0047AB', 'Púrpura': '#800080',
    'Blanco roto': '#F8F8F8', 'Gris perla': '#D4D4D4', 'Azul polvo': '#B0C4DE', 'Lavanda': '#E6E6FA',
    'Rosa palo': '#FADADD', 'Menta': '#98FF98', 'Frambuesa suave': '#E30B5D', 'Verde salvia': '#8A9A5B',
    'Azul cielo': '#87CEEB', 'Gris topo': '#483C32', 'Nude rosado': '#E8C7C8', 'Malva': '#E0B0FF', 'Verde agua': '#B0E0E6',
    'Marrón chocolate': '#7B3F00', 'Terracota': '#E2725B', 'Mostaza': '#FFDB58', 'Naranja quemado': '#CC5500',
    'Verde musgo': '#8A9A5B', 'Crema': '#FFFDD0', 'Rojo ladrillo': '#B22222', 'Salmón': '#FA8072', 'Verde militar': '#556B2F',
    'Coral': '#FF7F50', 'Turquesa': '#40E0D0', 'Amarillo brillante': '#FFEA00', 'Verde césped': '#7CFC00',
    'Melocotón': '#FFE5B4', 'Rojo amapola': '#E32636', 'Camel': '#C19A6B', 'Multicolor': '#ABA5A5', 'Sintético': '#808080', 'Cuero': '#8B4513'
}

# --- DESCRIPCIONES DE ESTACIONES ---
DESCRIPCIONES_ESTACIONES = {
    'Invierno': "Tus rasgos (piel, ojos, pelo) tienen un **subtono frío y un alto contraste** entre ellos. Te favorecen los colores intensos, nítidos y audaces.",
    'Verano': "Tus rasgos tienen un **subtono frío, pero un contraste más suave y delicado**. Los colores que mejor te sientan son los empolvados, pasteles y suaves.",
    'Otoño': "Tus rasgos tienen un **subtono cálido y una profundidad terrosa**. Tu paleta ideal se compone de colores ricos, dorados y especiados.",
    'Primavera': "Tus rasgos tienen un **subtono cálido y un alto contraste lleno de brillo**. Los colores que más te iluminan son los vibrantes, claros y alegres."
} 