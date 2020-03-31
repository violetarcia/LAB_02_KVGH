
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: datos.py - datos generales para uso en el proyecto
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #

import numpy as np
import pandas_datareader.data as web
#from funciones import log_dailiy_rends
#from principal import data


# DATOS

# Capital 
cap = 5000

# Tasa libre de riesgo anual
rf = 0.08

# Minimum Acceptable Return anual
mar = 0.3

# Benchmark
sp500 = web.YahooDailyReader('^GSPC',  '2019-08-27', '2019-09-27', interval='d').read()['Close']
# Rendimientos del  bechchmark
sp500_rends = np.log(sp500/sp500.shift(1)).iloc[1:]

benchmark = sp500_rends.mean()
#benchmark = 0.1

# OANDA
OANDA_ACCESS_TOKEN = '800f1b3f91d7cb0a713c532e17823f6d-f9acd6a21490f97aef649dfd8e723435'


#%%
'''
inicio : str(data['opentime'].min())[:10]
fin : str(data['closetime'].max())[:10]
'''

