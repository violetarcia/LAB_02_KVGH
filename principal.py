
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - layout general del proyecto
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import pandas as pd

# -- PART II --

# Leer archivo (el de Francisco es el 2)
datos = fn.f_leer_archivo('archivo_tradeview_2.xlsx')

# Agregar la columna de los tiempos
fn.f_columnas_tiempos(datos)

# Agregar columna de pips
fn.f_columna_pips(datos)

# DataFrames de Estadisticas basicas y ranking
df_1_tabla, df_2_ranking = fn.f_estadistica_ba(datos)


# -- PART III --

# Agregar capital acumulado
fn.f_columna_capital_acm(datos)

# DataFrame de profits
df_profit = fn.f_profit_diario(datos)

# Agregar rendimientos 
fn.log_dailiy_rends(df_profit)

# Estadisticas de metricas de desempeño
df_estadistic = fn.f_estadisticas_mad(df_profit)