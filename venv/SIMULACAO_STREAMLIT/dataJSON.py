import pandas as pd
import json

# Função para carregar e processar dados de partidas de JSON
def load_match_data(file_content_io):
    data_json = json.load(file_content_io)  # Carregar JSON da entrada de BytesIO no Streamlit

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

    return participants_df  # Retorna o DataFrame processado
