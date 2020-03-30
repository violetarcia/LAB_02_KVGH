
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - graficas para el proyecto
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #


import matplotlib.pyplot as plt
import numpy as np
from principal import df_profit


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Grafica del capital acumulado a traves del tiempo

plt.plot(df_profit['timestamp'], df_profit['profit_acm'])
# Titulo
plt.title('Profit acumulado')
# Eje X
plt.xlabel('tiempo')
plt.xticks(rotation=90)
# Eje Y
plt.ylabel('Capital')
plt.show()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
 