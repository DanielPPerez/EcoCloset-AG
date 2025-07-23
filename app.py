# app.py
import numpy as np
import streamlit as st
import pandas as pd
import os
from database import cargar_catalogo
from genetic_algorithm import EcoClosetAG
from utils import crear_mood_board, graficar_evolucion_fitness
from analysis import analizar_prenda_mvp  # Nuevo import
from colorimetry import determinar_estacion_colorimetria  # Nuevo import

# --- Configuración de la página de Streamlit ---
st.set_page_config(layout="wide", page_title="EcoCloset AG")

# --- Estado de la sesión para mantener los datos ---
if 'resultados' not in st.session_state:
    st.session_state.resultados = None
if 'historial_fitness' not in st.session_state:
    st.session_state.historial_fitness = None
if 'catalogo_completo' not in st.session_state:
    st.session_state.catalogo_completo = None

# --- Interfaz Principal ---
st.title("🌿 EcoCloset AG")
st.markdown("Un sistema inteligente para construir un armario cápsula optimizado mediante **Algoritmos Genéticos**.")

# --- Barra Lateral (Sidebar) para Entradas del Usuario ---
with st.sidebar:
    st.header("1. Carga tu Catálogo")
    uploaded_file = st.file_uploader("Sube tu archivo `prendas.csv`", type=["csv"])
    
    # Crear carpeta temporal para moodboards si no existe
    if not os.path.exists('moodboards_temp'):
        os.makedirs('moodboards_temp')

    if uploaded_file is not None:
        # Guardar en el estado de la sesión para persistencia
        if st.session_state.catalogo_completo is None:
             st.session_state.catalogo_completo = pd.read_csv(uploaded_file)
        
    if st.session_state.catalogo_completo is not None:
        catalogo_completo = st.session_state.catalogo_completo
        st.success("¡Catálogo cargado con éxito!")
        
        st.header("2. Define tus Preferencias")
        
        tam_armario = st.slider(
            "Número de prendas en el armario cápsula:", 
            min_value=5, max_value=50, value=20, step=1
        )
        
        st.markdown("**Distribución de necesidades por contexto:**")
        col1, col2 = st.columns(2)
        ctx_oficina = col1.number_input("Oficina (%)", min_value=0, max_value=100, value=50)
        ctx_casual = col2.number_input("Casual (%)", min_value=0, max_value=100, value=40)
        ctx_evento = st.number_input("Evento Social (%)", min_value=0, max_value=100, value=10)

        total_pct = ctx_oficina + ctx_casual + ctx_evento
        contextos = {
            'Oficina': ctx_oficina / total_pct if total_pct > 0 else 0,
            'Casual': ctx_casual / total_pct if total_pct > 0 else 0,
            'Evento Social': ctx_evento / total_pct if total_pct > 0 else 0
        }

        st.header("3. Prendas Imprescindibles")
        prendas_obligatorias_nombres = st.multiselect(
            "Selecciona prendas que DEBEN estar en el armario:",
            options=catalogo_completo['Nombre'].tolist()
        )
        prendas_obligatorias_idx = catalogo_completo[catalogo_completo['Nombre'].isin(prendas_obligatorias_nombres)].index.tolist()

        # --- NUEVO: SECCIÓN DE COLORIMETRÍA ---
        st.header("4. Tu Perfil de Colorimetría (Opcional)")
        
        tono_piel = st.selectbox(
            "Tu tono de piel se describe mejor como:",
            ['Frío (rosado)', 'Cálido (dorado)', 'Neutro', 'Oliva']
        )
        color_ojos = st.selectbox(
            "Color de ojos:",
            ['Azul', 'Verde', 'Marrón', 'Gris', 'Avellana']
        )
        color_pelo = st.selectbox(
            "Color de pelo natural:",
            ['Rubio', 'Castaño claro', 'Castaño oscuro', 'Negro', 'Pelirrojo']
        )

        estacion_usuario = determinar_estacion_colorimetria(tono_piel, color_ojos, color_pelo)
        st.info(f"Tu estación de colorimetría sugerida es: **{estacion_usuario}**")

        # Botón para iniciar la optimización
        if st.button("✨ ¡Optimizar mi Armario!", type="primary"):
            with st.spinner('El algoritmo genético está buscando las mejores combinaciones... ¡Esto puede tardar un momento!'):
                
                progress_bar = st.progress(0)
                status_text = st.empty()

                def streamlit_callback(progreso, mensaje):
                    progress_bar.progress(progreso)
                    status_text.text(mensaje)
                
                user_inputs = {
                    'tam_armario': tam_armario,
                    'contextos': contextos,
                    'prendas_obligatorias_idx': prendas_obligatorias_idx,
                    'estacion_colorimetria': estacion_usuario # Nuevo input
                }
                
                ag = EcoClosetAG(catalogo_df=catalogo_completo, user_inputs=user_inputs)
                mejores_armarios, historial_fitness = ag.ejecutar(streamlit_callback=streamlit_callback)
                
                st.session_state.resultados = mejores_armarios
                st.session_state.historial_fitness = historial_fitness

            st.success("¡Optimización completada!")

