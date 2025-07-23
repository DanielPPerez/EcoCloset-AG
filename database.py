# database.py
import pandas as pd

def cargar_catalogo(filepath='data/prendas.csv'):
    """
    Carga el catálogo de prendas desde un archivo CSV.
    """
    try:
        df = pd.read_csv(filepath)
        print("Catálogo de prendas cargado exitosamente.")
        return df
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{filepath}'")
        return None

if __name__ == '__main__':
    # Pequeña prueba para ver si funciona
    catalogo = cargar_catalogo()
    if catalogo is not None:
        print("Primeras 5 prendas del catálogo:")
        print(catalogo.head())