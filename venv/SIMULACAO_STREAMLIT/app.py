import streamlit as st
from streamlit_simulation import run_simulation

# Título da Aplicação
st.title('Simulação de Partida com Comparação')

# Área para upload do arquivo JSON
uploaded_file = st.file_uploader("Faça o upload do arquivo JSON da partida", type="json")

# Verifique se o arquivo foi enviado
if uploaded_file is not None:
    # Mostrar uma mensagem de progresso
    with st.spinner('Processando o arquivo JSON...'):
        comparison_df = run_simulation(uploaded_file)  # Passar o arquivo para a função run_simulation

    # Exibir os resultados
    st.write("Resultado da Comparação:")
    st.dataframe(comparison_df)

    # Exibir a acurácia ou outros insights
    total_predictions = len(comparison_df)
    correct_predictions = (comparison_df['Real Result'] == comparison_df['Predicted Result']).sum()
    st.write(f"Acurácia: {correct_predictions / total_predictions:.2f}")
else:
    st.info("Por favor, faça o upload do arquivo JSON para iniciar a simulação.")
