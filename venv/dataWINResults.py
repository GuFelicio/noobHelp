import pandas as pd

# Carregar os dados limpos do CSV
data_path = r"F:\Devs\helpNBlol\match_details_processed.csv"  # Arquivo gerado no passo anterior
data = pd.read_csv(data_path, low_memory=False)

# Função para determinar o resultado do jogador com base nos dados processados
def get_player_result(row):
    return 'Win' if row['participant_win'] == True else 'Loss'

# Aplicar a função na coluna 'participant_win' para criar uma nova coluna 'gameResult'
data['gameResult'] = data.apply(get_player_result, axis=1)

# Verificar as primeiras linhas para confirmar a nova coluna
print(data[['participant_summonerName', 'gameResult']].head())

# Salvar os dados transformados
output_path = r"F:\Devs\helpNBlol\match_details_results.csv"
data.to_csv(output_path, index=False)
print(f"Dados com resultados armazenados em {output_path}")
