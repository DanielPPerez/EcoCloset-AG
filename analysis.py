# analysis.py
import pandas as pd

def analizar_prenda_mvp(armario_df: pd.DataFrame):
    """
    Analiza un DataFrame de un armario y encuentra la prenda más valiosa (MVP).
    El valor se mide por la cantidad de atuendos que la prenda ayuda a formar.

    Args:
        armario_df (pd.DataFrame): El DataFrame con las prendas del armario seleccionado.

    Returns:
        dict: Un diccionario con la información de la prenda MVP y sus estadísticas.
    """
    if armario_df.empty:
        return None

    # Contar los tipos de prendas en el armario
    tops = armario_df[armario_df['Tipo'] == 'Top']
    pantalones_faldas = armario_df[armario_df['Tipo'].isin(['Pantalón', 'Falda'])]
    calzados = armario_df[armario_df['Tipo'] == 'Calzado']
    exteriores = armario_df[armario_df['Tipo'] == 'Exterior']
    vestidos = armario_df[armario_df['Tipo'] == 'Vestido']

    # Asignar un "poder de combinación" a cada prenda
    poder_combinacion = []

    for index, prenda in armario_df.iterrows():
        tipo = prenda['Tipo']
        score = 0
        if tipo == 'Top':
            # Un top combina con todas las partes de abajo y todos los zapatos.
            # Los exteriores son un extra.
            score = len(pantalones_faldas) * len(calzados) * (1 + len(exteriores))
        elif tipo in ['Pantalón', 'Falda']:
            # Una parte de abajo combina con todos los tops y zapatos.
            score = len(tops) * len(calzados) * (1 + len(exteriores))
        elif tipo == 'Calzado':
            # Los zapatos combinan con atuendos básicos y atuendos de vestido.
            atuendos_con_pantalones = len(tops) * len(pantalones_faldas)
            atuendos_con_vestidos = len(vestidos)
            score = atuendos_con_pantalones + atuendos_con_vestidos
        elif tipo == 'Vestido':
            # Un vestido combina con todos los zapatos y exteriores.
            score = len(calzados) * (1 + len(exteriores))
        elif tipo == 'Exterior':
            # Un exterior combina con atuendos básicos y atuendos de vestido.
            atuendos_con_pantalones = len(tops) * len(pantalones_faldas) * len(calzados)
            atuendos_con_vestidos = len(vestidos) * len(calzados)
            score = atuendos_con_pantalones + atuendos_con_vestidos
        
        poder_combinacion.append(score)

    armario_df['Poder_Combinacion'] = poder_combinacion
    
    # Encontrar la prenda con el score más alto
    prenda_mvp = armario_df.loc[armario_df['Poder_Combinacion'].idxmax()]

    return {
        'nombre': prenda_mvp['Nombre'],
        'tipo': prenda_mvp['Tipo'],
        'color': prenda_mvp['Color'],
        'estilo': prenda_mvp['Estilo'],
        'combinaciones': prenda_mvp['Poder_Combinacion'],
        'df_completo': armario_df[['Nombre', 'Tipo', 'Poder_Combinacion']].sort_values(by='Poder_Combinacion', ascending=False)
    }