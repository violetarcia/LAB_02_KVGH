
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - graficas para el proyecto
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #

import numpy as np
import matplotlib.pyplot as plt
from principal import df_profit, data, df_estadistic
from funciones import f_drawdown
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#%% Parte II
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Datos
df_1_ranking = df_estadistic['ranking']

# Grafica de barras del ranking
fig_rank = plt.figure('Gráfica de barras') # Figure
ax = fig_rank.add_subplot(111) # Axes

nombres = list(df_1_ranking.index)
datos = sum(df_1_ranking.values.tolist(), [])
xx = range(len(datos))

ax.bar(xx, datos, width=0.8, align='center')
ax.set_xticks(xx)
ax.set_xticklabels(nombres, rotation=45)
plt.title('Ranking de las ganadoras por instrumento')
plt.ylabel('porcentaje')
plt.show()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Segundo Ranking
# Datos
df_2_ranking = df_estadistic['ranking 2']

# Grafica de barras del ranking
fig_rank2 = plt.figure('Gráfica de barras') # Figure
ax = fig_rank2.add_subplot(111) # Axes

nombres = list(df_2_ranking.index)
datos = sum(df_2_ranking.values.tolist(), [])
xx = range(len(datos))

ax.bar(xx, datos, width=0.8, align='center')
ax.set_xticks(xx)
ax.set_xticklabels(nombres, rotation=45)
plt.title('Ranking del profit por instrumento')
plt.ylabel('dinero')
plt.show()

#%% Parte III

up, down = f_drawdown(df_profit, 'profit_acm', string=False)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Grafica del capital acumulado a traves del tiempo
fig_dd = plt.figure()
plt.plot(df_profit['timestamp'], df_profit['profit_acm'], color = 'k')
plt.plot(df_profit['timestamp'][down[1:]], df_profit['profit_acm'][down[1:]], '--', color='Red')
plt.plot(df_profit['timestamp'][up[1:]], df_profit['profit_acm'][up[1:]], '--', color='Green')

# Titulo
plt.title('Profit acumulado por dia')
# Eje X
plt.xlabel('tiempo')
plt.xticks(rotation=90)
# Eje Y
plt.ylabel('Capital')
plt.show()


#%%
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Grafica de capital acumulado por operacion
fig_cap = plt.figure()
plt.plot(np.arange(len(data)), data['capital_acm'])
# Titulo
plt.title('Profit acumulado por operacion')
# Eje X
plt.xlabel('operacion')
# Eje Y
plt.ylabel('Capital')
plt.show()










