import numpy as np
import matplotlib.pyplot as plt

cm = float(input("Digite o consumo médio mensal presente na conta de luz(kWh): "))
t_l = int(input("Qual o tipo de ligação? Digite: \
                1 para Monofásico\
                2 para Bifásico\
                3 para Trifásico                         :"))
at = float(input("Digite a área disponível do telhado (área limite 30m²) "))
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
ptp = eg / (tex * n)  # potência máxima total de acoro com consumo
print("Energia de geração: ", eg,  "Rendimento:  ",
      n, "Potência dos painéis: ", ptp)

# utilizando a placa Placa Solar Canadian Solar - Modelo CS6X-320P \
# como exemplo - 320 w = 0.32kw por placa área = 1.911
ntp3 = ptp // p3  # número total de paineis 3
print()
ptgp3 = ntp3 * p3  # potência total gerada pelo numero total de paineis
# modelo 3 recalculada
atn3 = ntp3 * at3  # área do telhado necessária 3
print("Número total de paineis modelo 3 = ", ntp3, "A área total\
        necessária modelo 3: ", atn3, "Potência total gerada pelos paineis modelo 3 (kW): ", ptgp3)
if atn3 > at:
    print("Seu telhado não suporta a instalação, precisamos de no mínimo \
          28.665 m²")  # depois vou colocar um modelo menor
# potência gerada por hora
pg3 = ptgp3 * tex
print("Potência gerada por hora pelos painéis: ", pg3)
pg3m = pg3 * 30
print("Potência gerada por hora mensal pelos painéis: (kWh)", pg3m)

# valor a ser economizado pela geração dos paineis por mes
ep = pg3m * txcemig  # economia paineis mensal
print("Economia mensal: (R$) sem a taxa da ANEEL", ep)

# valor a ser economizado pela geração dos paineis por mes com a taxa da ANEEL
ep = pg3m * txcemig * (1 - 0.62)  # economia paineis mensal
print("Economia mensal: (R$) com a taxa da ANEEL", ep)

# variando taxa ANEEL

tx_aneel = np.arange(0.00, 0.62, 0.01)
ep_variavel = pg3m * txcemig * (1 - tx_aneel)
print(tx_aneel)
plt.plot(tx_aneel, ep_variavel)
plt.show()
