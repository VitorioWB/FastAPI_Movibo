
# FastAPI Movibo

## Descrição
FastAPI Movibo é uma aplicação web desenvolvida com FastAPI para buscar e recomendar filmes com base em dados de uma lista dos 1000 melhores filmes do IMDB.

## Funcionalidades
- Buscar filmes pelo título
- Recomendar filmes baseados em um filme específico

## Endpoints da API

### 1. Página Inicial
- **Endpoint:** `/`
- **Método:** GET
- **Descrição:** Exibe uma página inicial com formulários para buscar filmes e recomendar filmes baseados em um título.

### 2. Buscar Filmes
- **Endpoint:** `/busca/`
- **Método:** GET
- **Parâmetros de Consulta:**
  - `query` (string): O título ou parte do título do filme a ser buscado.
- **Descrição:** Busca filmes no banco de dados cujo título contenha o texto fornecido em `query`.
- **Exemplo de Uso:** 
  ```
  /busca/?query=Inception
  ```
- **Resposta:**
  ```json
  [
    {
      "Title": "Inception",
      "Genre": "Action, Adventure, Sci-Fi",
      "Director": "Christopher Nolan",
      "IMDB_Rating": 8.8,
      "Meta_score": 74.0,
      "Description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    }
  ]
  ```

### 3. Recomendar Filmes
- **Endpoint:** `/recommendados/`
- **Método:** GET
- **Parâmetros de Consulta:**
  - `title` (string): O título do filme para o qual você deseja recomendações.
- **Descrição:** Recomenda filmes que pertencem ao mesmo cluster do filme fornecido em `title`.
- **Exemplo de Uso:** 
  ```
  /recommendados/?title=Inception
  ```
- **Resposta:**
  ```json
  [
    {
      "Title": "The Dark Knight",
      "Genre": "Action, Crime, Drama",
      "Director": "Christopher Nolan",
      "IMDB_Rating": 9.0,
      "Meta_score": 84.0,
      "Description": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham."
    },
    ...
  ]
  ```

## Como Executar a Aplicação
1. Clone o repositório:
   ```sh
   git clone https://github.com/VitorioWB/FastAPI_Movibo.git
   cd FastAPI_Movibo
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```sh
   python -m venv env
   source env/bin/activate   # No Windows: env\Scripts ctivate
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```sh
   uvicorn main:app --reload
   ```

5. Abra seu navegador e acesse:
   ```
   http://127.0.0.1:8000
   ```

## Estrutura do Projeto
- **main.py:** Arquivo principal da aplicação FastAPI.
- **model.py:** Define o modelo de dados e a lógica de treinamento.
- **utils.py:** Contém funções utilitárias.
- **templates/:** Diretório que contém os templates HTML para as páginas da aplicação.
- **imdb_top_1000.csv:** Base de dados utilizada para buscar e recomendar filmes.

## Exemplo de Uso
### Buscar Filme
1. Acesse a página inicial.
2. Insira o título ou parte do título do filme no campo de busca.
3. Clique em "Buscar" para ver os resultados.

### Recomendar Filme
1. Acesse a página inicial.
2. Insira o título do filme no campo de recomendação.
3. Clique em "Recomendar" para ver as recomendações baseadas no filme fornecido.

## Contato
Para mais informações, entre em contato com [ptia202424@gmail.com].
