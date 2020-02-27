
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - procesamiento de datos
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #
import pandas as pd

def f_leer_archivo(param_archivo):
    """
    Parameters
    ---------
    :param param_archivo:

    Returns
    ---------
    :return:

    Debuggin
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'

    """

    # Leer archivo de datos y guardalo en un DataFrame
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Hoja1')

    # Convertir en minusculas el nombre de las columnas
    df_data.columns = [df_data.columns[i].lower() for i in range(len(df_data.columns))]

    # Asegurar que ciertas columnas son del tipo numerico
    num_col = ['order', 'size', 'openprice', 's/l', 't/p', 'closeprice', 'taxes', 'swap']
    df_data[num_col] = df_data[num_col].apply(pd.to_numeric)

    return df_data
