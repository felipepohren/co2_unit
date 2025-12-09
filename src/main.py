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
    output_dir = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False, sep=';')
    print(f"Arquivo exportado para: {output_path}")