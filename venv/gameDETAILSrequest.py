import mysql.connector
import requests
import json
import os
import time

API_KEY = 'RGAPI-16ef65ad-4522-490f-b0d4-342abf7c6b1d'
BASE_URL = 'https://americas.api.riotgames.com'

# Configuração de Armazenamento
LOCAL_STORAGE_PATH = r"F:\Devs\helpNBlol"  # Caminho de armazenamento local

# Configuração de conexão com o banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ALTERAR SENHA",
    database="league_data"
)
cursor = db.cursor()

# Limite de requisição
REQUESTS_PER_SECOND = 20
REQUESTS_PER_2_MINUTES = 100


def match_ids_bd():
    """
    Função para obter Match IDs armazenados no banco de dados.
    """
    query = "SELECT match_id FROM matches"
    cursor.execute(query)
    match_ids = [row[0] for row in cursor.fetchall()]
    return match_ids


def detalhes_partida(match_id):
    """
    Função para coletar dados detalhados da partida usando a API da Riot Games.
    """
    url = f"{BASE_URL}/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Dados da partida {match_id} coletados com sucesso.")
        return response.json()  # Retorna o JSON diretamente
    else:
        print(f"Erro ao coletar dados da partida {match_id}: {response.status_code}")
        return None


def armazenar_dados_local(match_id, dados):
    """
    Função para armazenar dados localmente em arquivos JSON.
    """
    caminho_arquivo = os.path.join(LOCAL_STORAGE_PATH, f"{match_id}.json")
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)  # Cria diretórios, se necessário
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    print(f"Dados da partida {match_id} armazenados localmente em {caminho_arquivo}")


def main():
    # Obtém os Match IDs do banco de dados
    match_ids = match_ids_bd()

    # Inicializa o controle de taxa de requisição
    start_time_interval = time.time()
    requests_made = 0

    for match_id in match_ids:
        # Controle de taxa de requisição
        if requests_made >= REQUESTS_PER_SECOND:
            elapsed_time = time.time() - start_time_interval
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)  # Aguarda o tempo necessário
            start_time_interval = time.time()
            requests_made = 0

        # Coleta dados detalhados da partida
        dados_partida = detalhes_partida(match_id)
        if dados_partida:
            armazenar_dados_local(match_id, dados_partida)

        requests_made += 1
        time.sleep(1 / REQUESTS_PER_SECOND)  # Pausa para respeitar o limite de taxa de requisição


if __name__ == "__main__":
    main()
