
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - procesamiento de datos
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #
import pandas as pd

# Funcion para leer archivo de datos
def f_leer_archivo(param_archivo):
    """
    Parameters
    ---------
    :param param_archivo: str : nombre de archivo leer

    Returns
    ---------
    :return: df_data: DataFrame

    Debuggin
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'

    """

    # Leer archivo de datos y guardalo en un DataFrame
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Hoja1')

    # Convertir en minusculas el nombre de las columnas
    df_data.columns = [df_data.columns[i].lower() for i in range(len(df_data.columns))]

    # Elegir solo renglones en los que la columna type == buy | type == sell
    #df_data.columns = [df_data[i] for i in range(len(df_data)) if df_data[i] == 'buy' or df_data[i] == 'sell' ]

    # Asegurar que ciertas columnas son del tipo numerico
    #num_col = ['order', 'size', 'openprice', 's/l', 't/p', 'closeprice', 'taxes', 'swap', 'profit']
    #df_data[num_col] = df_data[num_col].apply(pd.to_numeric)

    return df_data


''' Función para obtener el numero multplicador
para expresar la diferencia de precios en pips
'''
def f_pip_size(param_ins):
    """
    Parameters
    ---------
    :param param_ins: str : nombre de instrumento para asociarse el multiplicador de pips

    Returns
    ---------
    :return: pip: int

    Debuggin
    ---------

    """
    if param_ins == "usdjpy-2":
        num_pip = 1000
    else:
        num_pip = 10000
    return num_pip


''' Función para agregar mas columnas de transformaciones de tiempo
'''
def f_columnas_tiempos(param_data):
    """
    Parameters
    ---------
    :param param_data: DataFrame : frame del archivo de operaciones

    Returns
    ---------
    :return: df_tiempos: DataFrame

    Debuggin
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'

    """

    return 0


def f_columna_pips(param_data):
    """
    Parameters
    ---------
    :param param_archivo: str : nombre de archivo leer

    Returns
    ---------
    :return: df_data: DataFrame

    Debuggin
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'

    """

    return 0


def f_estadistica_ba(param_data):
    """
    Parameters
    ---------
    :param param_archivo: str : nombre de archivo leer

    Returns
    ---------
    :return: df_data: DataFrame

    Debuggin
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'

    """

    return 0


def f_estadistica_av(param_data):
    """
    Parameters
    ---------
    :param param_archivo: str : nombre de archivo leer

    Returns
    ---------
    :return: df_data: DataFrame

    Debuggin
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'

    """

    return 0