# --- Área de Resultados ---
st.header("🏆 Resultados de la Optimización")

if st.session_state.resultados:
    catalogo_completo = st.session_state.catalogo_completo
    cols = st.columns(len(st.session_state.resultados))
    
    for i, armario_data in enumerate(st.session_state.resultados):
        with cols[i]:
            st.subheader(f"Armario Propuesto #{i+1}")
            
            individuo = armario_data['individuo']
            armario_df = catalogo_completo.iloc[np.where(individuo == 1)[0]]
            
            moodboard_path = f'moodboards_temp/armario_{i+1}.png'
            crear_mood_board(armario_df, moodboard_path, img_folder='imagenes')
            st.image(moodboard_path, caption=f"Mood board del Armario #{i+1}")
            
            st.metric("Prendas Totales", len(armario_df))
            st.metric("Atuendos Estimados", f"{armario_data['atuendos']:,}")
            st.metric("Fitness", f"{armario_data['fitness']:.4f}")
            
            with st.expander("Ver lista de prendas"):
                st.dataframe(armario_df[['Nombre', 'Tipo', 'Color', 'Estilo', 'Temporada']])

    st.header("📈 Evolución del Fitness")
    fig = graficar_evolucion_fitness(st.session_state.historial_fitness)
    st.pyplot(fig)

    # --- NUEVA SECCIÓN: ANÁLISIS DEL MEJOR ARMARIO ---
    st.header("🔍 Análisis Profundo del Mejor Armario")
    st.markdown("Análisis detallado del **Armario Propuesto #1**, la mejor solución encontrada por el algoritmo.")

    mejor_armario_data = st.session_state.resultados[0]
    mejor_armario_individuo = mejor_armario_data['individuo']
    mejor_armario_df = catalogo_completo.iloc[np.where(mejor_armario_individuo == 1)[0]]
    
    analisis_mvp = analizar_prenda_mvp(mejor_armario_df)

    if analisis_mvp:
        st.subheader("🏆 Prenda Más Valiosa (MVP)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Nombre de la Prenda",
                value=analisis_mvp['nombre']
            )
            st.write(f"**Tipo:** {analisis_mvp['tipo']}")
            st.write(f"**Color:** {analisis_mvp['color']}")
            st.write(f"**Estilo:** {analisis_mvp['estilo']}")

        with col2:
            st.metric(
                label="Combinaciones Potenciales",
                value=f"{int(analisis_mvp['combinaciones']):,}",
                help="Número estimado de atuendos diferentes que esta prenda puede ayudar a formar dentro de este armario."
            )

        st.subheader("Ranking de Versatilidad de Prendas")
        st.dataframe(analisis_mvp['df_completo'].reset_index(drop=True))

elif st.session_state.catalogo_completo is None:
    st.info("Carga un catálogo en la barra lateral para comenzar.")