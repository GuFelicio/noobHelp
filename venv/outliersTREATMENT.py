import pandas as pd
import os
import json

# Caminho da pasta onde os arquivos JSON estão armazenados
LOCAL_STORAGE_PATH = r"F:\Devs\helpNBlol\arquivosJSON"

# Lista para armazenar todos os DataFrames
dataframes = []


# Função para carregar e processar dados de partidas de JSON
def load_match_data(file_path):
    # Abrir o arquivo JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        data_json = json.load(file)

        # Normalizar participantes
        participants_df = pd.json_normalize(data_json['info']['participants'])
        participants_df.columns = ['participant_' + col for col in participants_df.columns]

        # Normalizar os times
        teams_df = pd.json_normalize(data_json['info']['teams'])
        teams_df.columns = ['team_' + col for col in teams_df.columns]

        # Incluir detalhes do jogo
        game_details = pd.json_normalize(data_json['info']).drop(columns=['participants', 'teams'])
        game_details.columns = ['game_' + col for col in game_details.columns]

        # Adicionar o resultado da partida (Vitória ou Derrota)
        participants_df['gameResult'] = participants_df.apply(
            lambda row: 'Win' if row['participant_teamId'] ==
                                 teams_df.loc[teams_df['team_win'] == True, 'team_teamId'].values[0] else 'Loss', axis=1
        )

        # Concatenar os dados
        game_details_df = pd.concat([participants_df, teams_df, game_details], axis=1)

        return game_details_df


# Carregar todos os arquivos JSON na pasta especificada
for filename in os.listdir(LOCAL_STORAGE_PATH):
    if filename.endswith('.json'):
        file_path = os.path.join(LOCAL_STORAGE_PATH, filename)
        df = load_match_data(file_path)
        dataframes.append(df)

# Concatenar todos os DataFrames em um único DataFrame
data = pd.concat(dataframes, ignore_index=True)

# Salvar os dados tratados em CSV
output_path = r"F:\Devs\helpNBlol\match_details_processed.csv"
data.to_csv(output_path, index=False)

print(f"Dados processados armazenados em {output_path}")
