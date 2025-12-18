# Automação de Busca de Passagens Aéreas - Classe Executiva

Este projeto implementa uma automação em Python para buscar passagens aéreas de **Classe Executiva** na rota **São Paulo (SAO) para Boston (BOS)**, com foco em encontrar o menor preço.

## ✈️ Escopo da Busca

| Parâmetro | Valor |
| :--- | :--- |
| **Rota** | São Paulo (SAO) → Boston (BOS) |
| **Classe** | Executiva (`business`) |
| **Preço Alvo** | R$ 8.000,00 (ida e volta) |
| **Período** | 6 meses a partir de 17/04/2025 |
| **Duração** | 7 dias |
| **Fonte de Dados** | SerpApi (Google Flights API) |

## 🛠️ Pré-requisitos

Para que a automação funcione, você precisará de uma chave de API da SerpApi.

1.  **Obtenha sua Chave SerpApi:**
    *   Crie uma conta no site da [SerpApi](https://serpapi.com/).
    *   Obtenha sua chave de API no painel de controle.

2.  **Instale as Dependências:**
    ```bash
    pip install google-search-results
    ```

3.  **Configure a Chave de API:**
    A chave deve ser configurada como uma variável de ambiente chamada `SERPAPI_API_KEY`.

    *   **Linux/macOS:**
        ```bash
        export SERPAPI_API_KEY="SUA_CHAVE_AQUI"
        ```
    *   **Windows (Prompt de Comando):**
        ```bash
        set SERPAPI_API_KEY="SUA_CHAVE_AQUI"
        ```
    *   **Windows (PowerShell):**
        ```bash
        $env:SERPAPI_API_KEY="SUA_CHAVE_AQUI"
        ```

## 🚀 Como Executar

1.  Salve o código Python (`main.py`) em um arquivo.
2.  Certifique-se de que a variável de ambiente `SERPAPI_API_KEY` esteja configurada.
3.  Execute o script:
    ```bash
    python3 main.py
    ```

## 🔔 Lógica de Alerta

O script irá iterar sobre as datas no período definido. Se o menor preço encontrado para a classe executiva for **menor ou igual a R$ 8.000,00**, um alerta detalhado será impresso no console, incluindo o link direto para a busca no Google Flights.

**Nota:** O código está pronto para ser expandido para enviar alertas por e-mail ou outras plataformas, bastando adicionar a lógica de envio na função `analisar_resultados`.
