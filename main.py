from datetime import date, timedelta
import time
import os
from serpapi import GoogleSearch

# --- Configurações do Usuário ---
# Rota: São Paulo (GRU/CGH/VCP) para Boston (BOS)
# Códigos IATA: SAO (São Paulo - todos os aeroportos) e BOS (Boston)
ORIGEM = "SAO"
DESTINO = "BOS"
CLASSE = "business"
PRECO_ALVO_BRL = 8000.00
DURACAO_DIAS = 7
DATA_INICIO_BUSCA = date(2025, 4, 17)
PERIODO_BUSCA_MESES = 6

def buscar_voos(data_ida: date, data_volta: date) -> dict | None:
    """
    Realiza a busca de voos no Google Flights usando a SerpApi.
    """
    print(f"Buscando voos para {ORIGEM} -> {DESTINO} de {data_ida} a {data_volta}...")
    
    # A chave da API deve ser definida como variável de ambiente
    if not os.getenv("SERPAPI_API_KEY"):
        print("ERRO: A variável de ambiente SERPAPI_API_KEY não está definida.")
        return None

    params = {
        "engine": "google_flights",
        "hl": "pt",
        "gl": "br",
        "currency": "BRL",
        "departure_id": ORIGEM,
        "arrival_id": DESTINO,
        "outbound_date": data_ida.isoformat(),
        "return_date": data_volta.isoformat(),
        "travel_class": CLASSE,
        "api_key": os.getenv("SERPAPI_API_KEY")
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            print(f"Erro da SerpApi: {results['error']}")
            return None
            
        return results
    except Exception as e:
        print(f"Erro ao buscar voos na SerpApi: {e}")
        return None

def analisar_resultados(results: dict, data_ida: date, data_volta: date) -> bool:
    """
    Analisa os resultados da SerpApi e verifica se o preço alvo foi atingido.
    """
    if not results.get("best_flights"):
        print("Nenhum voo encontrado ou erro na busca.")
        return False

    # A SerpApi retorna o preço já em BRL e como número
    melhores_voos = results["best_flights"]
    
    # Filtra voos de classe executiva (embora já tenhamos filtrado na busca, é bom garantir)
    # E encontra o menor preço
    menor_preco = float('inf')
    melhor_voo = None
    
    for voo in melhores_voos:
        # O preço total é a soma dos preços dos segmentos
        preco_total = voo["price"]
        
        if preco_total < menor_preco:
            menor_preco = preco_total
            melhor_voo = voo

    if menor_preco == float('inf'):
        print("Nenhum preço válido encontrado para os voos.")
        return False

    # Formatação para o padrão brasileiro (R$ 8.000,00)
    preco_formatado = f"{menor_preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    alvo_formatado = f"{PRECO_ALVO_BRL:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    print(f"Menor preço encontrado: R$ {preco_formatado}")
    
    if menor_preco <= PRECO_ALVO_BRL:
        print("!!! ALERTA DE PREÇO BAIXO !!!")
        print(f"Preço alvo de R$ {alvo_formatado} atingido!")
        
        # Aqui você implementaria a lógica de envio de alerta (e-mail, etc.)
        # Por enquanto, vamos apenas imprimir os detalhes
        print("\nDetalhes do Melhor Voo:")
        print(f"Preço: R$ {preco_formatado}")
        
        # Extrai detalhes do voo
        # O primeiro segmento contém a companhia aérea principal
        primeiro_segmento = melhor_voo["segments"][0]
        companhia = primeiro_segmento["airline"]
        duracao = melhor_voo["duration"]
        escalas = len(melhor_voo["segments"]) - 1
        
        print(f"Companhia: {companhia}")
        print(f"Duração Total: {duracao} minutos")
        print(f"Escalas: {escalas}")
        print(f"Link de Busca: {results['search_metadata']['google_flights_url']}")
        
        # Retorna True para indicar que o alerta deve ser enviado
        return True
    else:
        print(f"Preço encontrado (R$ {preco_formatado}) acima do alvo (R$ {alvo_formatado}).")
        return False

def main():
    print("--- Iniciando Automação de Busca de Passagens Executivas ---")
    
    # Define o período de busca
    data_fim_busca = DATA_INICIO_BUSCA + timedelta(days=30 * PERIODO_BUSCA_MESES)
    
    data_atual = DATA_INICIO_BUSCA
    
    print(f"Iniciando busca de {PERIODO_BUSCA_MESES} meses a partir de {DATA_INICIO_BUSCA.isoformat()}...")
    
    # Formatação para o padrão brasileiro (R$ 8.000,00)
    alvo_formatado = f"{PRECO_ALVO_BRL:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    print(f"Preço alvo para alerta: R$ {alvo_formatado}")
    
    alertas_enviados = 0
    
    while data_atual < data_fim_busca:
        data_volta = data_atual + timedelta(days=DURACAO_DIAS)
        
        print(f"\n--- Buscando: {data_atual.isoformat()} a {data_volta.isoformat()} ---")
        
        resultado = buscar_voos(data_atual, data_volta)
        
        if resultado:
            if analisar_resultados(resultado, data_atual, data_volta):
                alertas_enviados += 1
        
        # Avança para a próxima semana (7 dias)
        data_atual += timedelta(days=7)
        
        # Adiciona um pequeno delay para evitar sobrecarregar a API
        time.sleep(2)
        
    print(f"\nBusca finalizada. Total de alertas de preço baixo: {alertas_enviados}")
    
    print("--- Fim da Automação ---")

if __name__ == "__main__":
    main()
