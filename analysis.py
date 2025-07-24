# analysis.py
import pandas as pd

def analizar_prenda_mvp(armario_df: pd.DataFrame, lista_de_atuendos_validos: list):
    """
    Analiza un armario para encontrar la prenda más valiosa (MVP) basándose
    en la cantidad de atuendos VÁLIDOS y estilísticamente coherentes en los que participa.

    Args:
        armario_df (pd.DataFrame): El DataFrame con las prendas del armario seleccionado.
        lista_de_atuendos_validos (list): La lista de tuplas con los IDs de los atuendos válidos.

    Returns:
        dict: Un diccionario con la información de la prenda MVP y sus estadísticas.
    """
    if armario_df.empty or not lista_de_atuendos_validos:
        return None

    # Crear un diccionario para contar la participación de cada prenda
    # La clave es el ID de la prenda, el valor es su conteo.
    conteo_de_participacion = {prenda_id: 0 for prenda_id in armario_df.index}

    # Iterar sobre cada atuendo válido y sumar 1 a cada prenda que lo compone
    for atuendo in lista_de_atuendos_validos:
        for prenda_id in atuendo:
            if prenda_id in conteo_de_participacion:
                conteo_de_participacion[prenda_id] += 1
    
    # Crear un DataFrame con los resultados para un manejo más fácil
    df_versatilidad = pd.DataFrame(
        list(conteo_de_participacion.items()), 
        columns=['ID', 'Poder_Combinacion_Real']
    ).set_index('ID')

    # Unir esta información con los nombres y tipos de las prendas
    ranking_completo_df = armario_df.join(df_versatilidad)

    # Si hay prendas sin combinaciones (valor NaN), rellenar con 0
    ranking_completo_df['Poder_Combinacion_Real'].fillna(0, inplace=True)
    ranking_completo_df['Poder_Combinacion_Real'] = ranking_completo_df['Poder_Combinacion_Real'].astype(int)

    # Encontrar la prenda con el score más alto
    if ranking_completo_df.empty or ranking_completo_df['Poder_Combinacion_Real'].sum() == 0:
        return None # No hay MVP si no hay combinaciones
        
    prenda_mvp = ranking_completo_df.loc[ranking_completo_df['Poder_Combinacion_Real'].idxmax()]

    return {
        'nombre': prenda_mvp['Nombre'],
        'tipo': prenda_mvp['Tipo'],
        'color': prenda_mvp['Color'],
        'estilo': prenda_mvp['Estilo'],
        'combinaciones': prenda_mvp['Poder_Combinacion_Real'],
        'df_completo': ranking_completo_df[['Nombre', 'Tipo', 'Poder_Combinacion_Real']].sort_values(
            by='Poder_Combinacion_Real', ascending=False
        )
    }