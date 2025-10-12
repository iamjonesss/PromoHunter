# 🤖 PromoHunter

_Um assistente inteligente para encontrar os melhores produtos com base em avaliações e custo-benefício._

![Status do Projeto](https://img.shields.io/badge/status-em%20desenvolvimento-yellowgreen)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📖 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [✨ Funcionalidades](#-funcionalidades)
- [🖼️ Demonstração](#-demonstração)
- [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [🚀 Começando](#-começando)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
- [🔥 Como Usar](#-como-usar)
- [🤝 Como Contribuir](#-como-contribuir)
- [📝 Licença](#-licença)
- [📧 Contato](#-contato)

## 📌 Sobre o Projeto

O **Product Recommender Bot** é uma solução de chatbot desenvolvida em Python que utiliza o poder dos modelos de linguagem locais (LLMs) através do **Ollama** para ajudar usuários a tomar decisões de compra mais inteligentes.

A principal proposta é simplificar a busca pelo produto ideal. Em vez de gastar horas pesquisando em diferentes sites, o usuário pode simplesmente conversar com o bot, que irá analisar e comparar produtos com base em múltiplos critérios, como preço, avaliações de outros compradores e especificações técnicas, para recomendar a opção com o melhor custo-benefício.

## ✨ Funcionalidades

-   **Interação em Linguagem Natural:** Converse com o bot de forma intuitiva para solicitar recomendações.
-   **Análise de Produtos:** O bot é capaz de coletar e processar informações de produtos de diversas fontes (a ser implementado/especificado).
-   **Critérios Múltiplos de Avaliação:** Análise baseada em uma combinação de:
    -   Preço atual.
    -   Média de avaliações de usuários.
    -   Sentimento geral dos comentários.
    -   Especificações técnicas relevantes.
-   **Recomendações Personalizadas:** Respostas diretas e resumidas, indicando o melhor produto de acordo com a solicitação.
-   **Privacidade:** Por utilizar o Ollama, todo o processamento da linguagem pode ser feito localmente, garantindo a privacidade dos dados do usuário.

## 🖼️ Demonstração

*(Esta é uma ótima seção para adicionar GIFs ou screenshots do seu bot em ação.)*

## 🛠️ Tecnologias Utilizadas

A seguir, as principais tecnologias e bibliotecas que movem este projeto:

-   [Python](https://www.python.org/)
-   [Ollama](https://ollama.com/)
-   [Biblioteca `requests`](https://requests.readthedocs.io/en/latest/) (ou outra para web scraping/API)
-   [Biblioteca `ollama-python`](https://github.com/ollama/ollama-python)
-   [Jupyter Notebook](https://jupyter.org/) (para desenvolvimento e testes)

## 🚀 Começando

Para executar o projeto localmente, siga os passos abaixo.

### Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

1.  **Python 3.9 ou superior:**
    ```bash
    python --version
    ```
2.  **Ollama:**
    Siga as instruções de instalação no [site oficial do Ollama](https://ollama.com/).
3.  **Um modelo de linguagem via Ollama:**
    Recomendamos um modelo instrucional como o Llama 3 ou o Mistral.
    ```bash
    ollama pull llama3
    ```

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)
    cd nome-do-repositorio
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔥 Como Usar

Para iniciar o bot, execute o script principal a partir do seu terminal:

```bash
python main.py
```

Após a inicialização, você poderá interagir com o bot diretamente no console. Siga as instruções que aparecerão na tela.

## 🤝 Como Contribuir

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

Se você tiver uma sugestão para melhorar este projeto, por favor, faça um fork do repositório e crie um pull request. Você também pode simplesmente abrir uma issue com a tag "enhancement".

1.  Faça um **Fork** do projeto.
2.  Crie uma **Branch** para sua feature (`git checkout -b feature/AmazingFeature`).
3.  Faça o **Commit** de suas mudanças (`git commit -m 'Add some AmazingFeature'`).
4.  Faça o **Push** da Branch (`git push origin feature/AmazingFeature`).
5.  Abra um **Pull Request**.

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE.txt` para mais informações.

## 📧 Contato

Seu Nome - [Seu Perfil no LinkedIn](https://www.linkedin.com/in/seu-linkedin/) - seu.email@example.com

Link do Projeto: [https://github.com/seu-usuario/nome-do-repositorio](https://github.com/seu-usuario/nome-do-repositorio)