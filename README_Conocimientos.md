# Base de Conocimientos de EcoCloset AG (`Conocimientos.py`)

Este archivo centraliza **toda la base de conocimientos** utilizada por el sistema EcoCloset AG. Aquí se encuentran listas, diccionarios y reglas fundamentales para la lógica de colorimetría, estilos, compatibilidad, paletas y mapeos de colores. 

## ¿Por qué centralizar la base de conocimientos?
- **Mantenimiento sencillo:** Modifica reglas, paletas o estilos en un solo lugar.
- **Consistencia:** Todos los módulos usan la misma fuente de verdad.
- **Escalabilidad:** Facilita la expansión y documentación del sistema.

---

## Contenido del archivo

### 1. Colorimetría y atributos personales
- `TONOS_DE_PIEL`, `COLORES_DE_OJOS`, `COLORES_DE_CABELLO`: Listas de opciones para el perfil de usuario.
- `NEUTROS_UNIVERSALES`: Colores neutros válidos para cualquier estación.
- `PALETAS_POR_ESTACION`: Diccionario con las paletas de colores recomendadas según la estación colorimétrica.
- `ATRIBUTOS_DE_COLOR`: Mapeo de atributos a subtonos y contraste, usado para determinar la estación del usuario.

**Se utiliza en:**
- `colorimetry.py` (lógica de análisis de colorimetría y sugerencia de paleta)
- `app.py` (interfaz de selección de perfil y visualización de paletas)

### 2. Estilos y compatibilidad
- `ESTILOS_ROPA`: Lista de estilos disponibles para el usuario.
- `REGLAS_COMBINACION_ESTILO`: Matriz de compatibilidad entre estilos.
- `REGLAS_COMBINACION_MATERIAL`: Matriz de compatibilidad entre materiales/texturas.

**Se utiliza en:**
- `compatibility.py` (cálculo de compatibilidad de atuendos y generación de combinaciones válidas)
- `app.py` (selección de estilos preferidos)

### 3. Paletas y mapeos de colores
- `COLOR_PALETTES`: Mapeo simple de colores a categorías (Neutro, Cálido, Frío).
- `COLOR_MAP`: Diccionario que asocia nombres de colores a sus códigos hexadecimales para visualización.

**Se utiliza en:**
- `utils.py` (clasificación de colores y visualización de moodboards)
- `app.py` (visualización de colores en la interfaz)

### 4. Descripciones de estaciones
- `DESCRIPCIONES_ESTACIONES`: Diccionario con descripciones para cada estación colorimétrica.

**Se utiliza en:**
- `app.py` (mostrar explicación de la estación sugerida al usuario)



## Relación con los módulos principales
- **colorimetry.py:** Usa los atributos y paletas para determinar la estación y sugerir colores.
- **compatibility.py:** Usa los estilos y reglas para validar combinaciones de atuendos.
- **utils.py:** Usa las paletas y mapeos para clasificar y mostrar colores.
- **app.py:** Usa todo para construir la interfaz y lógica de usuario.

---

## ¿Cómo modificar la base de conocimientos?
1. Abre `Conocimientos.py`.
2. Modifica, agrega o elimina elementos en las listas o diccionarios según tus necesidades.
3. ¡Listo! Todos los módulos usarán automáticamente los nuevos valores.

---

## Notas adicionales
- Si agregas un nuevo estilo, recuerda actualizar tanto `ESTILOS_ROPA` como las reglas de compatibilidad.
- Si agregas un nuevo color, añade su código hex en `COLOR_MAP` para que se visualice correctamente.
- Si cambias la lógica de estaciones, ajusta también las paletas y descripciones.

---

**Autor:** Daniel Peregrino Perez
**Proyecto:** EcoCloset AG 

---

## Algoritmo Genético en EcoCloset AG

El sistema utiliza un **algoritmo genético** para optimizar la selección del armario cápsula ideal según tus preferencias, estilos, colorimetría y sostenibilidad.

### ¿Cómo funciona?
1. **Inicialización:**
   - Se genera una población inicial de posibles armarios (conjuntos de prendas), respetando las prendas obligatorias y el tamaño deseado.
2. **Evaluación (Fitness):**
   - Cada armario se evalúa según:
     - Calidad y compatibilidad de atuendos (usando reglas de estilo y material).
     - Versatilidad de estilos (qué tanto se ajusta a tus preferencias).
     - Cobertura de temporadas.
     - Afinidad de colores con tu paleta recomendada.
     - Sostenibilidad promedio.
3. **Selección:**
   - Se utiliza **torneo**: se eligen varios armarios al azar y se selecciona el mejor para reproducirse.
4. **Cruza (Crossover):**
   - Se combinan los genes (prendas) de dos padres usando un **pool de genes** (unión de prendas de ambos padres), asegurando que las prendas obligatorias siempre estén presentes.
   - Se completa el armario con prendas únicas hasta alcanzar el tamaño deseado.
5. **Mutación:**
   - Con cierta probabilidad, se intercambia una prenda no obligatoria por otra que no esté en el armario, promoviendo la diversidad.
6. **Poda y reemplazo:**
   - Se mantiene la población en tamaño fijo, reemplazando la generación anterior por la nueva.
   - Al final, se filtran los mejores armarios únicos (sin duplicados) según su fitness.

### Estrategias específicas
- **Mutación:**
  - Intercambio de una prenda no obligatoria por otra fuera del armario (si existe), solo si ocurre la probabilidad de mutación.
- **Cruza:**
  - Pool de genes: los hijos se forman a partir de la unión de prendas de ambos padres, completando con prendas únicas hasta el tamaño requerido.
- **Selección:**
  - Torneo de 5: se seleccionan 5 armarios al azar y se elige el de mayor fitness para reproducirse.
- **Poda:**
  - Al final de la evolución, se filtran los 3 mejores armarios únicos (sin duplicados) para mostrar al usuario.

### Resumen visual
```
Inicialización → Evaluación → Selección (Torneo) → Cruza (Pool de genes) → Mutación (Intercambio) → Nueva generación → ...
```

**Este enfoque permite encontrar armarios óptimos, variados y personalizados, maximizando la compatibilidad, versatilidad y sostenibilidad.** 