import streamlit as st
import pandas as pd
import os
import numpy as np

# --- IMPORTACIONES ACTUALIZADAS ---
from colorimetry import (
    determinar_estacion_colorimetria,
    obtener_paleta_recomendada,
    TONOS_DE_PIEL,
    COLORES_DE_OJOS,
    COLORES_DE_CABELLO,
    PALETAS_POR_ESTACION
)
from compatibility import ESTILOS_ROPA
from genetic_algorithm import EcoClosetAG
from utils import crear_mood_board, graficar_evolucion_fitness
from analysis import analizar_prenda_mvp
from outfit_visualizer import create_outfit_image

# --- CONFIGURACIÓN Y FUNCIONES AUXILIARES ---
st.set_page_config(layout="wide", page_title="EcoCloset AG")

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

def color_swatch_html(color_name):
    hex_code = COLOR_MAP.get(color_name, '#FFFFFF')
    border_color = '#333333' if hex_code == '#FFFFFF' else 'transparent'
    return f'<div style="width:20px; height:20px; background-color:{hex_code}; border:1px solid {border_color}; border-radius:50%; display:inline-block; vertical-align:middle; margin-left:10px;"></div>'

DESCRIPCIONES_ESTACIONES = {
    'Invierno': "Tus rasgos (piel, ojos, pelo) tienen un **subtono frío y un alto contraste** entre ellos. Te favorecen los colores intensos, nítidos y audaces.",
    'Verano': "Tus rasgos tienen un **subtono frío, pero un contraste más suave y delicado**. Los colores que mejor te sientan son los empolvados, pasteles y suaves.",
    'Otoño': "Tus rasgos tienen un **subtono cálido y una profundidad terrosa**. Tu paleta ideal se compone de colores ricos, dorados y especiados.",
    'Primavera': "Tus rasgos tienen un **subtono cálido y un alto contraste lleno de brillo**. Los colores que más te iluminan son los vibrantes, claros y alegres."
}

# --- ESTADO DE LA SESIÓN ---
if 'resultados' not in st.session_state: st.session_state.resultados = None
if 'historial_fitness' not in st.session_state: st.session_state.historial_fitness = None
if 'catalogo_completo' not in st.session_state: st.session_state.catalogo_completo = None
if 'outfit_index' not in st.session_state: st.session_state.outfit_index = 0
if 'prenda_seleccionada' not in st.session_state: st.session_state.prenda_seleccionada = None

# --- INTERFAZ PRINCIPAL ---
st.title("🌿 EcoCloset AG")
st.markdown("Un sistema inteligente para construir un armario cápsula optimizado, enfocado en tu **estilo personal**, la **versatilidad** y el **consumo consciente**.")

