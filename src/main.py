import streamlit as st
import pandas as pd
import os


#cra função que formata o dataframe
def format_df(df):
    df = df.replace({',': ';'}, regex=True)


    # converte ponto decimal para vírgula nas colunas numéricas
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].apply(lambda x: str(x).replace('.', ',') if pd.notnull(x) else x)
        # substitui valores na coluna 'Temperature unit'
        if 'Temperature unit' in df.columns:
            df['Temperature unit'] = df['Temperature unit'].replace({0: 'celcius', 1: 'fahrenheit'}, regex=True)
            # substitui valores na coluna 'Pressure unit'
        if 'Pressure unit' in df.columns:
            df['Pressure unit'] = df['Pressure unit'].replace({0: 'psi', 1: 'bar'}, regex=True)
    return df


def export(df, filename):
    """
    Exporta o DataFrame para um arquivo CSV com o nome especificado.
    """
    output_dir = os.path.join(os.getcwd(), "../data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False, sep=';')
    print(f"Arquivo exportado para: {output_path}")


def join_files(data_dir):
    """
    Função para ler e concatenar todos os arquivos CSV em um diretório específico.
    """
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    df_list = []
    
    for file in csv_files:
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)
        df_list.append(df)
    
    df_final = pd.concat(df_list, ignore_index=True)
    return df_final

if __name__ == "__main__":

    # monta os arquivos de entrada a partir dos logs diários
    data_dir = os.path.join(os.getcwd(), "../raw_data")
    df = join_files(data_dir)
    df_formatted = format_df(df)

    out_dir = os.path.join(os.getcwd(), "../data")
    export(df_formatted, "data.csv")

    df.to_pickle(os.path.join(out_dir, f"data.pkl"))