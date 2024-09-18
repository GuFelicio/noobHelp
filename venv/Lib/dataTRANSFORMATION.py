import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Carregar os dados limpos do CSV
data_path = r"F:\Devs\helpNBlol\match_details_cleaned.csv"
data = pd.read_csv(data_path)

# Exibir todas as colunas disponíveis no DataFrame
print("Colunas disponíveis:", data.columns.tolist())

# Definir as colunas categóricas e numéricas baseadas nas colunas disponíveis
categorical_features = ['info.gameMode', 'info.gameType']  # Ajuste conforme as colunas do seu CSV
numerical_features = [
    'info.gameDuration'
]

# Verifique se as colunas categóricas existem no DataFrame antes de prosseguir
categorical_features = [col for col in categorical_features if col in data.columns]
numerical_features = [col for col in numerical_features if col in data.columns]

# Tratamento de valores ausentes
data[categorical_features] = data[categorical_features].fillna('Unknown')
data[numerical_features] = data[numerical_features].fillna(data[numerical_features].mean())

# Pipeline para transformação de características
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', drop='first'), categorical_features)
    ]
)

# Ajustar o pré-processador aos dados
preprocessor.fit(data)

# Aplicar transformações
data_transformed = preprocessor.transform(data)

# Recalcular nomes de colunas para características categóricas
columns_num = numerical_features
columns_cat = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
columns = list(columns_num) + list(columns_cat)

# Converter o resultado para DataFrame para manter a interpretabilidade
data_transformed_df = pd.DataFrame(data_transformed, columns=columns)

# Salvar os dados transformados
output_path = r"F:\Devs\helpNBlol\match_details_transformed.csv"
data_transformed_df.to_csv(output_path, index=False)
print(f"Dados transformados armazenados em {output_path}")