with st.sidebar:
    st.header("1. Carga tu Catálogo")
    uploaded_file = st.file_uploader("Sube tu archivo `prendas.csv`", type=["csv"])
    
    if not os.path.exists('moodboards_temp'): os.makedirs('moodboards_temp')

    if uploaded_file is not None:
        if st.session_state.catalogo_completo is None:
             st.session_state.catalogo_completo = pd.read_csv(uploaded_file)
    
    if st.session_state.catalogo_completo is not None:
        catalogo_completo = st.session_state.catalogo_completo
        
        required_cols = ['Nombre', 'Tipo', 'Color', 'Estilo', 'Temporada', 'Imagen', 'Sostenibilidad', 'Material']
        if not all(col in catalogo_completo.columns for col in required_cols):
            st.error(f"Error: El CSV debe contener las columnas: {', '.join(required_cols)}")
            st.session_state.catalogo_completo = None
        else:
            st.success("¡Catálogo cargado con éxito!")
            
            st.header("2. Tus Preferencias de Estilo")
            tam_armario = st.slider("Tamaño del armario cápsula:", 5, 50, 20, help="Define el número total de prendas que deseas.")
            st.markdown("**¿Cuáles son tus 5 estilos principales?**")
            estilos_preferidos = st.multiselect("Selecciona hasta 5 estilos que te representen:", options=ESTILOS_ROPA, max_selections=5, default=['Casual', 'Clásico', 'Minimalista'])
            preferencias_usuario = {}
            if estilos_preferidos:
                st.markdown("**Del 1 al 10, ¿qué tanto usas cada estilo?**")
                for estilo in estilos_preferidos:
                    puntuacion = st.slider(f"Puntuación para '{estilo}':", 1, 10, 5)
                    preferencias_usuario[estilo] = puntuacion

            st.header("3. Tus Imprescindibles")
            prendas_obligatorias_nombres = st.multiselect("Prendas que DEBEN estar en el armario:", options=catalogo_completo['Nombre'].tolist())
            prendas_obligatorias_idx = catalogo_completo[catalogo_completo['Nombre'].isin(prendas_obligatorias_nombres)].index.tolist()

            st.header("4. Tu Perfil de Colorimetría")
            col1, col2 = st.columns([0.8, 0.2])
            with col1: tono_piel = st.selectbox("Tu tono de piel:", TONOS_DE_PIEL)
            with col2: st.markdown(color_swatch_html(tono_piel), unsafe_allow_html=True)
            col1, col2 = st.columns([0.8, 0.2])
            with col1: color_ojos = st.selectbox("Tu color de ojos:", COLORES_DE_OJOS)
            with col2: st.markdown(color_swatch_html(color_ojos), unsafe_allow_html=True)
            col1, col2 = st.columns([0.8, 0.2])
            with col1: color_pelo = st.selectbox("Tu color de pelo:", COLORES_DE_CABELLO)
            with col2: st.markdown(color_swatch_html(color_pelo), unsafe_allow_html=True)
            todos_los_colores = sorted(list(set(catalogo_completo['Color'].unique())))
            colores_favoritos_usuario = st.multiselect("Tus colores favoritos:", todos_los_colores)
            if colores_favoritos_usuario:
                swatches_html = " ".join([color_swatch_html(c) for c in colores_favoritos_usuario])
                st.markdown(swatches_html, unsafe_allow_html=True)

            estacion_usuario = determinar_estacion_colorimetria(tono_piel, color_ojos, color_pelo)
            with st.container(border=True):
                st.subheader(f"Estación sugerida: {estacion_usuario}")
                st.markdown(DESCRIPCIONES_ESTACIONES.get(estacion_usuario, ""))
                st.markdown("**Paleta de colores clave:**")
                colores_estacion = PALETAS_POR_ESTACION.get(estacion_usuario, [])
                cols = st.columns(5)
                for i, color in enumerate(colores_estacion[:10]):
                    with cols[i % 5]:
                        st.markdown(f"{color_swatch_html(color)} {color}", unsafe_allow_html=True)
            
            if st.button("✨ ¡Optimizar mi Armario!", type="primary", use_container_width=True):
                if len(prendas_obligatorias_idx) > tam_armario:
                    st.error("Error: Has seleccionado más prendas imprescindibles que el tamaño total del armario.")
                else:
                    with st.spinner('El algoritmo genético está buscando...'):
                        progress_bar = st.progress(0, text="Iniciando optimización...")
                        user_inputs = {'tam_armario': tam_armario, 'preferencias_estilo': preferencias_usuario, 'prendas_obligatorias_idx': prendas_obligatorias_idx, 'estacion_colorimetria': estacion_usuario, 'colores_favoritos': colores_favoritos_usuario}
                        ag = EcoClosetAG(catalogo_df=catalogo_completo, user_inputs=user_inputs)
                        mejores_armarios, historial_fitness = ag.ejecutar(streamlit_callback=lambda p, m: progress_bar.progress(p, text=m))
                        st.session_state.resultados = mejores_armarios
                        st.session_state.historial_fitness = historial_fitness
                    st.success("¡Optimización completada!")

st.header("🏆 Tus 3 Mejores Armarios Cápsula")
if st.session_state.resultados is None:
    st.info("👋 ¡Bienvenido! Configura tus preferencias en el panel de la izquierda y haz clic en 'Optimizar' para ver la magia.")
