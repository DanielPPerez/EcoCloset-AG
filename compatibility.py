# compatibility.py
import pandas as pd
from itertools import product
from Conocimientos import ESTILOS_ROPA, REGLAS_COMBINACION_ESTILO, REGLAS_COMBINACION_MATERIAL


def _get_compatibility_score(reglas, item1, item2):
    """
    Devuelve la puntuación de compatibilidad entre dos elementos según la matriz dada.
    Busca en ambas direcciones para asegurar simetría.
    """
    score1 = reglas.get(item1, {}).get(item2, 0.0)
    score2 = reglas.get(item2, {}).get(item1, 0.0)
    return max(score1, score2)

def calcular_puntuacion_atuendo(atuendo_df):
    """
    Calcula la puntuación de compatibilidad de un atuendo (conjunto de prendas).
    Considera tanto el estilo como el material de las prendas.
    Penaliza severamente si los estilos son incompatibles.
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
    Calcula la puntuación total de calidad de atuendos para un armario.
    Suma las puntuaciones de compatibilidad de cada atuendo válido.
    Considera bonus por variedad de exteriores.
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
    Genera todas las combinaciones de atuendos válidas que superen un umbral de compatibilidad.
    Incluye combinaciones con y sin prendas exteriores.
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