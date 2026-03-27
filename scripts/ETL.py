import pandas as pd

def run_etl():
    df_2020 = pd.read_csv('data/raw/ENMA_2020.csv.csv')
    df_2023 = pd.read_csv('data/raw/ENMA_2023.csv')
    coincidencias = pd.read_csv('data/raw/ENMA_coincidencias.csv')
    
    # TODO: Reaqlizar las transformaciones
    print("ETL completado con éxito.")

if __name__ == "__main__":
    run_etl()