else:
    catalogo_completo = st.session_state.catalogo_completo
    num_resultados = len(st.session_state.resultados)
    cols = st.columns(num_resultados) if num_resultados > 0 else []
    
    for i, armario_data in enumerate(st.session_state.resultados):
        with cols[i]:
            st.subheader(f"Armario Propuesto #{i+1}")
            individuo_ids = armario_data['individuo']
            armario_df = catalogo_completo.iloc[individuo_ids]
            moodboard_path = f'moodboards_temp/armario_{i+1}.png'
            crear_mood_board(armario_df, moodboard_path, img_folder='imagenes')
            st.image(moodboard_path, caption=f"Mood board del Armario #{i+1}")
            st.metric("Puntuación Fitness", f"{armario_data['fitness']:.4f}")
            st.metric("Puntuación de Atuendos", f"{armario_data['atuendos']:.2f}", help="Puntuación de la calidad y compatibilidad de los atuendos posibles (más alto es mejor).")
            st.metric("Sostenibilidad Promedio", f"{armario_data['sostenibilidad_score']:.2f} / 5.0")
            with st.expander("Ver lista de prendas"):
                st.dataframe(armario_df[['Nombre', 'Tipo', 'Color', 'Estilo', 'Temporada', 'Sostenibilidad', 'Material']])

    if st.session_state.historial_fitness:
        st.header("📈 Evolución del Fitness")
        fig = graficar_evolucion_fitness(st.session_state.historial_fitness)
        st.pyplot(fig)

    if st.session_state.resultados and 'combinaciones_lista' in st.session_state.resultados[0]:
        st.divider()
        # --- SECCIÓN DE ANÁLISIS PROFUNDO CORREGIDA ---
        st.header("🔍 Análisis Profundo del Mejor Armario")
        st.markdown("Análisis detallado del **Armario Propuesto #1**, la mejor solución encontrada por el algoritmo.")
        
        mejor_armario_data = st.session_state.resultados[0]
        mejor_armario_ids = mejor_armario_data['individuo']
        mejor_armario_df = st.session_state.catalogo_completo.iloc[mejor_armario_ids]
        lista_atuendos_validos = mejor_armario_data.get('combinaciones_lista', [])
        
        # Llamar a la nueva función de análisis con la lista de atuendos
        analisis_mvp = analizar_prenda_mvp(mejor_armario_df, lista_atuendos_validos)
        
        if analisis_mvp:
            st.subheader("🏆 Prenda Más Valiosa (MVP)")
            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader(f"{analisis_mvp['nombre']}")
                st.write(f"**Tipo:** {analisis_mvp['tipo']}")
            with c2:
                # El número ahora es coherente con el explorador de atuendos
                st.metric("Combinaciones Válidas", f"{int(analisis_mvp['combinaciones']):,}")

            with st.expander("Ver ranking de versatilidad de todas las prendas"):
                # Renombrar la columna para mayor claridad en la UI
                df_ranking = analisis_mvp['df_completo'].rename(
                    columns={'Poder_Combinacion_Real': 'Combinaciones Válidas'}
                )
                st.dataframe(df_ranking[['Nombre', 'Tipo', 'Combinaciones Válidas']])
        
        # --- EXPLORADOR DE ATUENDOS (sin cambios, ya debería funcionar) ---
        st.divider()
        st.header("👗 Explorador de Atuendos")
        st.markdown("Selecciona una prenda para visualizar todas sus combinaciones posibles.")
        
        prenda_seleccionada_nombre = st.selectbox("Elige una prenda para explorar:", options=mejor_armario_df['Nombre'].tolist(), key="selector_prenda")

        if prenda_seleccionada_nombre:
            if st.session_state.prenda_seleccionada != prenda_seleccionada_nombre:
                st.session_state.prenda_seleccionada = prenda_seleccionada_nombre
                st.session_state.outfit_index = 0

            prenda_seleccionada_id = mejor_armario_df[mejor_armario_df['Nombre'] == prenda_seleccionada_nombre].index[0]
            atuendos_filtrados = [outfit for outfit in lista_atuendos_validos if prenda_seleccionada_id in outfit]
            
            num_atuendos = len(atuendos_filtrados)
            st.info(f"Se encontraron **{num_atuendos}** combinaciones para **{prenda_seleccionada_nombre}**.")

            if num_atuendos > 0:
                col1, col2, col3 = st.columns([1, 4, 1])
                with col1:
                    if st.button("⬅️ Anterior", use_container_width=True):
                        st.session_state.outfit_index = (st.session_state.outfit_index - 1) % num_atuendos
                with col3:
                    if st.button("Siguiente ➡️", use_container_width=True):
                        st.session_state.outfit_index = (st.session_state.outfit_index + 1) % num_atuendos

                with col2:
                    with st.container(border=True):
                        st.markdown(f"<p style='text-align: center; font-weight: bold;'>Atuendo {st.session_state.outfit_index + 1} / {num_atuendos}</p>", unsafe_allow_html=True)
                        outfit_actual_ids = atuendos_filtrados[st.session_state.outfit_index]
                        outfit_actual_df = st.session_state.catalogo_completo.loc[list(outfit_actual_ids)]
                        outfit_filename = f"outfit_{st.session_state.outfit_index}_{prenda_seleccionada_id}.png"
                        
                        with st.spinner("Creando visualización del atuendo..."):
                            imagen_atuendo_path = create_outfit_image(outfit_actual_df, outfit_filename)
                        
                        if imagen_atuendo_path:
                            st.image(imagen_atuendo_path, use_column_width=True)
                            for _, prenda in outfit_actual_df.iterrows():
                                st.markdown(f"- **{prenda['Tipo']}:** {prenda['Nombre']}")
                        else:
                            st.error("No se pudo generar la imagen del atuendo.")