import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import time  # Import necessário para a pausa

# Caminho da pasta onde os arquivos JSON estão armazenados
LOCAL_STORAGE_PATH = r"F:\Devs\helpNBlol"

# Lista para armazenar todos os DataFrames
dataframes = []

# Definir colunas esperadas
expected_columns = [
    'info.participants.totalDamageDealtToChampions', 'info.participants.kills', 'info.participants.deaths',
    'info.participants.assists', 'info.participants.goldEarned', 'info.gameDuration',
    'info.participants.towerKills', 'info.participants.dragonKills', 'info.participants.baronKills',
    'info.participants.inhibitorKills', 'info.participants.wardsPlaced', 'info.participants.wardsKilled',
    'info.participants.visionScore'
]

# Carregar todos os arquivos JSON na pasta especificada
for filename in os.listdir(LOCAL_STORAGE_PATH):
    if filename.endswith('.json'):
        file_path = os.path.join(LOCAL_STORAGE_PATH, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            # Carregar o arquivo JSON e convertê-lo em um DataFrame
            data_json = json.load(file)
            # Transformar o JSON em DataFrame; ajuste conforme a estrutura do JSON
            df = pd.json_normalize(data_json)

            # Adicionar colunas ausentes com NaN
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = pd.NA  # Preencher com NaN se a coluna estiver ausente

            dataframes.append(df)

# Concatenar todos os DataFrames em um único DataFrame
data = pd.concat(dataframes, ignore_index=True)

# Remover colunas que estão completamente ausentes (todas as entradas são NaN)
data = data.dropna(axis=1, how='all')

# Lista de características numéricas a serem analisadas para outliers
features_to_analyze = [
    'info.participants.totalDamageDealtToChampions', 'info.participants.kills', 'info.participants.deaths',
    'info.participants.assists', 'info.participants.goldEarned', 'info.gameDuration',
    'info.participants.towerKills', 'info.participants.dragonKills', 'info.participants.baronKills',
    'info.participants.inhibitorKills', 'info.participants.wardsPlaced', 'info.participants.wardsKilled',
    'info.participants.visionScore'
]

# Detectar e tratar outliers para cada característica
for feature in features_to_analyze:
    if feature in data.columns:
        # Visualização inicial dos dados
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        sns.boxplot(data[feature])
        plt.title(f"Boxplot de {feature}")
        plt.show()

        time.sleep(2)  # Pausa de 2 segundos para evitar excesso de requisições

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 2)
        sns.histplot(data[feature], bins=30, kde=True)
        plt.title(f"Histograma de {feature}")
        plt.show()

        time.sleep(2)  # Pausa de 2 segundos para evitar excesso de requisições

        # Calcular o IQR para detectar outliers
        Q1 = data[feature].quantile(0.25)
        Q3 = data[feature].quantile(0.75)
        IQR = Q3 - Q1

        # Definir limites inferior e superior
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filtrar os dados para remover os outliers
        data = data[(data[feature] >= lower_bound) & (data[feature] <= upper_bound)]

        # Visualizar dados após remoção de outliers
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        sns.boxplot(data[feature])
        plt.title(f"Boxplot de {feature} (Sem Outliers)")
        plt.show()

        time.sleep(2)  # Pausa de 2 segundos para evitar excesso de requisições

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 2)
        sns.histplot(data[feature], bins=30, kde=True)
        plt.title(f"Histograma de {feature} (Sem Outliers)")
        plt.show()

        time.sleep(2)  # Pausa de 2 segundos para evitar excesso de requisições

# Salvar os dados limpos em um arquivo CSV
output_path = r"F:\Devs\helpNBlol\match_details_cleaned.csv"
data.to_csv(output_path, index=False)
print(f"Dados tratados armazenados em {output_path}")
