import numpy as np
import pandas as pd


def main(cm, t_l, at):
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
    p3 = 320 / 1000       # Placa Solar Canadian Solar - Modelo CS6X-320P \
    # 320 W por módulo
    at3 = 1.911              # Área da placa

    eg = float()
    if t_l == 1:
        eg = (cm - t_l1) / 30  # passar de mês para dias dividir por 30
    if t_l == 2:
        eg = (cm - t_l2) / 30
    if t_l == 3:
        eg = (cm - t_l3) / 30

    n = (abs((pt-1)*(ie-1)*(pcc-1)*(pca-1)*(pi-1)))
    ptp = eg / (tex * n)  # potência máxima total de acordo com consumo
    results_dict['energia_geracao'] = eg
    results_dict['rendimento'] = n
    results_dict['potencia_paineis'] = ptp
    ntp3 = ptp // p3  # número total de paineis 3
    ptgp3 = ntp3 * p3  # potência total gerada pelo numero total de paineis
    atn3 = ntp3 * at3  # área do telhado necessária 3
    results_dict['numero_paineis'] = ntp3
    results_dict['area_necessaria'] = atn3
    results_dict['potencia_gerada'] = ptgp3
    pg3 = ptgp3 * tex
    results_dict['potencia_gerada_dia'] = pg3
    pg3m = pg3 * 30  # pot gerada mensal
    results_dict['potencia_gerada_mes'] = pg3m
    # avaliar a potencia encontrada dentre as potencias com preços
    potencias = np.array([2.03, 2.43, 3.65, 4.46, 4.86, 5.27, 6.48, 6.89, 7.7, 8.97,
                          9.72, 11.34, 12.56, 14.58, 21.06])
    precos = {2.03: 15818.78, 2.43: 16760.55, 3.65: 22372.49, 4.46: 26122.8,
              4.86: 27747.49, 5.27: 29580.19, 6.48: 34222.86,
              6.89: 35868.27, 7.7: 39922.59, 8.97: 44133.82,
              9.72: 47140.47, 11.34: 51419.19, 12.56: 57302.99,
              14.58: 67057.57, 21.06: 92070.13}

    preco_final = precos[potencias[np.argmax(potencias >= ptgp3)]]
    results_dict['preco_investimento'] = preco_final
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
