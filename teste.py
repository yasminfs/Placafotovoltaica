cm = float(input("Digite o consumo médio presente na conta de luz: "))
t_l = int(input("Qual o tipo de ligação? Digite: \
                1 para Monofásico\
                2 para Bifásico\
                3 para Trifásico                         :"))
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
taxa = 0.6
p5m = 1.65             # Placa Fotovoltaica 5 Módulos 1,65kWp WEG \
# Área Necessária no Telhado	11 m²
p8m = 2.64             # Placa Fotovoltaica 8 Módulos 2,64kWp WEG\
# Área Necessária no Telhado	18 m²
p14m = 4.62            # Placa Fotovoltaica 14 Módulos 4,62kWp WEG\
# Área Necessária no Telhado	31 m²

preço1 = 9349.9          # Preço (R$)
preço2 = 11149.9         # Preço (R$)
preço3 = 21899.9        # Preço (R$)


eg = float
if t_l == 1:
    eg = (cm - t_l1) / 30  # passar de mês para dias dividir por 30
if t_l == 2:
    eg = (cm - t_l2) / 30
if t_l == 3:
    eg = (cm - t_l3) / 30


n = (abs((pt-1)*(ie-1)*(pcc-1)*(pca-1)*(pi-1)))
ptp = eg / (tex * n)  # potência total dos paineis
print("Energia de geração: ", eg,  "Rendimento:  ",
      n, "Potência total dos painéis: ", ptp)

nt = ptp / p5m  # usando como base a placa de 5 módulos  (N total de paineis)
