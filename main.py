# main.py
import pandas as pd
from database import cargar_catalogo
from genetic_algorithm import EcoClosetAG
from utils import crear_mood_board, graficar_evolucion_fitness

def main():
    print("--- Iniciando EcoCloset AG ---")

    # 1. Entradas del Sistema (definidas por el usuario)
    user_inputs = {
        'tam_armario': 15,  # Número deseado de prendas en el armario cápsula
        'contextos': {      # Distribución de necesidades por contexto
            'Oficina': 0.5,
            'Casual': 0.4,
            'Evento Social': 0.1
        },
        # 'prendas_obligatorias': [1, 6] # Futura mejora: prendas que deben estar sí o sí
    }
    
    print("\nParámetros del usuario:")
    print(f" - Tamaño del armario deseado: {user_inputs['tam_armario']}")
    print(f" - Necesidades por contexto: {user_inputs['contextos']}")

    # 2. Cargar la base de conocimiento
    catalogo_completo = cargar_catalogo()
    if catalogo_completo is None:
        return # Termina la ejecución si no se carga el catálogo
    
    # 3. Inicializar y ejecutar el Algoritmo Genético
    print("\nIniciando optimización con Algoritmo Genético...")
    ag = EcoClosetAG(catalogo_df=catalogo_completo, user_inputs=user_inputs)
    mejores_armarios, historial_fitness = ag.ejecutar()

    # 4. Mostrar las salidas esperadas
    print("\n--- Optimización Finalizada. Mostrando los 3 mejores armarios encontrados ---")
    
    if not mejores_armarios:
        print("No se encontraron soluciones válidas.")
        return

    for i, armario_data in enumerate(mejores_armarios):
        print("\n" + "="*50)
        print(f"  MEJOR ARMARIO CÁPSULA #{i+1}")
        print("="*50)
        
        individuo = armario_data['individuo']
        armario_df = catalogo_completo[individuo == 1]
        
        # a) Tabla detallada de prendas
        print("\n[+] Prendas seleccionadas:")
        print(armario_df[['Nombre', 'Tipo', 'Color', 'Estilo']].to_string(index=False))

        # b) Panel de resumen con métricas
        print("\n[+] Resumen del armario:")
        print(f"  - Número total de prendas: {len(armario_df)}")
        print(f"  - Fitness de la solución: {armario_data['fitness']:.4f}")
        print(f"  - Atuendos únicos estimados: {armario_data['atuendos']}")
        
        # c) Visualización gráfica (mood board)
        print("\n[+] Generando visualización...")
        output_moodboard_path = f'armario_propuesto_{i+1}.png'
        crear_mood_board(armario_df, output_moodboard_path)

    # 5. Graficar evolución del fitness
    graficar_evolucion_fitness(historial_fitness)

if __name__ == '__main__':
    main()