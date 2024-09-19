import pandas as pd

# Carregar os dados
data_path = r"F:\Devs\helpNBlol\match_details_transformed.csv"
data = pd.read_csv(data_path)

# Exibir todas as colunas disponíveis no DataFrame
print("Colunas disponíveis:", data.columns.tolist())