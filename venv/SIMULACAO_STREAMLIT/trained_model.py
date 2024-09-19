import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Carregar os dados transformados do CSV
data_path = r"F:\Devs\helpNBlol\match_details_transformed.csv"
data = pd.read_csv(data_path)

# Codificar 'gameResult' de categórico ('Win', 'Loss') para numérico (1, 0)
label_encoder = LabelEncoder()
data['gameResult'] = label_encoder.fit_transform(data['gameResult'])

# Salvar o LabelEncoder para uso posterior
label_encoder_path = r"F:\Devs\helpNBlol\label_encoder.pkl"
joblib.dump(label_encoder, label_encoder_path)

# Definir as colunas de entrada (X) e a coluna de saída (y)
X = data.drop(columns=['gameResult'])
y = data['gameResult']

# Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Salvar o melhor modelo
model_path = r"F:\Devs\helpNBlol\best_model.pkl"
joblib.dump(model, model_path)
