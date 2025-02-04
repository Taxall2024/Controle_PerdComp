
import pandas as pd
import streamlit as st
import numpy as np



st.set_page_config( layout='wide')


class ControlePerdComp():

  def __init__(self):
    self.primeira_regra = False
    self.segunda_regra = False


    self.lista_dfs_tratados = []

    self.dataframe_primeira_regra = pd.DataFrame()
    self.dataframe_segunda_regra = pd.DataFrame()

  def read_file(self,file_path):

      #arquivo = pd.read_csv(r"C:\Users\lauro.loyola\Desktop\Teste\consolidado.csv", sep=';')
      self.arquivo = pd.read_csv(file_path, sep=';')
      print(self.arquivo.columns)
      return self.arquivo
      
  def preparando_arquivos_para_edciao(self):
      numero_per = self.arquivo['PER/DCOMP'].drop_duplicates()
      numero_perd_inicial =self.arquivo['PER/DCOMP inicial'].drop_duplicates()
      print('Contagem numero PERD')
      print(numero_perd_inicial.count())

      #arquivo = arquivo[~arquivo['Tipo de documento'].str.contains('Pedido Cancelamento')]

      self.arquivo['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'] = self.arquivo['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].str.replace('.', '').str.replace(',', '.')
      self.arquivo['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'] = pd.to_numeric(self.arquivo['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'])

      self. arquivo['Vl. Crédito Dt. Transmissão'] = self.arquivo['Vl. Crédito Dt. Transmissão'].str.replace('.', '').str.replace(',', '.')
      self.arquivo['Vl. Crédito Dt. Transmissão'] = pd.to_numeric(self.arquivo['Vl. Crédito Dt. Transmissão'])

      self.arquivo['Vl. Total Crédito'] = self.arquivo['Vl. Total Crédito'].str.replace('.', '').str.replace(',', '.')
      self.arquivo['Vl. Total Crédito'] = pd.to_numeric(self.arquivo['Vl. Total Crédito'])



      self.arquivo['Data de transmissão'] = pd.to_datetime(self.arquivo['Data de transmissão'], format='%d/%m/%Y')


      return self.arquivo

  def filtragem_de_dados(self,numero_perd_inicial:str):


    self.seletor_perd = numero_perd_inicial
    self.tabela_exibicao = self.arquivo[self.arquivo['PER/DCOMP inicial'] == numero_perd_inicial]

  def primeira_regra_filtragem(self):
  # Primeira regra de negocios
    
    self.valor_a_subtrair = self.arquivo.loc[self.arquivo['PER/DCOMP'] == self.seletor_perd, 'Vl. Total Crédito'].values[0]
    somatorio_credito_utilizado = self.tabela_exibicao['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].sum()
    dataframe_condicional_dois = self.tabela_exibicao.loc[self.tabela_exibicao['PER/DCOMP'] != self.seletor_perd]
    valor_condicional_dois = round(dataframe_condicional_dois['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].sum(),2)
    valor_final_dois = round(self.valor_a_subtrair - valor_condicional_dois,2)

    # Primeira condicional


    valor_a_subtrair = self.arquivo.loc[self.arquivo['PER/DCOMP'] == self.seletor_perd]

    if valor_a_subtrair['Situação'].iloc[0] in ['Análise concluída','Análise concluída''Homologado', 'PER deferido']:
         self.tabela_exibicao['Resultado'] = 0
     
    if valor_a_subtrair['Situação'].iloc[0] not in ['Análise concluída','Análise concluída''Homologado', 'PER deferido']:
      self.tabela_exibicao['Resultado'] = np.where(~
          self.tabela_exibicao['Situação'].isin(['Retificado', 'Cancelado', 'Pedido de cancelamento deferido', 'Despacho decisório deferido', 'Em discussão administrativa - DRJ']),
                np.where(self.tabela_exibicao['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].iloc[0] != self.tabela_exibicao['Vl. Crédito Dt. Transmissão'].iloc[0],
                                                                                        self.valor_a_subtrair - somatorio_credito_utilizado,
                                                                                          valor_final_dois), 0 )
    

    print('Primeira regra de filtragem DENTRO DA FUNÇÃO DA PRIMEIRA REGRA ---___--->>>>>', self.primeira_regra)

    if self.tabela_exibicao['Resultado'].any() > 0:
        self.tabela_exibicao['Resultado'] = self.tabela_exibicao['Resultado'].max()
    if self.tabela_exibicao['Resultado'].any() < 0:
        self.tabela_exibicao['Resultado'] = 0
    if valor_a_subtrair['Tipo de documento'].iloc[0] == 'Decl. Compensação':
        self.tabela_exibicao['Resultado'] = 0
    if  self.arquivo.loc[self.arquivo['PER/DCOMP'] == self.seletor_perd, 'Retificado/Cancelado por'].any() != 'Retificado':
        self.lista_dfs_tratados.append(self.tabela_exibicao)

    #st.subheader('Primeira regra de filtragem')
    #st.dataframe(self.tabela_exibicao)


    self.dataframe_primeira_regra = self.tabela_exibicao


    return self.dataframe_primeira_regra , self.primeira_regra

  def segunda_regra_filtragem(self):

    somatorio_credito_utilizado = self.tabela_exibicao.loc[
            ~self.tabela_exibicao['Situação'].isin(['Retificado', 'Cancelado',
                                                     'Pedido de cancelamento deferido', 
                                                     'Despacho decisório emitido', 'Em discussão administrativa - DRJ']), 'Vl. Total Crédito'].sum()
    
    def get_last_row(df):

        num_perd = self.seletor_perd
        
        row = df[df['PER/DCOMP'] == num_perd]
        perd_final = df[df['PER/DCOMP'] == row['Retificado/Cancelado por'].iloc[0]]
        while True:
           if perd_final['Retificado/Cancelado por'].any():
              row = df[df['PER/DCOMP'] == perd_final['Retificado/Cancelado por'].iloc[0]]
              perd_final = df[df['PER/DCOMP'] == row['Retificado/Cancelado por'].iloc[0]]
           else:
              break

                
        return perd_final
    

    
    self.abela_exibicao_condicional_dois = get_last_row(self.tabela_exibicao)

    somatario_cred_utilizado_condicional_dois = self.tabela_exibicao['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].sum() - self.abela_exibicao_condicional_dois['Vl. Crédito Dt. Transmissão'].sum()
    valor_final_segunda_condicional = round(self.abela_exibicao_condicional_dois['Vl. Total Crédito'] - somatorio_credito_utilizado,2)

    #Regra numero 2 dentro no segundo np.where- -- ---
    dataframe_sem_per_recente = self.tabela_exibicao.loc[self.tabela_exibicao['PER/DCOMP'] != self.abela_exibicao_condicional_dois['PER/DCOMP'].iloc[0]]


    dataframe_sem_per_recente = dataframe_sem_per_recente.loc[
            ~dataframe_sem_per_recente['Situação'].isin(['Retificado', 'Cancelado',
                                                     'Pedido de cancelamento deferido', 
                                                     'Despacho decisório emitido', 'Em discussão administrativa - DRJ']),
            'Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'
        ].sum()

    
    valor_final_tecerira_condicional = round(self.abela_exibicao_condicional_dois['Vl. Total Crédito'] - dataframe_sem_per_recente,2)

    print('SHAPE SEGUNDA CONDICIONAL SEGUNDA REGRA ----->>>>     :', valor_final_segunda_condicional)
    print('SHAPE SEGUNDA CONDICIONAL TERCEIRA REGRA ----->>>>     :', valor_final_tecerira_condicional)

    valor_final_segunda_condicional_array = np.full(
    len(self.tabela_exibicao), valor_final_segunda_condicional
    )
    valor_final_tecerira_condicional_array = np.full(
        len(self.tabela_exibicao), valor_final_tecerira_condicional
    )
      #Segunda condicional

    if self.abela_exibicao_condicional_dois['Situação'].iloc[0] in ['Análise concluída', 'Homologado', 'PER deferido']:
         self.tabela_exibicao['Resultado'] = 0
   
    if self.abela_exibicao_condicional_dois['Situação'].iloc[0] not in ['Análise concluída', 'Homologado', 'PER deferido']:
      self.tabela_exibicao['Resultado'] = np.where(~self.tabela_exibicao['Situação'].isin(['Retificado', 'Cancelado',
                                                                                         'Pedido de cancelamento deferido','Despacho decisório emitido',
                                                                                         'Em discussão administrativa - DRJ']),
                    np.where(self.abela_exibicao_condicional_dois['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].iloc[0] != self.abela_exibicao_condicional_dois['Vl. Crédito Dt. Transmissão'].iloc[0],
                                                                                          valor_final_segunda_condicional_array,
                                                                                            valor_final_tecerira_condicional_array), 
                                                                                                0, )

    self.dataframe_segunda_regra = self.tabela_exibicao

    if self.tabela_exibicao['Resultado'].any() > 0:
        self.tabela_exibicao['Resultado'] = self.tabela_exibicao['Resultado'].max()
    if self.tabela_exibicao['Resultado'].any() < 0:
        self.tabela_exibicao['Resultado'] = 0
    if self.abela_exibicao_condicional_dois['Tipo de documento'].iloc[0] == 'Decl. Compensação':        
      self.tabela_exibicao['Resultado'] = 0
    if  self.abela_exibicao_condicional_dois.loc[self.abela_exibicao_condicional_dois['Situação'] == 'Retificado' ].empty:
        self.lista_dfs_tratados.append(self.tabela_exibicao)



    #st.subheader('Segunda regra de filtragem')
    #st.dataframe(self.tabela_exibicao)
    return self.dataframe_segunda_regra, self.segunda_regra
  
  def aplicar_regras(self):
      try:
          self.primeira_regra_filtragem()
          self.segunda_regra_filtragem()

      except Exception as e:
          print('Error : Regra número 1 : --->', e)
          print('Error : Regra número 2 : --->', e)
      
  def main(self):
    self.read_file(r"C:\Users\lauro.loyola\Desktop\Tax\Controle PerdComp\consolidado.csv")
    self.preparando_arquivos_para_edciao()
    
    numero_perd_inicial =self.arquivo['PER/DCOMP inicial'].drop_duplicates()
    for i in numero_perd_inicial:
      self.filtragem_de_dados(i)
      self.primeira_regra_filtragem()
      try:
        self.segunda_regra_filtragem()
      except Exception as e:
        print('Error : Regra número 1 : --->', e)
    data_frame_final = pd.concat(self.lista_dfs_tratados)
    
    valor_total = data_frame_final['Resultado'].drop_duplicates().sum()
    valor_total_formatado = f"{valor_total:,.2f}" 
    st.metric(label='Valor total', value=valor_total_formatado)
    

    st.write('')
    st.write('')
    st.write('')

    seletor_perd = st.sidebar.selectbox('Selecione o PER/DCOMP', data_frame_final['PER/DCOMP inicial'].drop_duplicates())
    dataframe_filtrado_pelo_seletor = data_frame_final.loc[data_frame_final['PER/DCOMP inicial'] == seletor_perd]
    st.subheader('Cadeias de PER/DCOMP')
    st.dataframe(dataframe_filtrado_pelo_seletor)



    with st.expander('PER/DCOMP com valores maiores que zero'):
      df_com_valores = data_frame_final.loc[data_frame_final['Resultado'] > 0]
      df_com_valores = df_com_valores.drop_duplicates(subset='Resultado').reset_index(drop=True)
      st.subheader('PER/DCOMP com valores')
      st.dataframe(df_com_valores)
    
    with st.expander('Tabela com todas as PER/DCOMP'):
      st.subheader('Dataframe final')
      st.dataframe(data_frame_final)

    print('Lista de dataframes tratados -----------> ', self.lista_dfs_tratados)
    return self.lista_dfs_tratados



ct = ControlePerdComp()
ct.main()



