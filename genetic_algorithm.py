import numpy as np
import random
from compatibility import calcular_atuendos_ponderados, encontrar_atuendos_validos
from colorimetry import obtener_paleta_recomendada
from utils import get_color_category

class EcoClosetAG:
    def __init__(self, catalogo_df, user_inputs):
        self.catalogo = catalogo_df
        self.todos_los_indices = list(range(len(catalogo_df)))
        
        self.tam_poblacion = 50
        self.num_generaciones = 100
        self.prob_cruce = 0.85
        self.prob_mutacion = 0.10
        
        self.tam_armario_deseado = user_inputs['tam_armario']
        self.preferencias_estilo = user_inputs.get('preferencias_estilo', {})
        self.prendas_obligatorias_idx = user_inputs.get('prendas_obligatorias_idx', [])
        
        self.estacion_usuario = user_inputs.get('estacion_colorimetria', None)
        self.colores_favoritos = user_inputs.get('colores_favoritos', [])
        
        self.paleta_recomendada = obtener_paleta_recomendada(
            self.estacion_usuario, 
            self.colores_favoritos
        )

    def _crear_individuo(self):
        individuo = list(self.prendas_obligatorias_idx)
        num_prendas_a_elegir = self.tam_armario_deseado - len(individuo)
        if num_prendas_a_elegir < 0:
            return individuo[:self.tam_armario_deseado]

        pool_candidatos = [idx for idx in self.todos_los_indices if idx not in individuo]
        if len(pool_candidatos) < num_prendas_a_elegir:
            num_prendas_a_elegir = len(pool_candidatos)

        prendas_aleatorias = random.sample(pool_candidatos, num_prendas_a_elegir)
        individuo.extend(prendas_aleatorias)
        random.shuffle(individuo)
        return individuo

    def _crear_poblacion_inicial(self):
        return [self._crear_individuo() for _ in range(self.tam_poblacion)]

    def _calcular_fitness(self, individuo):
        armario_df = self.catalogo.iloc[individuo]
        if armario_df.empty:
            return 0, {}

        puntuacion_total_atuendos = calcular_atuendos_ponderados(armario_df)
        fitness_atuendos = np.log1p(puntuacion_total_atuendos)

        if self.preferencias_estilo:
            total_puntuacion_usuario = sum(self.preferencias_estilo.values())
            preferencias_normalizadas = {estilo: punt / total_puntuacion_usuario for estilo, punt in self.preferencias_estilo.items()}
            distribucion_actual = armario_df['Estilo'].value_counts(normalize=True).to_dict()
            error_estilo = sum((preferencias_normalizadas.get(estilo, 0) - distribucion_actual.get(estilo, 0))**2 for estilo in set(preferencias_normalizadas) | set(distribucion_actual))
            fitness_versatilidad_estilo = 1 / (1 + np.sqrt(error_estilo))
        else:
            fitness_versatilidad_estilo = 0.5

        temporadas_cubiertas = armario_df['Temporada'].unique()
        score_temporada = 0
        if 'Todo el año' in temporadas_cubiertas: score_temporada += 0.5
        if len([t for t in temporadas_cubiertas if t != 'Todo el año']) > 1: score_temporada += 0.5
        
        fitness_versatilidad_total = (fitness_versatilidad_estilo * 0.7) + (score_temporada * 0.3)

        colores_armario = armario_df['Color'].tolist()
        if self.paleta_recomendada:
            prendas_compatibles = sum(1 for color in colores_armario if color in self.paleta_recomendada)
            fitness_colores = prendas_compatibles / len(colores_armario) if len(colores_armario) > 0 else 0
        else:
            categorias_color = [get_color_category(c) for c in colores_armario]
            num_neutros = categorias_color.count('Neutro')
            fitness_colores = num_neutros / len(colores_armario) if len(colores_armario) > 0 else 0

        puntuacion_sostenibilidad = armario_df['Sostenibilidad'].mean()
        fitness_sostenibilidad = (puntuacion_sostenibilidad - 1) / 4 if not np.isnan(puntuacion_sostenibilidad) else 0

        peso_atuendos = 0.45
        peso_versatilidad = 0.35
        peso_colores = 0.10
        peso_sostenibilidad = 0.10
        fitness_total = (peso_atuendos * fitness_atuendos +
                         peso_versatilidad * fitness_versatilidad_total +
                         peso_colores * fitness_colores +
                         peso_sostenibilidad * fitness_sostenibilidad)
        
        metricas = {'atuendos': puntuacion_total_atuendos, 'sostenibilidad_score': puntuacion_sostenibilidad}
        return fitness_total, metricas

    def _seleccion_torneo(self, poblacion, fitness_scores):
        torneo_size = 5
        indices_torneo = random.sample(range(len(poblacion)), torneo_size)
        mejor_individuo_idx = max(indices_torneo, key=lambda idx: fitness_scores[idx][0])
        return poblacion[mejor_individuo_idx]

    def _cruce_pool_genes(self, padre1, padre2):
        pool_genes = list(set(padre1) | set(padre2))
        hijo1 = list(self.prendas_obligatorias_idx)
        hijo2 = list(self.prendas_obligatorias_idx)
        genes_disponibles = [gen for gen in pool_genes if gen not in self.prendas_obligatorias_idx]
        
        def completar_hijo(hijo):
            necesarios = self.tam_armario_deseado - len(hijo)
            if necesarios <= 0: return hijo[:self.tam_armario_deseado]

            genes_a_anadir = random.sample(genes_disponibles, min(len(genes_disponibles), necesarios))
            hijo.extend(genes_a_anadir)

            if len(hijo) < self.tam_armario_deseado:
                pool_global = [i for i in self.todos_los_indices if i not in hijo]
                hijo.extend(random.sample(pool_global, self.tam_armario_deseado - len(hijo)))
            return hijo
        
        return completar_hijo(hijo1), completar_hijo(hijo2)

    def _mutacion_intercambio(self, individuo):
        """
        Función de mutación corregida y simplificada.
        """
        if random.random() < self.prob_mutacion:
            # 1. Encuentra las POSICIONES (índices) en el individuo que se pueden mutar.
            posiciones_mutables = [i for i, gen_id in enumerate(individuo) if gen_id not in self.prendas_obligatorias_idx]
            
            # Si no hay posiciones mutables (ej. todo el armario es obligatorio), no hacer nada.
            if not posiciones_mutables:
                return individuo
            
            # 2. Elige una de esas POSICIONES al azar para cambiar.
            posicion_a_reemplazar = random.choice(posiciones_mutables)
            
            # 3. Encuentra un nuevo gen (ID de prenda) que no esté ya en el armario.
            pool_reemplazo = [gen_id for gen_id in self.todos_los_indices if gen_id not in individuo]
            
            # Si no hay prendas fuera del armario para intercambiar, no hacer nada.
            if not pool_reemplazo:
                return individuo
            
            gen_nuevo = random.choice(pool_reemplazo)
            
            # 4. Realiza el reemplazo en la posición elegida.
            individuo[posicion_a_reemplazar] = gen_nuevo
            
        return individuo

    def ejecutar(self, streamlit_callback=None):
        poblacion = self._crear_poblacion_inicial()
        mejor_fitness_historial = []
        
        for generacion in range(self.num_generaciones):
            # Filtrar individuos que no tengan el tamaño correcto (salvaguarda)
            poblacion = [ind for ind in poblacion if len(ind) == self.tam_armario_deseado]
            if not poblacion:
                print("Error: La población se ha quedado vacía. Comprueba la lógica de cruce.")
                return [], []

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
                
                hijo1, hijo2 = self._cruce_pool_genes(padre1, padre2)
                
                hijo1 = self._mutacion_intercambio(hijo1)
                nueva_poblacion.append(hijo1)
                
                if len(nueva_poblacion) < self.tam_poblacion:
                    hijo2 = self._mutacion_intercambio(hijo2)
                    nueva_poblacion.append(hijo2)
            poblacion = nueva_poblacion

        poblacion_final_evaluada = []
        for ind in poblacion:
            if len(ind) == self.tam_armario_deseado:
                fitness, metricas = self._calcular_fitness(ind)
                metricas['individuo'] = ind
                metricas['fitness'] = fitness
                poblacion_final_evaluada.append(metricas)
        
        poblacion_final_evaluada.sort(key=lambda x: x['fitness'], reverse=True)

        mejores_individuos = []
        hashes_vistos = set()
        for item in poblacion_final_evaluada:
            h = hash(tuple(sorted(item['individuo'])))
            if h not in hashes_vistos:
                mejores_individuos.append(item)
                hashes_vistos.add(h)
            if len(mejores_individuos) == 3:
                break
        
        if mejores_individuos:
            mejor_armario_df = self.catalogo.iloc[mejores_individuos[0]['individuo']]
            lista_de_atuendos = encontrar_atuendos_validos(mejor_armario_df)
            mejores_individuos[0]['combinaciones_lista'] = lista_de_atuendos
        
        return mejores_individuos, mejor_fitness_historial