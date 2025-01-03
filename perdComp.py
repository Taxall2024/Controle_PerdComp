


st.set_page_config(page_title='Filtro PER/DCOMP', layout='wide')

arquivo = pd.read_csv(r"C:\Users\lauro.loyola\Desktop\Teste\consolidado.csv", sep=';')

numero_per = arquivo['PER/DCOMP'].drop_duplicates()
numero_perd_inicial = arquivo['PER/DCOMP inicial'].drop_duplicates()
print('Contagem numero PERD')
print(numero_perd_inicial.count())

seletor_perd = st.sidebar.selectbox('Selecione o PER/DCOMP:',options=numero_perd_inicial)
#arquivo = arquivo[~arquivo['Tipo de documento'].str.contains('Pedido Cancelamento')]

# Replace commas with dots and convert to numeric
arquivo['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'] = arquivo['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].str.replace('.', '').str.replace(',', '.')
arquivo['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'] = pd.to_numeric(arquivo['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'])

arquivo['Vl. Crédito Dt. Transmissão'] = arquivo['Vl. Crédito Dt. Transmissão'].str.replace('.', '').str.replace(',', '.')
arquivo['Vl. Crédito Dt. Transmissão'] = pd.to_numeric(arquivo['Vl. Crédito Dt. Transmissão'])

arquivo['Vl. Total Crédito'] = arquivo['Vl. Total Crédito'].str.replace('.', '').str.replace(',', '.')
arquivo['Vl. Total Crédito'] = pd.to_numeric(arquivo['Vl. Total Crédito'])



arquivo['Data de transmissão'] = pd.to_datetime(arquivo['Data de transmissão'], format='%d/%m/%Y')

tabela_exibicao = arquivo[arquivo['PER/DCOMP inicial'] == seletor_perd]

# Primeira regra de negocios

valor_a_subtrair = arquivo.loc[arquivo['PER/DCOMP'] == seletor_perd, 'Vl. Total Crédito'].values[0]
somatorio_credito_utilizado = tabela_exibicao['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].sum()




dataframe_condicional_dois = tabela_exibicao.loc[tabela_exibicao['PER/DCOMP'] != seletor_perd]
valor_condicional_dois = round(dataframe_condicional_dois['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].sum(),2)
valor_final_dois = round(valor_a_subtrair - valor_condicional_dois,2)

 
st.dataframe(dataframe_condicional_dois)



def get_last_row(df):

  df_filtrado = df[df['Situação'] == 'Retificado']
  lista_retificados_cacelados =  df_filtrado['Retificado/Cancelado por']
  perd_final = df[(df['PER/DCOMP'].isin(lista_retificados_cacelados))&(df['Retificado/Cancelado por'].isna())]


  return perd_final

tabela_exibicao_condicional_dois = get_last_row(tabela_exibicao)

somatario_cred_utilizado_condicional_dois = tabela_exibicao['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].sum() - tabela_exibicao_condicional_dois['Vl. Crédito Dt. Transmissão'].sum()

valor_final_segunda_condicional = round(tabela_exibicao_condicional_dois['Vl. Total Crédito'] - somatorio_credito_utilizado,2)


# Primeira condicional
tabela_exibicao['Resultado'] = np.where(~
      tabela_exibicao['Situação'].isin(['Retificado', 'Cancelado', 'Pedido de cancelamento deferido', 'Despacho decisório deferido', 'Em discussão administrativa - DRJ']),
            np.where(tabela_exibicao['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].iloc[0] != tabela_exibicao['Vl. Crédito Dt. Transmissão'].iloc[0],
                                                                                    valor_a_subtrair - somatorio_credito_utilizado,
                                                                                      valor_final_dois),
                                                                                                         0 )

#Segunda condicional
tabela_exibicao['Resultado'] = np.where(~ tabela_exibicao['Situação'].isin(['Retificado', 'Cancelado','Pedido de cancelamento deferido','Despacho decisório emitido','Em discussão administrativa - DRJ']),
              np.where(tabela_exibicao_condicional_dois['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].iloc[0] == tabela_exibicao_condicional_dois['Vl. Crédito Dt. Transmissão'].iloc[0],
                                                                                    valor_final_segunda_condicional,
                                                                                      valor_final_dois), 
                                                                                           0, )


tabela_big_number = arquivo.sort_values(by='Data de transmissão', ascending=False).drop_duplicates(subset='PER/DCOMP inicial', keep='first').reset_index()







#big_number = 

st.dataframe(tabela_exibicao)
st.dataframe(arquivo)
print(arquivo.info())