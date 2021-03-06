
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - layout general del proyecto
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
from time import time

t0 = time()

# -- PART II --

# Leer archivo (el de Francisco es el 2)
data = fn.f_leer_archivo('archivo_tradeview_1.xlsx')

# Agregar la columna de los tiempos
fn.f_columna_tiempos(data)

# Agregar columna de pips
fn.f_columna_pips(data)

# DataFrames de Estadisticas basicas y ranking
df_estadistic = fn.f_estadistica_ba(data)


# -- PART III --

# Agregar capital acumulado
fn.f_columna_capital_acm(data)

# DataFrame de profits
df_profit = fn.f_profit_diario(data)


# Agregar rendimientos 
fn.log_dailiy_rends(df_profit, 'profit_acm')

# Estadisticas de metricas de desempeño
df_profit_estad = fn.f_estadisticas_mad(data)


# -- PART IV --

# Operaciones ganadora vs perdedora (ocurrencia)
sesgos = fn.f_sesgos_cognitivo(data)

# Porcentaje de profit ganadoras / profit perdedoras
porcentaje = abs(sum(data[data['profit/cap'] > 0]['profit/cap']) /
             sum(data[data['profit/cap'] < 0]['profit/cap']))

# Tiempo
print(time() - t0)


