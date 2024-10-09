# Movibo API Documentation

## Visão Geral
A **Movibo API** é uma API de recomendação de filmes desenvolvida em Python usando o framework **FastAPI**. A aplicação permite que os usuários enviem consultas com o nome, gênero ou descrição de um filme e obtenham recomendações baseadas em similaridade, utilizando técnicas de processamento de linguagem natural e clustering.

### URLs Publicadas
- **Versão JSON**: [https://fastapi-movibo-cnow.onrender.com/](https://fastapi-movibo-cnow.onrender.com/)
- **Versão HTML**: [https://fastapi-movibo.onrender.com/](https://fastapi-movibo.onrender.com/)

### Objetivo da API
O objetivo principal da API é fornecer recomendações de filmes similares com base em critérios fornecidos pelo usuário, como nome, gênero e/ou descrição. As respostas são geradas com base em um banco de dados pré-processado de filmes e em técnicas de agrupamento de dados.

---

## Endpoints e Funcionalidades

### 1. `/recomendados/` - Endpoint de Recomendação de Filmes

- **Método HTTP**: `GET`
- **Descrição**: Retorna uma lista de filmes recomendados com base nos parâmetros fornecidos pelo usuário.
- **Parâmetros de Consulta (Query Parameters)**:
  - `title` (opcional): Nome do filme que o usuário deseja usar como referência para recomendações.
  - `genres` (opcional): Gênero(s) do filme, separados por vírgula. Por exemplo, `Action, Sci-Fi`.
  - `description` (opcional): Uma breve descrição do filme para ajudar a API a identificar temas e tópicos relevantes.
  
- **Comportamento**:
  - Se **todos** os parâmetros forem fornecidos (`title`, `genres` e `description`), a API considera a combinação para calcular a similaridade e gerar as recomendações.
  - Se **nenhum** parâmetro for fornecido, a API retornará uma lista de filmes genéricos como sugestão.
  - Caso **apenas um** parâmetro seja fornecido (por exemplo, apenas o título), a recomendação será baseada apenas neste parâmetro.

- **Exemplo de Requisição**:
  ```
  GET /recomendados/?title=Inception&genres=Action, Sci-Fi&description=Dreams within dreams
  ```

- **Exemplo de Resposta**:
  ```json
  {
    "status": "success",
    "recomended_movies": [
      {
        "title": "The Matrix",
        "genres": "Action, Sci-Fi",
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality."
      },
      {
        "title": "Paprika",
        "genres": "Animation, Sci-Fi",
        "description": "When a machine that allows therapists to enter their patients' dreams is stolen, all hell breaks loose."
      }
    ]
  }
  ```

- **Mensagens de Erro**:
  - Se o título fornecido não for encontrado no banco de dados:
    ```json
    {
      "status": "error",
      "message": "O filme especificado não foi encontrado no banco de dados."
    }
    ```
  - Se houver problemas nos parâmetros fornecidos (por exemplo, um formato incorreto de gênero):
    ```json
    {
      "status": "error",
      "message": "Gênero fornecido está em um formato inválido. Use vírgulas para separar múltiplos gêneros."
    }
    ```

### 2. `/` - Página de Busca com Interface HTML

- **Método HTTP**: `GET`
- **Descrição**: Exibe uma interface HTML onde os usuários podem realizar buscas por filmes e obter recomendações visualmente.
- **Comportamento**:
  - O usuário insere as informações nos campos correspondentes (Título, Gênero, Descrição).
  - O formulário é enviado, e a resposta é exibida diretamente na página com uma lista de recomendações.

- **Parâmetros de Consulta (HTML Form)**:
  - `title` (opcional): Nome do filme para recomendação.
  - `genres` (opcional): Gênero(s) do filme.
  - `description` (opcional): Descrição do filme para ajudar na identificação temática.

- **Exemplo de Uso**:
  - Acesse [https://fastapi-movibo.onrender.com/](https://fastapi-movibo.onrender.com/) e preencha os campos de busca conforme desejado.

---

## Estrutura do Código e Organização

### Arquivo: `main.py`

Este é o ponto de entrada da API. Ele contém a definição dos endpoints e a lógica principal para processar as solicitações de recomendação.

- **Função `recomendados()`**:
  - Caminho: `/recomendados/`
  - Método: `GET`
  - Descrição: Lida com as requisições para gerar recomendações de filmes.
  - Lógica: Utiliza os parâmetros fornecidos (`title`, `genres`, `description`) para calcular a similaridade de filmes usando clusters gerados previamente.
  
- **Função `index()`**:
  - Caminho: `/`
  - Método: `GET`
  - Descrição: Serve a página HTML para a versão visual da API.
  - Lógica: Renderiza a página HTML com os campos para inserção dos parâmetros.

### Arquivo: `models/recommendation.py`

Este arquivo contém as funções de suporte para carregar o dataset, calcular a similaridade e retornar recomendações com base no clustering.

- **Função `load_dataset()`**:
  - Descrição: Carrega o dataset de filmes (`imdb_top_1000.csv`), pré-processa e cria os clusters.
  
- **Função `get_recommendations()`**:
  - Descrição: A partir de um título, gênero e descrição fornecidos, calcula a similaridade dos filmes e retorna uma lista de sugestões.

---

## Guia de Uso e Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/VitorioWB/FastAPI_Movibo.git
   ```

2. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Rode a API localmente**:

   ```bash
   uvicorn main:app --reload
   ```

4. **Acesse a API no navegador**:

   - Para JSON: [http://localhost:8000/recomendados/](http://localhost:8000/recomendados/)
   - Para HTML: [http://localhost:8000/](http://localhost:8000/)
