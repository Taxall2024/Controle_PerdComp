
import pandas as pd
import streamlit as st
import numpy as np



st.set_page_config(page_title='Filtro PER/DCOMP', layout='wide')


class ControlePerdComp():

  def read_file(self,file_path):

      #arquivo = pd.read_csv(r"C:\Users\lauro.loyola\Desktop\Teste\consolidado.csv", sep=';')
      self.arquivo = pd.read_csv(file_path, sep=';')
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

  def filtragem_de_dados(self):

    numero_perd_inicial =self.arquivo['PER/DCOMP inicial'].drop_duplicates()
    self.seletor_perd = st.sidebar.selectbox('Selecione o PER/DCOMP:',options=numero_perd_inicial)
    self.tabela_exibicao = self.arquivo[self.arquivo['PER/DCOMP inicial'] == self.seletor_perd]


  def primeira_regra_filtragem(self):
  # Primeira regra de negocios
    
    self.valor_a_subtrair = self.arquivo.loc[self.arquivo['PER/DCOMP'] == self.seletor_perd, 'Vl. Total Crédito'].values[0]
    somatorio_credito_utilizado = self.tabela_exibicao['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].sum()
    dataframe_condicional_dois = self.tabela_exibicao.loc[self.tabela_exibicao['PER/DCOMP'] != self.seletor_perd]
    valor_condicional_dois = round(dataframe_condicional_dois['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].sum(),2)
    valor_final_dois = round(self.valor_a_subtrair - valor_condicional_dois,2)

    # Primeira condicional
    self.tabela_exibicao['Resultado'] = np.where(~
          self.tabela_exibicao['Situação'].isin(['Retificado', 'Cancelado', 'Pedido de cancelamento deferido', 'Despacho decisório deferido', 'Em discussão administrativa - DRJ']),
                np.where(self.tabela_exibicao['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].iloc[0] != self.tabela_exibicao['Vl. Crédito Dt. Transmissão'].iloc[0],
                                                                                        self.valor_a_subtrair - somatorio_credito_utilizado,
                                                                                          valor_final_dois),
    
                                                                                             0 )

    st.subheader('Primeira regra de filtragem')
    st.dataframe(self.tabela_exibicao)




  def segunda_regra_filtragem(self):

    somatorio_credito_utilizado = self.tabela_exibicao.loc[
            ~self.tabela_exibicao['Situação'].isin(['Retificado', 'Cancelado',
                                                     'Pedido de cancelamento deferido', 
                                                     'Despacho decisório emitido', 'Em discussão administrativa - DRJ']),
            'Vl. Total Crédito'
        ].sum()
    
    def get_last_row(df):

        df_filtrado = df[df['Situação'] == 'Retificado']
        lista_retificados_cacelados =  df_filtrado['Retificado/Cancelado por']
        perd_final = df[(df['PER/DCOMP'].isin(lista_retificados_cacelados))&(df['Retificado/Cancelado por'].isna())]


        return perd_final

    tabela_exibicao_condicional_dois = get_last_row(self.tabela_exibicao)
    somatario_cred_utilizado_condicional_dois = self.tabela_exibicao['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].sum() - tabela_exibicao_condicional_dois['Vl. Crédito Dt. Transmissão'].sum()
    valor_final_segunda_condicional = round(tabela_exibicao_condicional_dois['Vl. Total Crédito'] - somatorio_credito_utilizado,2)

    #Regra numero 2 dentro no segundo np.where- -- ---
    dataframe_sem_per_recente = self.tabela_exibicao.loc[self.tabela_exibicao['PER/DCOMP'] != tabela_exibicao_condicional_dois['PER/DCOMP'].iloc[0]]
    dataframe_sem_per_recente = dataframe_sem_per_recente.loc[
            ~dataframe_sem_per_recente['Situação'].isin(['Retificado', 'Cancelado',
                                                     'Pedido de cancelamento deferido', 
                                                     'Despacho decisório emitido', 'Em discussão administrativa - DRJ']),
            'Vl. Total Crédito'
        ].sum()

    
    valor_final_tecerira_condicional = round(tabela_exibicao_condicional_dois['Vl. Total Crédito'] - dataframe_sem_per_recente,2)

      #Segunda condicional
    self.tabela_exibicao['Resultado'] = np.where(~self.tabela_exibicao['Situação'].isin(['Retificado', 'Cancelado','Pedido de cancelamento deferido','Despacho decisório emitido','Em discussão administrativa - DRJ']),
                    np.where(tabela_exibicao_condicional_dois['Créd. Orig. Necessário Débitos DCOMP ou Valor do PER'].iloc[0] != tabela_exibicao_condicional_dois['Vl. Crédito Dt. Transmissão'].iloc[0],
                                                                                          valor_final_segunda_condicional,
                                                                                            valor_final_tecerira_condicional), 
                                                                                                0, )
    st.subheader('Segunda regra de filtragem')
    st.dataframe(self.tabela_exibicao)



ct = ControlePerdComp()
ct.read_file(r"C:\Users\lauro.loyola\Desktop\Controle PerdComp\consolidado.csv")
ct.preparando_arquivos_para_edciao()
ct.filtragem_de_dados()
ct.primeira_regra_filtragem()
ct.segunda_regra_filtragem()


