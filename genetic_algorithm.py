# Importaciones necesarias para el funcionamiento del algoritmo
import numpy as np  # Para operaciones numéricas, especialmente en la función de fitness.
import random       # Para todas las operaciones aleatorias: selección, cruce, mutación.
from compatibility import calcular_atuendos_ponderados, encontrar_atuendos_validos # Importa las funciones "inteligentes" de estilismo.
from colorimetry import obtener_paleta_recomendada # Para obtener la paleta de colores personalizada del usuario.
from utils import get_color_category # Utilidad para clasificar colores.

class EcoClosetAG:
    # --- 1. Inicialización (`__init__`) ---
    # Esta sección se ejecuta una sola vez, cuando creas una instancia de la clase.
    # Su propósito es configurar el algoritmo con todos los parámetros y datos necesarios.
    def __init__(self, catalogo_df, user_inputs):
        # --- Almacenamiento de Datos ---
        self.catalogo = catalogo_df  # Guarda el DataFrame completo de prendas para poder consultarlo.
        self.todos_los_indices = list(range(len(catalogo_df))) # Crea una lista con todos los IDs posibles de prendas (ej. [0, 1, 2, ..., 19]). Esencial para la mutación y creación.

        # --- Hiperparámetros del Algoritmo Genético ---
        # Estos valores definen el comportamiento del algoritmo.
        self.tam_poblacion = 50       # Define cuántos "armarios" (individuos) existirán en cada generación.
        self.num_generaciones = 100   # Define cuántas veces el ciclo de evolución (selección, cruce, mutación) se repetirá.
        self.prob_cruce = 0.85        # La probabilidad (85%) de que dos padres seleccionados se crucen para crear hijos.
        self.prob_mutacion = 0.10     # La probabilidad (10%) de que un individuo sufra un cambio aleatorio (mutación).

        # --- Restricciones y Preferencias del Usuario ---
        # Estos valores vienen de la interfaz de Streamlit.
        self.tam_armario_deseado = user_inputs['tam_armario'] # El tamaño fijo que debe tener cada armario.
        self.preferencias_estilo = user_inputs.get('preferencias_estilo', {}) # El diccionario con los estilos y puntuaciones del usuario.
        self.prendas_obligatorias_idx = user_inputs.get('prendas_obligatorias_idx', []) # Lista de IDs de prendas que DEBEN estar en la solución.
        self.estacion_usuario = user_inputs.get('estacion_colorimetria', None) # La estación de colorimetría del usuario (ej. 'Verano').
        self.colores_favoritos = user_inputs.get('colores_favoritos', []) # Lista de colores favoritos del usuario.
        
        # --- Pre-cálculo de la Paleta de Colores ---
        # Se calcula una sola vez para ser usada repetidamente en la función de fitness.
        self.paleta_recomendada = obtener_paleta_recomendada(
            self.estacion_usuario, 
            self.colores_favoritos
        )

    # --- 2. Creación de Individuos y Población Inicial ---
    def _crear_individuo(self):
        # Crea un único armario (cromosoma) que cumple con las restricciones básicas.
        individuo = list(self.prendas_obligatorias_idx) # Empieza el armario con las prendas que el usuario marcó como obligatorias.
        num_prendas_a_elegir = self.tam_armario_deseado - len(individuo) # Calcula cuántas prendas faltan para completar el armario.
        
        # Salvaguarda: si el usuario eligió más prendas obligatorias que el tamaño del armario, se recorta la lista.
        if num_prendas_a_elegir < 0:
            return individuo[:self.tam_armario_deseado]

        # Crea un "pool" de candidatos: todos los IDs de prendas que no son obligatorios.
        pool_candidatos = [idx for idx in self.todos_los_indices if idx not in individuo]
        
        # Otra salvaguarda: si no hay suficientes candidatos para llenar el armario, se ajusta el número a elegir.
        if len(pool_candidatos) < num_prendas_a_elegir:
            num_prendas_a_elegir = len(pool_candidatos)

        # Selecciona al azar las prendas restantes del pool de candidatos.
        prendas_aleatorias = random.sample(pool_candidatos, num_prendas_a_elegir)
        individuo.extend(prendas_aleatorias) # Añade las prendas aleatorias al armario.
        random.shuffle(individuo) # Baraja el armario para que las prendas obligatorias no estén siempre al principio.
        return individuo

    def _crear_poblacion_inicial(self):
        # Crea la primera generación de armarios llamando a _crear_individuo repetidamente.
        return [self._crear_individuo() for _ in range(self.tam_poblacion)]

    # --- 3. Función de Aptitud (`_calcular_fitness`) ---
    # El cerebro del algoritmo. Evalúa qué tan "bueno" es un armario y le asigna una puntuación.
    def _calcular_fitness(self, individuo):
        armario_df = self.catalogo.iloc[individuo] # Obtiene el DataFrame con los datos de las prendas del armario actual.
        if armario_df.empty: # Si por alguna razón el armario está vacío, su calidad es cero.
            return 0, {}

        # --- Métrica 1: Calidad de Atuendos ---
        puntuacion_total_atuendos = calcular_atuendos_ponderados(armario_df) # Llama a la función experta que calcula la calidad de las combinaciones.
        fitness_atuendos = np.log1p(puntuacion_total_atuendos) # Aplica una transformación logarítmica para suavizar la puntuación.

        # --- Métrica 2: Versatilidad (Alineación con el Estilo del Usuario) ---
        if self.preferencias_estilo: # Solo si el usuario definió sus estilos...
            total_puntuacion_usuario = sum(self.preferencias_estilo.values()) # Suma las puntuaciones del usuario (ej. 5+8+3=16).
            preferencias_normalizadas = {estilo: punt / total_puntuacion_usuario for estilo, punt in self.preferencias_estilo.items()} # Convierte las puntuaciones a porcentajes (ej. 5/16, 8/16, 3/16).
            distribucion_actual = armario_df['Estilo'].value_counts(normalize=True).to_dict() # Calcula la distribución de estilos en el armario actual.
            error_estilo = sum((preferencias_normalizadas.get(estilo, 0) - distribucion_actual.get(estilo, 0))**2 for estilo in set(preferencias_normalizadas) | set(distribucion_actual)) # Calcula el error cuadrático entre la distribución deseada y la real.
            fitness_versatilidad_estilo = 1 / (1 + np.sqrt(error_estilo)) # Convierte el error en una puntuación de similitud (más cercano a 1 es mejor).
        else: # Si el usuario no eligió estilos, se le da una puntuación neutral.
            fitness_versatilidad_estilo = 0.5

        # --- Sub-métrica de Versatilidad: Cobertura de Temporadas ---
        temporadas_cubiertas = armario_df['Temporada'].unique() # Obtiene las temporadas cubiertas por el armario.
        score_temporada = 0
        if 'Todo el año' in temporadas_cubiertas: score_temporada += 0.5 # Premia si hay prendas para todo el año.
        if len([t for t in temporadas_cubiertas if t != 'Todo el año']) > 1: score_temporada += 0.5 # Premia si cubre más de una estación específica.
        
        # Combina las dos sub-métricas de versatilidad.
        fitness_versatilidad_total = (fitness_versatilidad_estilo * 0.7) + (score_temporada * 0.3)

        # --- Métrica 3: Armonía de Color ---
        colores_armario = armario_df['Color'].tolist() # Obtiene la lista de colores del armario.
        if self.paleta_recomendada: # Si se generó una paleta para el usuario...
            prendas_compatibles = sum(1 for color in colores_armario if color in self.paleta_recomendada) # Cuenta cuántas prendas coinciden con la paleta.
            fitness_colores = prendas_compatibles / len(colores_armario) if len(colores_armario) > 0 else 0 # Calcula el porcentaje de coincidencia.
        else: # Si no, se recurre a una regla general: premiar los colores neutros.
            categorias_color = [get_color_category(c) for c in colores_armario]
            num_neutros = categorias_color.count('Neutro')
            fitness_colores = num_neutros / len(colores_armario) if len(colores_armario) > 0 else 0

        # --- Métrica 4: Sostenibilidad ---
        puntuacion_sostenibilidad = armario_df['Sostenibilidad'].mean() # Calcula la sostenibilidad promedio del armario.
        fitness_sostenibilidad = (puntuacion_sostenibilidad - 1) / 4 if not np.isnan(puntuacion_sostenibilidad) else 0 # Normaliza el valor a un rango de 0 a 1.

        # --- Combinación Final de Fitness ---
        # Define la importancia de cada métrica.
        peso_atuendos = 0.45
        peso_versatilidad = 0.35
        peso_colores = 0.10
        peso_sostenibilidad = 0.10
        # Calcula la puntuación final como una suma ponderada.
        fitness_total = (peso_atuendos * fitness_atuendos +
                         peso_versatilidad * fitness_versatilidad_total +
                         peso_colores * fitness_colores +
                         peso_sostenibilidad * fitness_sostenibilidad)
        
        # Prepara un diccionario con las métricas para mostrar en la interfaz.
        metricas = {'atuendos': puntuacion_total_atuendos, 'sostenibilidad_score': puntuacion_sostenibilidad}
        return fitness_total, metricas # Devuelve la puntuación final y las métricas.

    # --- 4. Operadores Genéticos (Selección, Cruce, Mutación) ---
    def _seleccion_torneo(self, poblacion, fitness_scores):
        torneo_size = 5 # Elige 5 individuos al azar de la población.
        indices_torneo = random.sample(range(len(poblacion)), torneo_size)
        # De esos 5, encuentra el que tiene la mejor puntuación de fitness.
        mejor_individuo_idx = max(indices_torneo, key=lambda idx: fitness_scores[idx][0])
        return poblacion[mejor_individuo_idx] # Devuelve al ganador del torneo para ser un "padre".

    def _cruce_pool_genes(self, padre1, padre2):
        # Crea un "pool" de genes únicos combinando todas las prendas de ambos padres.
        pool_genes = list(set(padre1) | set(padre2))
        # Los hijos empiezan con las prendas obligatorias.
        hijo1 = list(self.prendas_obligatorias_idx)
        hijo2 = list(self.prendas_obligatorias_idx)
        # Genes disponibles para elegir (los del pool que no son obligatorios).
        genes_disponibles = [gen for gen in pool_genes if gen not in self.prendas_obligatorias_idx]
        
        # Función interna para rellenar un hijo hasta el tamaño deseado.
        def completar_hijo(hijo):
            necesarios = self.tam_armario_deseado - len(hijo)
            if necesarios <= 0: return hijo[:self.tam_armario_deseado]
            # Primero, intenta rellenar con genes del pool de los padres.
            genes_a_anadir = random.sample(genes_disponibles, min(len(genes_disponibles), necesarios))
            hijo.extend(genes_a_anadir)
            # Si aún faltan, rellena con genes aleatorios del catálogo global.
            if len(hijo) < self.tam_armario_deseado:
                pool_global = [i for i in self.todos_los_indices if i not in hijo]
                hijo.extend(random.sample(pool_global, self.tam_armario_deseado - len(hijo)))
            return hijo
        
        return completar_hijo(hijo1), completar_hijo(hijo2) # Devuelve los dos nuevos hijos.

    def _mutacion_intercambio(self, individuo):
        if random.random() < self.prob_mutacion: # Solo muta si se cumple la probabilidad.
            # Encuentra las POSICIONES en el individuo que se pueden cambiar (no obligatorias).
            posiciones_mutables = [i for i, gen_id in enumerate(individuo) if gen_id not in self.prendas_obligatorias_idx]
            if not posiciones_mutables: return individuo # Si no hay nada que mutar, se detiene.
            # Elige una de esas posiciones al azar.
            posicion_a_reemplazar = random.choice(posiciones_mutables)
            # Encuentra una nueva prenda que no esté ya en el armario.
            pool_reemplazo = [gen_id for gen_id in self.todos_los_indices if gen_id not in individuo]
            if not pool_reemplazo: return individuo # Si no hay prendas fuera, se detiene.
            gen_nuevo = random.choice(pool_reemplazo)
            # Realiza el intercambio.
            individuo[posicion_a_reemplazar] = gen_nuevo
        return individuo

    # --- 5. Ciclo de Ejecución Principal (`ejecutar`) ---
    def ejecutar(self, streamlit_callback=None):
        poblacion = self._crear_poblacion_inicial() # Crea la primera generación.
        mejor_fitness_historial = [] # Para guardar el mejor fitness de cada generación y hacer la gráfica.
        
        for generacion in range(self.num_generaciones): # Bucle principal que se repite por cada generación.
            poblacion = [ind for ind in poblacion if len(ind) == self.tam_armario_deseado] # Salvaguarda para asegurar que todos los individuos son válidos.
            if not poblacion: return [], [] # Si la población se vacía, detiene la ejecución.

            fitness_scores = [self._calcular_fitness(ind) for ind in poblacion] # Calcula el fitness de toda la población actual.
            mejor_fitness_actual = max(score[0] for score in fitness_scores) # Encuentra el mejor fitness de esta generación.
            mejor_fitness_historial.append(mejor_fitness_actual) # Lo guarda para la gráfica.
            
            if streamlit_callback: # Si se está usando con Streamlit, actualiza la barra de progreso.
                progreso = (generacion + 1) / self.num_generaciones
                streamlit_callback(progreso, f"Generación {generacion + 1}/{self.num_generaciones} - Mejor Fitness: {mejor_fitness_actual:.4f}")

            # --- Ciclo de Creación de la Nueva Generación ---
            nueva_poblacion = []
            while len(nueva_poblacion) < self.tam_poblacion: # Repite hasta que la nueva generación esté completa.
                padre1 = self._seleccion_torneo(poblacion, fitness_scores) # Selecciona al primer padre.
                padre2 = self._seleccion_torneo(poblacion, fitness_scores) # Selecciona al segundo padre.
                
                if random.random() < self.prob_cruce: # Si se cumple la probabilidad...
                    hijo1, hijo2 = self._cruce_pool_genes(padre1, padre2) # ...se cruzan para crear dos nuevos hijos.
                else: # Si no, los "hijos" son clones de los padres (elitismo).
                    hijo1, hijo2 = padre1[:], padre2[:]
                
                # Aplica la mutación a los hijos.
                hijo1 = self._mutacion_intercambio(hijo1)
                nueva_poblacion.append(hijo1) # Añade al primer hijo a la nueva generación.
                
                if len(nueva_poblacion) < self.tam_poblacion:
                    hijo2 = self._mutacion_intercambio(hijo2)
                    nueva_poblacion.append(hijo2) # Añade al segundo hijo si aún hay espacio.
            poblacion = nueva_poblacion # Reemplaza la población antigua con la nueva.

        # --- Procesamiento Final de Resultados ---
        poblacion_final_evaluada = []
        for ind in poblacion: # Itera sobre la última y mejor generación.
            if len(ind) == self.tam_armario_deseado:
                fitness, metricas = self._calcular_fitness(ind) # Calcula el fitness y las métricas finales.
                metricas['individuo'] = ind
                metricas['fitness'] = fitness
                poblacion_final_evaluada.append(metricas)
        
        poblacion_final_evaluada.sort(key=lambda x: x['fitness'], reverse=True) # Ordena a todos los individuos de mejor a peor.

        # --- Selección de los 3 Mejores Individuos ÚNICOS ---
        mejores_individuos = []
        hashes_vistos = set() # Para evitar mostrar armarios duplicados.
        for item in poblacion_final_evaluada:
            h = hash(tuple(sorted(item['individuo']))) # Crea una "huella digital" única para cada armario.
            if h not in hashes_vistos: # Si no hemos visto este armario antes...
                mejores_individuos.append(item) # ...lo añadimos a la lista de resultados.
                hashes_vistos.add(h)
            if len(mejores_individuos) == 3: # Detiene la búsqueda cuando ya tenemos 3.
                break
        
        # Genera la lista de combinaciones de atuendos solo para el mejor resultado.
        if mejores_individuos:
            mejor_armario_df = self.catalogo.iloc[mejores_individuos[0]['individuo']]
            lista_de_atuendos = encontrar_atuendos_validos(mejor_armario_df)
            mejores_individuos[0]['combinaciones_lista'] = lista_de_atuendos
        
        return mejores_individuos, mejor_fitness_historial # Devuelve los resultados finales.