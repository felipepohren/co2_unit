import pandas as pd
import os

def load_data(pickle_file):
    """
    Carrega um DataFrame a partir de um arquivo pickle.
    
    Args:
        pickle_file (str): Caminho para o arquivo pickle.
    
    Returns:
        pd.DataFrame: DataFrame carregado.
    """
    return pd.read_pickle(pickle_file)

def save_to_csv(df, filename):
    """
    Salva um DataFrame em um arquivo CSV.
    
    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        filename (str): Nome do arquivo CSV de saída.
    """
    output_dir = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False, sep=';')
    print(f"Arquivo exportado para: {output_path}")

def read_csv_files(data_dir):
    """
    Lê todos os arquivos CSV em um diretório e os concatena em um único DataFrame.
    
    Args:
        data_dir (str): Caminho para o diretório contendo arquivos CSV.
    
    Returns:
        pd.DataFrame: DataFrame concatenado.
    """
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    df_list = []
    
    for file in csv_files:
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)
        df_list.append(df)
    
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()