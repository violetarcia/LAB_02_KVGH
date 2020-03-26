
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - procesamiento de datos
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #
import pandas as pd
import numpy as np


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Leer archivo - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

''' Funcion para leer archivo de datos
        f_leer_archivo :
        Leer tu archivo histórico de operaciones, 
        es el que se descarga de MT4 en formato .xlsx.
'''
def f_leer_archivo(param_archivo):
    """
    Parameters
    ---------
    :param: 
        param_archivo: str : nombre de archivo leer

    Returns
    ---------
    :return: 
        df_data: DataFrame : Datos del archivo

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
    num_col = ['order', 'size', 'openprice', 's/l', 't/p', 'closeprice', 'taxes', 'swap', 'profit']
    df_data[num_col] = df_data[num_col].apply(pd.to_numeric)

    return df_data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: pip de instrumento - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
''' Función para obtener el numero multplicador
    para expresar la diferencia de precios en pips
        f_pip_size:
        Función para obtener el número multiplicador 
        para expresar la diferencia de precios en pips.
'''
def f_pip_size(param_ins):
    """

    Parameters
    ---------
    :param: 
        param_ins: str : nombre de instrumento para asociarse el multiplicador de pips

    Returns
    ---------
    :return: 
        pip_inst: int

    Debuggin
        param_ins = 'usdjpy'
    
    ---------

    """
    # transformar a minusculas
    inst = param_ins.lower()

    # lista de pips por instrumento
    pips_inst = {
                'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                 'chfjpy': 100,'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 
                 'usdmxn': 10000,'audusd': 10000, 'nzdusd': 10000, 'usdchf': 10000,
                 'eurgbp': 10000, 'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000,
                 'gbpnzd': 10000, 'gbpchf': 10000, 'gbpaud': 10000, 'audnzd': 10000, 
                 'nzdcad': 10000, 'audcad': 10000, 'xauusd': 10, 'xagusd': 10, 'btcusd': 1
                 }

    return pips_inst[inst]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Tiempo de operacion - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
''' Función para agregar mas columnas de transformaciones de tiempo
        f_columnas_tiempos:
        Agregar mas columnas de transformaciones de tiempo
'''
def f_columnas_tiempos(param_data):
    """

    Parameters
    ---------
    :param: 
        param_data: DataFrame : Data frame del archivo de operaciones

    Returns
    ---------
    :return: 
        param_data: DataFrame

    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')

    """
    # Convertir el tipo de las columnas de closetime y opentime a 'Date'
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # Tiempo entre el transcurso de la operacion
    param_data['time'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta
                            for i in range(len(param_data['closetime']))]

    return param_data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Visitas en el tiempo - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

'''f_columnas_pips: Agregar nuevas columnas: 
    - - - - - - - - - - - - - - - - - - - -
    'pips', que es la columna de pérdida o ganancia de la operación expresada en pips
    - - - - - - - - - - - - - - - - - - - - 
    'pips_acm' que son los pips acumulados operación por operación 
        (la suma acumulativa de la columna pips), 
    - - - - - - - - - - - - - - - - - - - -
    'profit_acm', que es el profit en capital, que acumula la cuenta 
        (también es la suma acumulativa de la columna profit)
'''

def f_columna_pips(param_data):
    """
    Parameters
    ---------
    :param:
        param_data: DataFrame : archivo de operaciones

    Returns
    ---------
    :return: 
        df_data: DataFrame

    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')

    """
    # Agregar pips
    param_data['pips'] = [
            (param_data.closeprice[i] - param_data.openprice[i])*f_pip_size(
                    param_data.symbol[i])
            if param_data.type[i] == 'buy' 
            else - (param_data.closeprice[i] - param_data.openprice[i])*f_pip_size(
                    param_data.symbol[i])
        for i in range(len(param_data))
        ]
    
    # Agregar los pips acumulados
    param_data['pips_acm'] = param_data.pips.cumsum()
    
    # Agregar rentabilidad acumulada
    param_data['profit_acm'] = param_data['profit'].cumsum()
    
    return param_data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Estadistica basica - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

''' f_estadisticas_ba: Una función cuya salida es un diccionario, 
    ese diccionario de salida debe de tener 2 llaves, 'df_1_tabla' y 'df_2_ranking'
    - - - - - - - - - - - - - - - - - - - -
        df_1_tabla:
            
        medida	        valor	descripcion
        Ops totales	      84	Operaciones totales
        Ganadoras	      46	Operaciones ganadoras
        Ganadoras_c	      20	Operaciones ganadoras de compra
        Ganadoras_v	      26	Operaciones perdedoras de venta
        Perdedoras	      38	Operaciones perdedoras
        Perdedoras_c	  19	Operaciones perdedoras de compra
        Perdedoras_v	  19	Operaciones perdedoras de venta
        Media (Profit)	1.205	Mediana de profit de operaciones   
        Media (Pips)	   3	Mediana de pips de operaciones
        r_efectividad	1.83	Ganadoras Totales/Operaciones Totales
        r_proporcion	1.21	Perdedoras Totales/Ganadoras Totales
        r_efectividad_c	  4.2	Ganadoras Compras/Operaciones Totales
        r_efectividad_v	3.23	Ganadoras Ventas/ Operaciones Totales
        - - - - - - - - - - - - - - - - - - - -
'''
def f_estadistica_ba(param_data):
    """
    Parameters
    ---------
    :param 
        param_archivo: DataFrame : archivo de operaciones

    Returns
    ---------
    :return: 
        df_1_tabla: DataFrame
        df_2_ranking: DataFrame

    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')

    """
    df_1_tabla = pd.DataFrame(
            {
                    'Ops totales':
                        [
                                len(param_data['order']), 
                                'Operaciones totales'
                                ],
                    
                    'Ganadoras':
                        [
                                len(param_data[param_data['pips_acm'] > 0]), 
                                'Operaciones ganadoras'
                                ], 
                        
                    'Ganadoras_c':
                        [
                                len([(param_data['type'] == 'buy') & (param_data['pips_acm'] > 0)]), 
                                'Operaciones ganadoras de compra'
                                ],
                        
                    'Ganadoras_v':
                        [
                                len(param_data[(param_data['type'] == 'sell') & (param_data['pips_acm'] > 0)]), 
                                'Operaciones ganadoras de venta'
                                ],
                        
                    'Perdedoras':
                        [
                                len(param_data[param_data['pips_acm'] < 0]), 
                                'Operaciones perdedoras'
                                ],
                        
                    'Perdedoras_c':
                        [
                                len(param_data[(param_data['type'] == 'buy') & (param_data['pips_acm'] < 0)]), 
                                'Operaciones perdedoras de compra'
                                ],
                        
                    'Perdedoras_v':
                        [
                                len(param_data[(param_data['type'] == 'sell') & (param_data['pips_acm'] < 0)]), 
                                'Operaciones perdedoras de venta'
                                ],
                        
                    'Media (Profit)':
                        [
                                param_data['profit'].median(), 
                                'Mediana de profit de las operaciones'
                                ],
                        
                    'Media (Pips)':
                        [
                                param_data['pips_acm'].median(), 
                                'Mediana de pips de las operaciones'
                                ],
                        
                    'r_efectividad':
                        [
                                len(param_data[param_data['pips_acm'] > 0]) / 
                                len(param_data['order']),
                                'Ganadoras Totales/Operaciones Totales'
                                ],
                        
                    'r_proporcion':
                        [
                                len(param_data[param_data['pips_acm'] > 0]) / 
                                len(param_data[param_data['pips_acm'] < 0]),
                                'Ganadoras Totales/ Perdedoras Totales'
                                ],
                        
                    'r_efectividad_c':
                        [
                                len(param_data[(param_data['type'] == 'buy') & (param_data['pips_acm'] > 0)]) /
                                len(param_data[param_data['type']=='buy']),
                            'Ganadoras Compras/ Operaciones Totales'
                            ],
                        
                    'r_efectividad_v':
                        [
                                len(param_data[(param_data['type'] == 'sell') & (param_data['pips_acm'] > 0)]) /
                                len(param_data[param_data['type'] == 'sell']),
                            'Ganadoras Ventas/ Operaciones Totales'
                            ]
                },
                index=['Valor', 'Descripcion']
            ).T
    
    # - - - - - - - - - - - - - - - - - - -
    
    # Symbols (unicos) en el DataFrame dado
    symbols = param_data.symbol.unique()
    
    # Creacion de DataFrame con ranking por symbol
    df_2_ranking = pd.DataFrame(
            {
                # Symbol
                i: 
                    # Porcentaje: del symbol que tiene profit positivo entre el total
                    len(param_data.query( f"(profit > 0) and (symbol == '{i}')")) /
                    len(param_data[param_data.symbol == i])
                    
            # Para todos los elementos de symbols 
            for i in symbols
            }, 
        
        # Nombre de la columna del DataFrame para ordenar
        index = ['ranking']).T.sort_values(
                by='ranking', 
                ascending=False)
        
   # df_2_ranking.applymap('{:.2f}%'.format)
    
    return df_1_tabla, df_2_ranking


# - - - - - - - - - - - - - - - - - - - - - - -
#%%
# PART III

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Capital acumulado - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion
    Es la columna de evolución de capital en la cuenta de trading, inicializala con 5,000 Usd 
    y va sumando (restando) las ganancias (perdidas) de la columna 'profit_acm'.
'''
def f_columna_capital_acm(param_data):
    """
    Parameters
    ---------
    :param: 
        param_data: DataFrame : archivo de operaciones

    Returns
    ---------
    :return: 
        param_data: DataFrame : archivo de operaciones

    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')
    """
    
    param_data['capital_acm'] = [float(5000.0 + param_data['profit_acm'][i]) for i in range(len(param_data['profit_acm']))]
    
    return param_data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Profit diarios - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion para sacar las perdidas o ganacias diarias
'''
def f_profit_diario(param_data):
    """
    Parameters
    ---------
    :param 
        param_data: DataFrame : archivo

    Returns
    ---------
    :return: 
        df_profit: DataFrame

    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')
    """
 
    dates = pd.DataFrame(
            {
            'timestamp' :   (pd.date_range(param_data['closetime'].min(), 
              param_data['closetime'].max(), normalize = True))
            }
        )

    profit_d = pd.DataFrame(
                [
                    [i[0], 
                     round(sum(i[1]['profit']), 2)
              ] for i in (list(param_data.groupby(pd.DatetimeIndex
                                        (param_data['closetime']).normalize())))], 
        columns = ['timestamp', 'profit_d'])
        
    df_profit = dates.merge(profit_d, how='outer', sort = True).fillna(0)

    df_profit['profit_acm'] = round(5000.0 + np.cumsum(df_profit['profit_d']), 2)
        
    return df_profit


# - - - - - - - - - - - - - - - - - - - - - FUNCION: Columna de rendimientos logaritmicos - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion para calcular rendimientos diarios: 
'''
def log_dailiy_rends(param_profit):
    """
    Parameters
    ---------
    :param 
        param_profit: DataFrame : archivo

    Returns
    ---------
    :return: 
        df: DataFrame

    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')
    """
    param_profit['rends'] = np.log(
                param_profit['profit_acm']/
                param_profit['profit_acm'].shift(1)).iloc[1:]
    
    return param_profit


# - - - - - - - - - - - - - - - - - - - - - - FUNCION: Medidas de Atribución al Desempeño - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion para sacar las Medidas de Atribución al Desempeño
    1.- Sharpe Ratio: (rp - rf)/std
    2.- Sortino Ratio: (rp - rf)/std(-)
'''
def f_estadisticas_mad(param_profit):
    
    rp = param_profit['rends']
    rf = 0.08
    
    df_estadistic = pd.DataFrame(
            {
                    'Sharpe':
                        [(rp.mean() - rf)/rp.std()],
                        
                    'Sortino_c':
                        [(rp.mean() - rf)/rp[rp < 0].std()],
                        
                    'Sortino_v':
                        [(rp.mean() - rf)/rp[rp > 0].std()],
                        
                    'Drawdown_capi_c':
                        [0],
                    
                    'Drawdown_capi_u':
                        [0],
                        
                    'Information':
                        [0]
                        
                        }
                )
                        
    return df_estadistic.T

    
    







