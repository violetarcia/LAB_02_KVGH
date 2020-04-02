
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - graficas para el proyecto
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #


import matplotlib.pyplot as plt
from principal import df_profit, data
import numpy as np

#%%
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Grafica del capital acumulado a traves del tiempo

plt.plot(df_profit['timestamp'], df_profit['profit_acm'])
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
plt.plot(np.arange(len(data)), data['capital_acm'])
# Titulo
plt.title('Profit acumulado por operacion')
# Eje X
plt.xlabel('operacion')
# Eje Y
plt.ylabel('Capital')
plt.show()










