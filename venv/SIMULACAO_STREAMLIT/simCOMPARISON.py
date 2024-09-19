import pandas as pd

# Função para comparar os resultados do jogo real com a previsão do modelo
def compare_results(data, model):
    # Separar as características (X) e o resultado real (y)
    X = data.drop(columns=['gameResult'])  # Excluir a coluna 'gameResult' que contém o resultado real
    y_real = data['gameResult']  # Resultado real (Win/Loss)

    # Fazer previsões com o modelo treinado
    y_pred = model.predict(X)

    # Comparação entre o placar real e o previsto
    comparison_df = pd.DataFrame({
        'Real Result': y_real,
        'Predicted Result': y_pred,
        'Summoner Name': data['participant_summonerName']
    })

    return comparison_df
