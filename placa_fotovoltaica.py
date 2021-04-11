import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main(cm, v_conta, t_l, at):
    results_dict = {}
    # definições das variáveis
    t_l1 = 30    # kWh monofásica
    t_l2 = 50    # kWh bifásica
    t_l3 = 100   # kWh trifásica
    tex = 4.96   # horas de pico sol para a cidade de Lavras h/dia
    pt = 0.18    # perda por tempratura de 7 a 18 %
    ie = 0.02    # perda por incompatibilidade elétrica 1 a 2 %
    pcc = 0.01   # perda devido aos cabos da corrente contínua
    pca = 0.01   # perda devido aos cabos da corrente alternada
    pi = 0.05     # perda associada ao inversor
    taxa = 0.62     # [%] taxa aneel
    txcemig = 0.618  # [R$] tarifa cobrada pela cemig por kWh
    # informações das placas
    p1 = 235 / 1000           # Placa Solar Canadian Solar - Modelo CS6P 235P \
    # 325 W por placa
    at1 = 1.5974               # Área da placa
    p2 = 270 / 1000       # Placa Solar Canadian Solar - Modelo CS6K-270M \
    # 273 W por placa
    at2 = 1.6335               # Área da placa
    p3 = 320 / 1000       # Placa Solar Canadian Solar - Modelo CS6X-320P \
    # 320 W por módulo
    at3 = 1.911              # Área da placa


    eg = float
    if t_l == 1:
        eg = (cm - t_l1) / 30  # passar de mês para dias dividir por 30
    if t_l == 2:
        eg = (cm - t_l2) / 30
    if t_l == 3:
        eg = (cm - t_l3) / 30


    n = (abs((pt-1)*(ie-1)*(pcc-1)*(pca-1)*(pi-1)))
    ptp = eg / (tex * n)  # potência máxima total de acordo com consumo
    # print("Energia de geração: ", eg,  "Rendimento:  ",
    #     n, "Potência dos painéis: ", ptp)
    results_dict['energia_geracao'] = eg
    results_dict['rendimento'] = n
    results_dict['potencia_paineis'] = ptp


    # utilizando a placa Placa Solar Canadian Solar - Modelo CS6X-320P \
    # como exemplo - 320 w = 0.32kw por placa área = 1.911
    ntp3 = ptp // p3  # número total de paineis 3
    ptgp3 = ntp3 * p3  # potência total gerada pelo numero total de paineis
    # modelo 3 recalculada
    atn3 = ntp3 * at3  # área do telhado necessária 3
    # print("Número total de paineis modelo 3 = ", ntp3,  
    #     "A área total necessária modelo 3: ", atn3, 
    #     "Potência total gerada pelos paineis modelo 3 (kW): ", ptgp3)
    results_dict['numero_paineis'] = ntp3
    results_dict['area_necessaria'] = atn3
    results_dict['potencia_gerada'] = ptgp3
    if atn3 > at:
        # print("Seu telhado não suporta a instalação, precisamos de no mínimo \
        #     28.665 m²")  # depois vou colocar um modelo menor
        results_dict['area_necessaria'] = "Não suporta. Área mínima: 28.665 m²"
    # potência gerada por dia considerando hora solar pico
    pg3 = ptgp3 * tex
    # print("Potência gerada pelos painéis por dia (kWh/dia): ", pg3)
    results_dict['potencia_gerada_dia'] = pg3
    pg3m = pg3 * 30 # pot gerada mensal
    # print("Potência gerada mensal pelos painéis: (kWh/mês)", pg3m)
    results_dict['potencia_gerada_mes'] = pg3m

    # avaliar a potencia encontrada dentre as potencias com preços
    potencias = np.array([2.03, 2.43, 3.65, 4.46, 4.86, 5.27, 6.48, 6.89, 7.7, 8.97,
                9.72, 11.34, 12.56, 14.58, 21.06])
    precos = {2.03: 15818.78, 2.43: 16760.55, 3.65: 22372.49, 4.46: 26122.8,
            4.86: 27747.49, 5.27: 29580.19, 6.48: 34222.86,
            6.89: 35868.27, 7.7: 39922.59, 8.97: 44133.82,
            9.72: 47140.47, 11.34: 51419.19, 12.56: 57302.99,
            14.58: 67057.57, 21.06: 92070.13}


    preco_final = precos[potencias[np.argmax(potencias>=ptgp3)]]

    # print("O preço a ser pago (investimento de 20 anos) (R$):", preco_final)
    results_dict['preco_investimento'] = preco_final

    # valor a ser economizado pela geração dos paineis por mes
    ep_1 = pg3m * txcemig # economia paineis mensal
    # print("Economia mensal: (R$) sem a taxa da ANEEL", ep_1)

    # valor a ser economizado pela geração dos paineis por mes com a taxa da ANEEL
    ep_2 = pg3m * txcemig * (1 - 0.62)  # economia paineis mensal
    # valor a ser economizado pela geração dos paineis em 20 anos sem taxa da ANEEL
    ep_anos = ep_1 * 25 * 12 # economia paineis 
    ep_anos2 = ep_2  * 25 * 12  # economia paineis 20 anos
    tx_aneel = np.arange(0.00, 0.62, 0.01)
    ep_variavel = pg3m * txcemig * (1 - tx_aneel) * 20 * 12
    tempo_anos = np.array(range(0, 26))
    taxas = np.array([0, 0.15, 0.30, 0.45, 0.60])
    r_df = pd.DataFrame()
    final_df = pd.DataFrame(columns=["Tempo (anos)", "Economia (R$)", "Taxa"])
    for taxa in taxas:
        r_df["Tempo (anos)"] = tempo_anos
        r_df["Economia (R$)"] = pg3m * txcemig * (1 - taxa) * 12 * tempo_anos
        r_df["Taxa"] = taxa
        final_df = pd.concat([final_df, r_df])

    return results_dict, final_df