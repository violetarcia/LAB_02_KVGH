
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - layout general del proyecto
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import pandas as pd

# Leer archivo (el de Francisco es el 2)
datos = fn.f_leer_archivo('archivo_tradeview_2.xlsx')

# Agregar la columna de los tiempos
fn.f_columnas_tiempos(datos)

# Agregar columna de pips
fn.f_columna_pips(datos)

# Ver Estadisticas basicas y ranking
df_1_tabla, df_2_ranking = fn.f_estadistica_ba(datos)

