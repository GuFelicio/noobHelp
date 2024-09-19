import streamlit as st
import pandas as pd
from simCOMPARISON import compare_results
from dataJSON import load_match_data
import joblib

# Função principal para rodar a simulação
def run_simulation(file_content_io):
    # Carregar e processar o arquivo JSON enviado
    participants_df = load_match_data(file_content_io)

    # Carregar o modelo treinado de Machine Learning (ajustar o caminho conforme necessário)
    model_path = r"F:\Devs\helpNBlol\best_model.pkl"
    model = joblib.load(model_path)

    # Realizar a comparação e obter os resultados da simulação
    comparison_df = compare_results(participants_df, model)

    return comparison_df

