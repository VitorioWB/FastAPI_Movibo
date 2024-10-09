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
  GET /recomendados/?title=Inception&genres=Action, Sci-Fi&description=dream
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
      }
    ]
  }
  ```

### 2. `/` - Página de Busca com Interface HTML

- **Método HTTP**: `GET`
- **Descrição**: Exibe uma interface HTML onde os usuários podem realizar buscas por filmes e obter recomendações visualmente.
- **Comportamento**:
  - O usuário insere as informações nos campos correspondentes (Título, Gênero, Descrição).
  - O formulário é enviado, e a resposta é exibida diretamente na página com uma lista de recomendações.

---

## Estrutura do Código e Organização

### Arquivo: `main.py`
- Contém a definição dos endpoints e a lógica principal para processar as solicitações de recomendação.
  
### Arquivo: `models/recommendation.py`
- Lida com a lógica de similaridade de filmes e gerenciamento de dados.

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

---

## Como Contribuir
Contribuições são bem-vindas! Se você deseja colaborar com melhorias, correções de bugs ou novas funcionalidades, siga os passos abaixo:

1. **Crie uma branch para sua feature ou correção**:

   ```bash
   git checkout -b feature/nome-da-feature
   ```

2. **Faça suas alterações e comite**:

   ```bash
   git add .
   git commit -m "Descrição clara das mudanças"
   ```

3. **Envie a branch para o repositório remoto**:

   ```bash
   git push origin feature/nome-da-feature
   ```

4. **Abra um Pull Request (PR)** no GitHub e descreva suas mudanças.
  
### Regras para Contribuição
- Mantenha o código bem documentado.
- Teste suas alterações antes de enviar.
- Acompanhe as discussões e siga o estilo de código existente.

---

## Contato
Se precisar de mais informações ou quiser discutir melhorias para o projeto, entre em contato com a equipe:

- **[Vitório Bearari](https://www.linkedin.com/in/vitorio-bearari/)**
- **[Eric de Lucas](https://www.linkedin.com/in/eric-de-lucas-silva-902589265/)**
- **[Fabrício Okamoto](https://www.linkedin.com/in/fabr%C3%ADcio-okamoto-087751302/)**
- **[Maria Clara Lucas Souza](https://www.linkedin.com/in/maria-clara-lucas-souza-975185192/)**
