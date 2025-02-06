# Controle PerdComp

Este projeto tem como objetivo realizar a filtragem e aplicação de regras de negócios em arquivos CSV contendo dados de PER/DCOMP. O código foi desenvolvido em Python e utiliza bibliotecas como `pandas` e `streamlit` para manipulação de dados e interface de usuário, respectivamente.

## Funcionalidades

- **Leitura de Arquivos**: Carrega arquivos CSV contendo dados de PER/DCOMP.
- **Preparação de Dados**: Realiza a limpeza e formatação dos dados para garantir a consistência.
- **Filtragem de Dados**: Filtra os dados com base em critérios específicos.
- **Aplicação de Regras de Negócios**: Aplica duas regras de negócios para calcular o valor final de crédito.
- **Interface de Usuário**: Utiliza `streamlit` para permitir a seleção de arquivos e exibição dos resultados.

## Estrutura do Código

### Métodos Principais

- **`read_file(self, file)`**: Lê o arquivo CSV e carrega os dados em um DataFrame do pandas.
- **`preparando_arquivos_para_edciao(self)`**: Prepara os dados para edição, realizando a limpeza e formatação necessárias.
- **`filtragem_de_dados(self, numero_perd_inicial: str)`**: Filtra os dados com base no número PERD inicial.
- **`primeira_regra_filtragem(self)`**: Aplica a primeira regra de negócios para calcular o valor final de crédito.
- **`segunda_regra_filtragem(self)`**: Aplica a segunda regra de negócios para calcular o valor final de crédito.
- **`aplicar_regras(self)`**: Aplica ambas as regras de negócios.
- **`main(self)`**: Método principal que coordena a execução do código, incluindo a leitura do arquivo, preparação dos dados, aplicação das regras e exibição dos resultados.

### Exemplo de Uso

1. **Upload do Arquivo**: O usuário faz o upload de um arquivo CSV contendo os dados de PER/DCOMP.
2. **Preparação dos Dados**: O método `preparando_arquivos_para_edciao` é chamado para limpar e formatar os dados.
3. **Filtragem e Aplicação de Regras**: Os métodos `filtragem_de_dados`, `primeira_regra_filtragem` e `segunda_regra_filtragem` são chamados para filtrar os dados e aplicar as regras de negócios.
4. **Exibição dos Resultados**: Os resultados são exibidos na interface do `streamlit`.

### Dependências

- `pandas`
- `streamlit`
- `numpy`

### Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/controle-perdcomp.git

   cd controle-perdcomp

   pip install -r requirements.txt

   streamlit run filtro_perd.py
from graphviz import Digraph

dot = Digraph()

dot.node('A', 'read_file')
dot.node('B', 'preparando_arquivos_para_edciao')
dot.node('C', 'filtragem_de_dados')
dot.node('D', 'primeira_regra_filtragem')
dot.node('E', 'segunda_regra_filtragem')
dot.node('F', 'aplicar_regras')
dot.node('G', 'main')

dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG'])

dot.render('organograma', format='png', view=True)
