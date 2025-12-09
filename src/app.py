import streamlit as st
import pandas as pd
from datetime import datetime, time
import os
import uuid
#from main import format_df, export
from viz import plot_df, plot_df_twinx

# Configurações iniciais
st.set_page_config(page_title="Log Visualizer", layout="wide")

# Inicializa session_state para isolar contexto por usuário
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "selected_columns" not in st.session_state:
    st.session_state.selected_columns = []

if "start_datetime" not in st.session_state:
    st.session_state.start_datetime = pd.to_datetime("2025-12-07 00:00:00")

if "end_datetime" not in st.session_state:
    st.session_state.end_datetime = pd.to_datetime("2025-12-07 23:59:59")

if "plot_type" not in st.session_state:
    st.session_state.plot_type = "Split"

# Título da aplicação
st.title("CO2 Unit Log Visualizer")

# Carrega o DataFrame a partir do arquivo pickle
output_dir = os.path.join(os.getcwd(), "data")

# Sidebar para seleção de colunas e intervalo de datas
st.sidebar.header("Configurations")

# Seleção de colunas
columns_list = [
    "Suction pressure",
    "Flash tank pressure",
    "Gas cooler pressure",
    "Evaporation Temperature",
    "Condensation Temperature",
    "Suction temperature",
    "Gas cooler temperature",
    "External temperature",
    "Superheat",
    "Subcooling",
    "Comprssor required",
    "Comprssor output",
    "Discharge temperature",
    "Fan output",
    "HPV oppening",
    "FGV oppening",
    "Cold room ambient temperature",
    "Cold room evaporation temperature",
    "Cold room suction temperature",
    "Cold room defrost temperature",
    "Cold room suction pressure",
    "Cold room superheat"
]

st.session_state.selected_columns = st.sidebar.multiselect(
    "Select the colums to visualize", 
    columns_list,
    default=st.session_state.selected_columns
)

# --- VALORES PADRÃO ---
start_datetime_default = pd.to_datetime("2025-12-07 00:00:00")
end_datetime_default = pd.to_datetime("2025-12-07 23:59:59")

# --- 📅 ENTRADAS DE DATA E HORA DE INÍCIO ---
st.sidebar.subheader("Period")

start_date_input = st.sidebar.date_input(
    "Init date", 
    value=st.session_state.start_datetime.date()
)

start_time_input = st.sidebar.time_input(
    "Init time", 
    value=st.session_state.start_datetime.time(),
    step=600
)

st.session_state.start_datetime = datetime.combine(start_date_input, start_time_input)

# --- 🗓️ ENTRADAS DE DATA E HORA DE FIM ---

end_date_input = st.sidebar.date_input(
    "End date", 
    value=st.session_state.end_datetime.date()
)

end_time_input = st.sidebar.time_input(
    "End time", 
    value=st.session_state.end_datetime.time(),
    step=600 
)

st.session_state.end_datetime = datetime.combine(end_date_input, end_time_input)

# --- VISUALIZAÇÃO DOS RESULTADOS ---

# st.write("## 🕰️ Datetimes Selecionados")
# st.write(f"**Início:** `{st.session_state.start_datetime}`")
# st.write(f"**Fim:** `{st.session_state.end_datetime}`")

# Seleção do tipo de plotagem
st.sidebar.subheader("Plot type")
st.session_state.plot_type = st.sidebar.selectbox(
    " ", 
    ["Split", "Combined"],
    index=0 if st.session_state.plot_type == "Split" else 1
)

# Botão para gerar o gráfico
if st.sidebar.button("Graph generate"):
    if not st.session_state.selected_columns:
        st.warning("⚠️ Please select at least one column to visualize")
    else:
        df_orig = pd.read_pickle(os.path.join(output_dir, "data.pkl"))
        if st.session_state.plot_type == "Split":
            plot_df(df_orig, st.session_state.selected_columns, start=st.session_state.start_datetime, end=st.session_state.end_datetime)
        else:
            plot_df_twinx(df_orig, st.session_state.selected_columns, start=st.session_state.start_datetime, end=st.session_state.end_datetime)

st.sidebar.markdown("---")


# # Botão para download do arquivo CSV
# if st.sidebar.button("Download CSV file"):
#     output_csv_path = os.path.join(output_dir, "data.csv")
#     with open(output_csv_path, "rb") as f:
#         st.download_button("Download data.csv", f, file_name="data.csv")


# --- Definição de Variáveis (Ajuste para seu ambiente) ---
output_dir = "data" # Exemplo: Ajuste para o diretório correto
output_csv_path = os.path.join(output_dir, "data.csv")

st.sidebar.write("Historic log data:")

# Verifica se o arquivo existe antes de tentar abrir
if os.path.exists(output_csv_path):
    try:
        # Abre o arquivo em modo binário ('rb') e usa o 'with open' 
        # para garantir que o recurso seja fechado corretamente.
        with open(output_csv_path, "rb") as f:
            file_data = f.read()
        
        # O st.download_button renderiza um botão que, quando clicado, 
        # usa os dados binários (file_data) para iniciar o download.
        st.sidebar.download_button(
            label="⬇️ Download",
            data=file_data,
            file_name="data.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        # Mensagem de erro caso haja problemas na leitura do arquivo
        st.sidebar.error(f"Erro ao ler o arquivo para download: {e}")
        
else:
    # Mensagem se o arquivo ainda não foi gerado ou não for encontrado
    st.sidebar.warning("Arquivo 'data.csv' não encontrado no diretório de saída.")


st.sidebar.write("02 sep 2025 - 08 dec 2025")
st.sidebar.markdown("---")


st.sidebar.write("version 1.00")