# genetic_algorithm.py
import numpy as np
import random
from utils import get_color_category
from colorimetry import obtener_paleta_recomendada # Nuevo import

class EcoClosetAG:
    def __init__(self, catalogo_df, user_inputs):
        self.catalogo = catalogo_df
        self.num_prendas_catalogo = len(catalogo_df)
        
        self.tam_poblacion = 50
        self.num_generaciones = 100
        self.prob_cruce = 0.8
        self.prob_mutacion = 0.15
        
        self.tam_armario_deseado = user_inputs['tam_armario']
        self.necesidades_contexto = user_inputs['contextos']
        self.prendas_obligatorias_idx = user_inputs.get('prendas_obligatorias_idx', [])
        
        # --- NUEVO: Manejo de Colorimetría ---
        self.estacion_usuario = user_inputs.get('estacion_colorimetria', None)
        if self.estacion_usuario:
            self.paleta_recomendada = obtener_paleta_recomendada(self.estacion_usuario)
        else:
            self.paleta_recomendada = []

    def _crear_individuo(self):
        individuo = np.zeros(self.num_prendas_catalogo, dtype=int)
        individuo[self.prendas_obligatorias_idx] = 1
        
        num_prendas_restantes = self.tam_armario_deseado - len(self.prendas_obligatorias_idx)
        if num_prendas_restantes > 0:
            candidatos_idx = np.where(individuo == 0)[0]
            indices_seleccionados = np.random.choice(candidatos_idx, num_prendas_restantes, replace=False)
            individuo[indices_seleccionados] = 1
            
        return individuo

    def _crear_poblacion_inicial(self):
        return [self._crear_individuo() for _ in range(self.tam_poblacion)]

    def _calcular_fitness(self, individuo):
        armario_df = self.catalogo.iloc[np.where(individuo == 1)[0]]
        if armario_df.empty:
            return 0, {}

        # --- MÉTRICA 1: ATUENDOS ---
        tops = armario_df[armario_df['Tipo'] == 'Top']
        pantalones_faldas = armario_df[armario_df['Tipo'].isin(['Pantalón', 'Falda'])]
        calzados = armario_df[armario_df['Tipo'] == 'Calzado']
        exteriores = armario_df[armario_df['Tipo'] == 'Exterior']
        vestidos = armario_df[armario_df['Tipo'] == 'Vestido']

        atuendos_basicos = len(tops) * len(pantalones_faldas) * len(calzados)
        atuendos_vestido = len(vestidos) * len(calzados)
        atuendos_invierno = atuendos_basicos * len(exteriores)

        total_atuendos_estimados = atuendos_basicos + atuendos_vestido + atuendos_invierno
        fitness_atuendos = np.log1p(total_atuendos_estimados)

        # --- MÉTRICA 2: VERSATILIDAD ---
        distribucion_actual = armario_df['Estilo'].value_counts(normalize=True).to_dict()
        error_estilo = sum(abs(prop_deseada - distribucion_actual.get(ctx, 0)) for ctx, prop_deseada in self.necesidades_contexto.items())
        fitness_versatilidad_estilo = 1 - error_estilo

        temporadas_cubiertas = armario_df['Temporada'].unique()
        score_temporada = 0
        if 'Todo el año' in temporadas_cubiertas:
            score_temporada += 0.5
        if len([t for t in temporadas_cubiertas if t != 'Todo el año']) > 0:
            score_temporada += 0.5
        fitness_versatilidad_temporada = score_temporada
        
        fitness_versatilidad_total = (fitness_versatilidad_estilo * 0.7) + (fitness_versatilidad_temporada * 0.3)

        # --- MÉTRICA 3: ARMONÍA DE COLOR (REDISEÑADA) ---
        colores_armario = armario_df['Color'].tolist()
        if self.estacion_usuario and self.paleta_recomendada:
            # Lógica de colorimetría personalizada
            prendas_compatibles = sum(1 for color in colores_armario if color in self.paleta_recomendada)
            fitness_colores = prendas_compatibles / len(colores_armario) if len(colores_armario) > 0 else 0
        else:
            # Lógica original si no se usa la colorimetría (basada en neutros)
            categorias_color = [get_color_category(c) for c in colores_armario]
            num_neutros = categorias_color.count('Neutro')
            fitness_colores = num_neutros / len(colores_armario) if len(colores_armario) > 0 else 0

        # --- COMBINACIÓN FINAL DE FITNESS ---
        peso_atuendos = 0.5
        peso_versatilidad = 0.3
        peso_colores = 0.2
        
        fitness_total = (peso_atuendos * fitness_atuendos +
                         peso_versatilidad * fitness_versatilidad_total +
                         peso_colores * fitness_colores)
        
        metricas = {
            'atuendos': total_atuendos_estimados,
            'versatilidad': fitness_versatilidad_total,
            'color': fitness_colores
        }

        return fitness_total, metricas

    def _seleccion_torneo(self, poblacion, fitness_scores):
        torneo_size = 5
        indices_torneo = random.sample(range(len(poblacion)), torneo_size)
        mejor_individuo_idx = max(indices_torneo, key=lambda idx: fitness_scores[idx][0])
        return poblacion[mejor_individuo_idx]

    def _cruce_un_punto(self, padre1, padre2):
        punto_cruce = random.randint(1, self.num_prendas_catalogo - 1)
        hijo1 = np.concatenate([padre1[:punto_cruce], padre2[punto_cruce:]])
        hijo2 = np.concatenate([padre2[:punto_cruce], padre1[punto_cruce:]])
        return hijo1, hijo2

    def _corregir_individuo(self, individuo):
        individuo[self.prendas_obligatorias_idx] = 1
        num_prendas_actual = np.sum(individuo)
        diferencia = num_prendas_actual - self.tam_armario_deseado

        if diferencia > 0:
            indices_removibles = np.where((individuo == 1) & (np.isin(np.arange(self.num_prendas_catalogo), self.prendas_obligatorias_idx, invert=True)))[0]
            indices_a_quitar = np.random.choice(indices_removibles, diferencia, replace=False)
            individuo[indices_a_quitar] = 0
        elif diferencia < 0:
            indices_agregables = np.where(individuo == 0)[0]
            indices_a_agregar = np.random.choice(indices_agregables, -diferencia, replace=False)
            individuo[indices_a_agregar] = 1
        return individuo

    def _mutacion(self, individuo):
        if random.random() < self.prob_mutacion:
            indices_dentro_mutables = np.where((individuo == 1) & (np.isin(np.arange(self.num_prendas_catalogo), self.prendas_obligatorias_idx, invert=True)))[0]
            indices_fuera = np.where(individuo == 0)[0]
            if len(indices_dentro_mutables) > 0 and len(indices_fuera) > 0:
                quitar_idx = random.choice(indices_dentro_mutables)
                agregar_idx = random.choice(indices_fuera)
                individuo[quitar_idx] = 0
                individuo[agregar_idx] = 1
        return individuo

    def ejecutar(self, streamlit_callback=None):
        poblacion = self._crear_poblacion_inicial()
        mejor_fitness_historial = []
        
        for generacion in range(self.num_generaciones):
            fitness_scores = [self._calcular_fitness(ind) for ind in poblacion]
            mejor_fitness_actual = max(score[0] for score in fitness_scores)
            mejor_fitness_historial.append(mejor_fitness_actual)
            
            if streamlit_callback:
                progreso = (generacion + 1) / self.num_generaciones
                streamlit_callback(progreso, f"Generación {generacion + 1}/{self.num_generaciones} - Mejor Fitness: {mejor_fitness_actual:.4f}")

            nueva_poblacion = []
            while len(nueva_poblacion) < self.tam_poblacion:
                padre1 = self._seleccion_torneo(poblacion, fitness_scores)
                padre2 = self._seleccion_torneo(poblacion, fitness_scores)
                
                if random.random() < self.prob_cruce:
                    hijo1, hijo2 = self._cruce_un_punto(padre1, padre2)
                    hijo1 = self._corregir_individuo(self._mutacion(hijo1))
                    hijo2 = self._corregir_individuo(self._mutacion(hijo2))
                else:
                    hijo1, hijo2 = padre1.copy(), padre2.copy()
                
                nueva_poblacion.append(hijo1)
                if len(nueva_poblacion) < self.tam_poblacion:
                    nueva_poblacion.append(hijo2)
            poblacion = nueva_poblacion

        poblacion_final_evaluada = []
        for ind in poblacion:
            fitness, metricas = self._calcular_fitness(ind)
            poblacion_final_evaluada.append({'individuo': ind, 'fitness': fitness, **metricas})
        
        poblacion_final_evaluada.sort(key=lambda x: x['fitness'], reverse=True)

        mejores_individuos = []
        hashes_vistos = set()
        for item in poblacion_final_evaluada:
            h = hash(item['individuo'].tobytes())
            if h not in hashes_vistos:
                mejores_individuos.append(item)
                hashes_vistos.add(h)
            if len(mejores_individuos) == 3:
                break
        
        return mejores_individuos, mejor_fitness_historial