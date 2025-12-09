import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- FUNÇÃO 1: Múltiplos Subplots (Originalmente plot_df) ---

def plot_df(df, columns, start=None, end=None):
    """
    Plota colunas em múltiplos subplots verticais no Streamlit.

    Args:
        df (pd.DataFrame): O DataFrame a ser plotado.
        columns (list): Lista de nomes de colunas a serem plotadas.
        start (str, optional): Data de início para filtragem.
        end (str, optional): Data de fim para filtragem.
    """
    # Garante que a coluna 'Data' está em formato datetime
    df['Data'] = pd.to_datetime(df['Data'])

    # --- Lógica de Filtragem (Mantida) ---
    tz = df['Data'].dt.tz
    if start is not None:
        start_dt = pd.to_datetime(start)
        if tz is not None and start_dt.tzinfo is None:
            start_dt = start_dt.tz_localize(tz)
        df = df[df['Data'] >= start_dt]
    if end is not None:
        end_dt = pd.to_datetime(end)
        if tz is not None and end_dt.tzinfo is None:
            end_dt = end_dt.tz_localize(tz)
        df = df[df['Data'] <= end_dt]

    cols_to_plot = [col for col in columns if col in df.columns]
    n = len(cols_to_plot)
    
    if n == 0:
        st.warning("Nenhuma coluna válida selecionada para plotar.")
        return

    # --- Criação do Gráfico Matplotlib ---
    # fig, axs = plt.subplots(n, 1, ...) - Cria a Figura e os Eixos
    fig, axs = plt.subplots(n, 1, figsize=(12, 4 * n), sharex=True)
    
    if n == 1:
        axs = [axs]
        
    for i, col in enumerate(cols_to_plot):
        axs[i].plot(df['Data'], df[col], linestyle='-')
        axs[i].set_title(f'{col}', fontsize=10) # Título ajustado para melhor visualização
        axs[i].set_ylabel(col)
        axs[i].grid(True)
        
    axs[-1].set_xlabel('Time')
    plt.tight_layout()
    
    # --- Saída Streamlit ---
    st.pyplot(fig) # Substitui plt.show()
    plt.close(fig) # Boa prática para liberar memória

# ---------------------------------------------------------------------
# --- FUNÇÃO 2: Eixo Gêmeo (Twinx) no Streamlit (Originalmente plot_df_twinx) ---

def plot_df_twinx(df, columns, start=None, end=None):
    """
    Plota colunas em um único subplot com eixos Y independentes (twinx) no Streamlit.

    Args:
        df (pd.DataFrame): O DataFrame a ser plotado.
        columns (list): Lista de nomes de colunas a serem plotadas.
        start (str, optional): Data de início para filtragem.
        end (str, optional): Data de fim para filtragem.
    """
    # Garante que a coluna 'Data' está em formato datetime
    df['Data'] = pd.to_datetime(df['Data'])

    # --- Lógica de Filtragem (Mantida) ---
    tz = df['Data'].dt.tz
    if start is not None:
        start_dt = pd.to_datetime(start)
        if tz is not None and start_dt.tzinfo is None:
            start_dt = start_dt.tz_localize(tz)
        df = df[df['Data'] >= start_dt]
    if end is not None:
        end_dt = pd.to_datetime(end)
        if tz is not None and end_dt.tzinfo is None:
            end_dt = end_dt.tz_localize(tz)
        df = df[df['Data'] <= end_dt]

    cols_to_plot = [col for col in columns if col in df.columns]
    n = len(cols_to_plot)
    
    if n == 0:
        st.warning("Nenhuma coluna selecionada para plotar.")
        return

    # --- Criação do Gráfico de Eixos Gêmeos (Twinx) ---
    fig, ax1 = plt.subplots(figsize=(14, 7))
    
    fig.suptitle(' ', fontsize=8)
    
    # Eixo principal (primeira coluna)
    color = 'tab:blue'
    col1 = cols_to_plot[0]
    ax1.set_xlabel('Time')
    ax1.set_ylabel(col1, color=color)
    line1 = ax1.plot(df['Data'], df[col1], color=color, linestyle='-', label=col1)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)
    
    lines = line1
    
    # Eixos gêmeos para as colunas restantes
    for i in range(1, n):
        col = cols_to_plot[i]
        
        ax_new = ax1.twinx()
        
        # Desloca o eixo Y para evitar sobreposição (se houver mais de 2 colunas)
        if i > 1:
            ax_new.spines['right'].set_position(('axes', 1.0 + 0.15 * (i-1)))
        
        color = f'C{i}'
        
        line_new = ax_new.plot(df['Data'], df[col], color=color, linestyle='-', label=col)
        ax_new.set_ylabel(col, color=color)
        ax_new.tick_params(axis='y', labelcolor=color)
        
        lines += line_new

    # Adiciona a legenda e ajusta o layout
    ax1.legend(lines, [l.get_label() for l in lines], loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=8)
   
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # --- Saída Streamlit ---
    st.pyplot(fig) # Substitui plt.show()
    plt.close(fig) # Boa prática para liberar memória