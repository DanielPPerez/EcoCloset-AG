# compatibility.py
import pandas as pd
from itertools import product

# --- BASE DE CONOCIMIENTO DE ESTILISMO PROFESIONAL ---

# 1. Lista curada de estilos para la selección del usuario.
# Basada en tu investigación, consolidando y definiendo arquetipos claros.
ESTILOS_ROPA = [
    'Casual',
    'Clásico',
    'Deportivo',
    'Elegante',
    'Minimalista',
    'Bohemio',
    'Romántico',
    'Vintage',
    'Preppy',
    'Streetwear',
    'Grunge',
    'Rockero',
    'Glam',
    'Creativo',
    'Smart Casual'
]

# 2. Matriz de compatibilidad de ESTILOS (Puntuación de 0.0 a 1.0)
# Define qué tan bien se mezclan dos estilos en un mismo atuendo.
# Una puntuación de 0.0 significa que es una combinación inaceptable.
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

# 3. Matriz de compatibilidad de MATERIALES/TEXTURAS
# Fomenta el contraste de texturas (ej. algo liso con algo rugoso).
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

def _get_compatibility_score(reglas, item1, item2):
    """Función auxiliar para obtener la puntuación de compatibilidad de las matrices."""
    score1 = reglas.get(item1, {}).get(item2, 0.0)
    score2 = reglas.get(item2, {}).get(item1, 0.0)
    return max(score1, score2)

def calcular_puntuacion_atuendo(atuendo_df):
    """
    Calcula la puntuación de compatibilidad para un único atuendo (combinación de prendas).
    Devuelve una puntuación de 0.0 a 1.0, donde 1.0 es una combinación perfecta.
    """
    prendas = [row for _, row in atuendo_df.iterrows()]
    if len(prendas) < 2:
        return 0.0

    peso_estilo = 0.70
    peso_material = 0.30
    total_score = 0
    num_comparaciones = 0

    for i in range(len(prendas)):
        for j in range(i + 1, len(prendas)):
            prenda1 = prendas[i]
            prenda2 = prendas[j]
            
            score_estilo = _get_compatibility_score(REGLAS_COMBINACION_ESTILO, prenda1['Estilo'], prenda2['Estilo'])
            score_material = _get_compatibility_score(REGLAS_COMBINACION_MATERIAL, prenda1['Material'], prenda2['Material'])
            
            # Penalización severa si los estilos son incompatibles.
            if score_estilo <= 0.1:
                return 0.0
            
            puntuacion_par = (score_estilo * peso_estilo) + (score_material * peso_material)
            total_score += puntuacion_par
            num_comparaciones += 1

    return total_score / num_comparaciones if num_comparaciones > 0 else 0.0


def calcular_atuendos_ponderados(armario_df: pd.DataFrame) -> float:
    """
    Calcula una puntuación total de "calidad de atuendos" para un armario.
    En lugar de solo contar, suma las puntuaciones de compatibilidad de cada atuendo válido.
    """
    if armario_df.empty:
        return 0.0

    tops = armario_df[armario_df['Tipo'] == 'Top']
    partes_de_abajo = armario_df[armario_df['Tipo'].isin(['Pantalón', 'Falda'])]
    calzados = armario_df[armario_df['Tipo'] == 'Calzado']
    vestidos = armario_df[armario_df['Tipo'] == 'Vestido']
    exteriores = armario_df[armario_df['Tipo'] == 'Exterior']

    puntuacion_total = 0.0

    # 1. Evaluar atuendos básicos (Top + Parte de abajo + Calzado)
    if not (tops.empty or partes_de_abajo.empty or calzados.empty):
        combinaciones_basicas = list(product(tops.iterrows(), partes_de_abajo.iterrows(), calzados.iterrows()))
        for (idx_t, top), (idx_p, p_abajo), (idx_c, calzado) in combinaciones_basicas:
            atuendo_actual_df = pd.DataFrame([top, p_abajo, calzado])
            puntuacion = calcular_puntuacion_atuendo(atuendo_actual_df)
            puntuacion_total += puntuacion

    # 2. Evaluar atuendos de vestido (Vestido + Calzado)
    if not (vestidos.empty or calzados.empty):
        combinaciones_vestido = list(product(vestidos.iterrows(), calzados.iterrows()))
        for (idx_v, vestido), (idx_c, calzado) in combinaciones_vestido:
            atuendo_actual_df = pd.DataFrame([vestido, calzado])
            puntuacion = calcular_puntuacion_atuendo(atuendo_actual_df)
            puntuacion_total += puntuacion
    
    # 3. Factor de prendas exteriores (tercera pieza)
    # Una buena selección de exteriores aumenta exponencialmente el valor del armario.
    if not exteriores.empty:
        # El bonus es mayor si hay variedad de exteriores.
        factor_exterior = 1 + (len(exteriores) * 0.20) + (exteriores['Estilo'].nunique() * 0.10)
        puntuacion_total *= factor_exterior
    
    return puntuacion_total

def encontrar_atuendos_validos(armario_df: pd.DataFrame, umbral_puntuacion=0.6):
    """
    Genera y devuelve una lista de todas las combinaciones de atuendos válidas
    que superen un umbral de puntuación de compatibilidad.
    """
    if armario_df.empty:
        return []

    tops = armario_df[armario_df['Tipo'] == 'Top']
    partes_de_abajo = armario_df[armario_df['Tipo'].isin(['Pantalón', 'Falda'])]
    calzados = armario_df[armario_df['Tipo'] == 'Calzado']
    vestidos = armario_df[armario_df['Tipo'] == 'Vestido']
    exteriores = armario_df[armario_df['Tipo'] == 'Exterior']

    atuendos_finales = []

    # 1. Atuendos básicos
    if not (tops.empty or partes_de_abajo.empty or calzados.empty):
        for (idx_t, top), (idx_p, p_abajo), (idx_c, calzado) in product(tops.iterrows(), partes_de_abajo.iterrows(), calzados.iterrows()):
            atuendo_df = pd.DataFrame([top, p_abajo, calzado])
            if calcular_puntuacion_atuendo(atuendo_df) >= umbral_puntuacion:
                atuendos_finales.append((idx_t, idx_p, idx_c))

    # 2. Atuendos de vestido
    if not (vestidos.empty or calzados.empty):
        for (idx_v, vestido), (idx_c, calzado) in product(vestidos.iterrows(), calzados.iterrows()):
            atuendo_df = pd.DataFrame([vestido, calzado])
            if calcular_puntuacion_atuendo(atuendo_df) >= umbral_puntuacion:
                atuendos_finales.append((idx_v, idx_c))
    
    # 3. Añadir exteriores a los atuendos existentes
    if not exteriores.empty and atuendos_finales:
        atuendos_con_exterior = []
        for atuendo_base in atuendos_finales:
            # Añadir una versión del atuendo base sin exterior
            atuendos_con_exterior.append(atuendo_base)
            # Y luego, crear nuevas combinaciones con cada prenda exterior
            for idx_e, exterior in exteriores.iterrows():
                atuendo_completo_ids = atuendo_base + (idx_e,)
                atuendos_con_exterior.append(atuendo_completo_ids)
        return atuendos_con_exterior
    else:
        return atuendos_finales