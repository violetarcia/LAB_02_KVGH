
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - procesamiento de datos
# -- mantiene: violetarcia
# -- repositorio: https://github.com/violetarcia/LAB_02_KVGH.git
# -- ------------------------------------------------------------------------------------ -- #
from oandapyV20 import API                                
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
import numpy as np
import datos as dat

#%%
# PART II
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

    # lista de pips por instrumento
    pips_instrument = {
                'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                 'chfjpy': 100,'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 
                 'usdmxn': 10000,'audusd': 10000, 'nzdusd': 10000, 'usdchf': 10000,
                 'eurgbp': 10000, 'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000,
                 'gbpnzd': 10000, 'gbpchf': 10000, 'gbpaud': 10000, 'audnzd': 10000, 
                 'nzdcad': 10000, 'audcad': 10000, 'xauusd': 10, 'xagusd': 10, 'btcusd': 1
                 }

    return pips_instrument[param_ins.lower()]


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
    param_data['time'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta/ 1e9
                            for i in range(len(param_data['closetime']))]

    return param_data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Columna de pip - #
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
        *Media (Pips)	   3	Mediana de pips de operaciones
        r_efectividad	  0.55 	Ganadoras Totales/Operaciones Totales
        r_proporcion	  1.21	Perdedoras Totales/Ganadoras Totales
        r_efectividad_c	  0.24	Ganadoras Compras/Operaciones Totales
        r_efectividad_v	  0.31	Ganadoras Ventas/ Operaciones Totales
        - - - - - - - - - - - - - - - - - - - -
'''
def f_estadistica_ba(param_data):
    """
    Parameters
    ---------
    :param:
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
                                len(param_data[param_data['profit'] >= 0]), 
                                'Operaciones ganadoras'
                                ], 
                        
                    'Ganadoras_c':
                        [
                                len(param_data[(param_data['type'] == 'buy') & (param_data['profit'] >= 0)]), 
                                'Operaciones ganadoras de compra'
                                ],
                        
                    'Ganadoras_v':
                        [
                                len(param_data[(param_data['type'] == 'sell') & (param_data['profit'] >= 0)]), 
                                'Operaciones ganadoras de venta'
                                ],
                        
                    'Perdedoras':
                        [
                                len(param_data[param_data['profit'] <= 0]), 
                                'Operaciones perdedoras'
                                ],
                        
                    'Perdedoras_c':
                        [
                                len(param_data[(param_data['type'] == 'buy') & (param_data['profit'] <= 0)]), 
                                'Operaciones perdedoras de compra'
                                ],
                        
                    'Perdedoras_v':
                        [
                                len(param_data[(param_data['type'] == 'sell') & (param_data['profit'] <= 0)]), 
                                'Operaciones perdedoras de venta'
                                ],
                        
                    'Media (Profit)':
                        [
                                param_data['profit'].median(), 
                                'Mediana de profit de las operaciones'
                                ],
                        
                    'Media (Pips)':
                        [
                                param_data['pips'].median(), 
                                'Mediana de pips de las operaciones'
                                ],
                        
                    'r_efectividad':
                        [
                                len(param_data[param_data['profit'] > 0]) / 
                                len(param_data['order']),
                                'Ganadoras Totales/Operaciones Totales'
                                ],
                        
                    'r_proporcion':
                        [
                                len(param_data[param_data['profit'] > 0]) / 
                                len(param_data[param_data['profit'] < 0]),
                                'Ganadoras Totales/ Perdedoras Totales'
                                ],
                        
                    'r_efectividad_c':
                        [
                                len(param_data[(param_data['type'] == 'buy') & (param_data['profit'] >= 0)]) /
                                len(param_data['order']),
                            'Ganadoras Compras/ Operaciones Totales'
                            ],
                        
                    'r_efectividad_v':
                        [
                                len(param_data[(param_data['type'] == 'sell') & (param_data['profit'] >= 0)]) /
                                len(param_data['order']),
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
    
    param_data['capital_acm'] = [float(dat.cap + param_data['profit_acm'][i]) 
                                    for i in range(len(param_data['profit_acm']))]
    
    return param_data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Profit diarios - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion para sacar las perdidas o ganacias diarias
'''
def f_profit_diario(param_data):
    """
    Parameters
    ---------
    :param:
        param_data: DataFrame : archivo con operaciones

    Returns
    ---------
    :return: 
        df_profit: DataFrame

    Debuggin
    ---------
        param_data = f_leer_archivo('archivo_tradeview_1.xlsx')
    """
    # Todas las fechas del rango desde que se cerro la pirmera hasta la ultima
    dates = pd.DataFrame(
            {
            'timestamp' :   (pd.date_range(param_data['closetime'].min(), 
              param_data['closetime'].max(), normalize = True))
            }
        )
            
    # Agrupar y sumar profit por dia
    profit_d = pd.DataFrame(
                [   # Fecha del dia
                    [i[0], 
                     # Suma del profit de las operaciones cerradas en el dia
                     round(sum(i[1]['profit']), 2)
              ] for i in (list(param_data.groupby(pd.DatetimeIndex
                                        (param_data['closetime']).normalize())))], 
        columns = ['timestamp', 'profit_d'])
    
    # Merge todas la fechas con aquellas en las que se hicieron operaciones
    df_profit = dates.merge(profit_d, how='outer', sort = True).fillna(0)
    
    # Agregar el profit acumulado diario
    df_profit['profit_acm'] = round(dat.cap + np.cumsum(df_profit['profit_d']), 2)
        
    return df_profit


# - - - - - - - - - - - - - - - - - - - - - FUNCION: Columna de rendimientos logaritmicos - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion para calcular rendimientos logaritmicos diarios: 
'''
def log_dailiy_rends(param_profit, col):
    """
    Parameters
    ---------
    :param:
        param_profit: DataFrame : rendimientos de las operaciones diarias

    Returns
    ---------
    :return: 
        param_profit: DataFrame

    Debuggin
    ---------
        param_profit = f_profit_diario(f_leer_archivo('archivo_tradeview_1.xlsx'))
    """
    param_profit['rends'] = np.log(
                param_profit[col]/
                param_profit[col].shift(1)).iloc[1:]
    
    return param_profit


# - - - - - - - - - - - - - - - - - - - - - FUNCION: Columna de rendimientos logaritmicos - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion para calcular drawdown: 
'''
def drawdown(param_profit, col):
    """
    Parameters
    ---------
    :param:
        param_profit: DataFrame : rendimientos de las operaciones diarias

    Returns
    ---------
    :return: 
        param_profit: DataFrame

    Debuggin
    ---------
        param_profit = f_profit_diario(f_leer_archivo('archivo_tradeview_1.xlsx'))
    """
    param_profit['down'] = (param_profit[col] - param_profit[col].cummax())
    param_profit['up'] = param_profit[col].cummax()
    
    return param_profit


# - - - - - - - - - - - - - - - - - - - - - - FUNCION: Medidas de Atribución al Desempeño - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion para sacar las Medidas de Atribución al Desempeño
    1.- Sharpe Ratio: (rp - rf)/std
    2.- Sortino Ratio: (rp - mar)/std(-)
'''
def f_estadisticas_mad(param_profit):
    """
    Parameters
    ---------
    :param:
        param_profit: DataFrame : rendimientos de las operaciones diarias

    Returns
    ---------
    :return: 
        df_estadistic: DataFrame

    Debuggin
    ---------
        param_profit = f_profit_diario(f_leer_archivo('archivo_tradeview_1.xlsx'))
    """
    # Rendimientos
    rp = param_profit['rends']
    
    # -- DATOS --
    # Tasa libre de riesgo
    rf = dat.rf/360
    # Benchmark
    benchmark = dat.benchmark
    
    # Crear DataFrame con estadisticas
    df_estadistic = pd.DataFrame(
            {
                    'Sharpe':
                        [(rp.mean() - rf) / rp.std()],
                        
                    'Sortino_c':
                        [(rp.mean() - rf) / (rp[rp < 0].std())],
                        
                    'Sortino_v':
                        [(rp.mean() - rf) / (rp[rp > 0].std())],
                        
                    'Drawdown_capi_c':
                        [1 - param_profit['profit_acm'].min()/dat.cap],
                    
                    'Drawdown_capi_u':
                        [1 - param_profit['profit_acm'].max()/dat.cap],
                        
                    'Information':
                        [rp.mean() / benchmark]
                        
                        }
                )
                        
    return df_estadistic.T

    
# - - - - - - - - - - - - - - - - - - - - - - -
#%%
# PART IV
    
def f_precios(param_instrument, date):
    """
    Parameters
    ---------
    :param: 
        instrument: str : instrumento del precio que se requiere
        date : date : fecha del dia del precio

    Returns
    ---------
    :return: 
        float: precio del intrumento en tal fecha

    Debuggin
    ---------
        instrument = 'EUR_USD'
        date = pd.to_datetime("2019-07-06 00:00:00")
    """ 
    # Inicializar api de OANDA
    api = API(environment = "practice", access_token = dat.OANDA_ACCESS_TOKEN)
    # Convertir en string la fecha
    fecha = date.strftime('%Y-%m-%dT%H:%M:%S')
    # Parametros
    parameters = {"count": 1, "granularity": 'M1', "price": "M", "dailyAlignment": 16, "from": fecha}
    # Definir el instrumento del que se quiere el precio
    r = instruments.InstrumentsCandles(instrument = param_instrument, params = parameters)
    # Descargarlo de OANDA
    response = api.request(r)
    # En fomato candles 'open, low, high, close'
    prices = response.get("candles")
    # Regresar el precio de apertura
    return float(prices[0]['mid']['o'])


def f_instrument(ins):
    """
    Parameters
    ---------
    :param: 
        ins: str : instrumento del precio que se requiere

    Returns
    ---------
    :return: 
        str: intrumento en formato 'EUR_USD'

    Debuggin
    ---------
        instrument = 'eurusd'
    """ 
    return ins.upper()[:3] + '_' + ins.upper()[3:]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Sesgos cognitivos - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion
    Diseñar y calcular una función para obtener evidencia sobre 
    la presencia de sesgos cognitivos en un trader
    - - - - - - - -
    Principio I : Proporcion de la ganadora y perdedora respecto al capital
        - Calcular ratio ganadora/capital, perdedora/capital
    Principio II : Proporcion perdedora / ganadora > 1.5
        - Ancla sera ganadoras. DF con ganadoras
    
'''
def f_sesgos_cognitivo(param_data):
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
    
    param_data['profit/cap'] = [
              (param_data['profit'][i]/dat.cap)*100 if i == 0 else 
              (param_data['profit'][i]/param_data['capital_acm'][i-1])*100
                        for i in range(len(param_data['profit']))
                        ]
    
    param_data['resultado'] = ['ganadora' if param_data['profit'][i] > 0 
                                           else 'perdedora' 
                                for i in range(len(param_data['profit']))]
    
    # Seleccionar solo los ganadores
    df_winners = param_data[param_data['profit'] > 0]
    df_winners.reset_index(inplace = True, drop = True)
    
    # De operaciones ganadores, buscar operaciones abiertas cuando se cerraron
    posibles_ocurrencias = [
                [
                        param_data.iloc[i,:] for i in range(len(param_data)) if 
              param_data['opentime'][i] < df_winners['opentime'][j]  and 
              param_data['closetime'][i] > df_winners['closetime'][j] or
              df_winners['closetime'][j] > param_data['opentime'][i] > df_winners['opentime'][j] and
              param_data['closetime'][i] > df_winners['closetime'][j]
                    ]
                for j in range(len(df_winners))
                ]
    
    # Concatenar para tenerlo en un solo DF, donde el primero es la operacion ancla
    pos_ocu_concat = [pd.concat(
                                    [ # Operacion ganadora
                                        df_winners.iloc[i, :], 
                                      # Operaciones abiertas
                                        pd.concat(posibles_ocurrencias[i], axis = 1)
                                        ], 
                    axis = 1, sort=False, ignore_index = True).T
                        for i in range(len(posibles_ocurrencias)) if posibles_ocurrencias[i] != []]
    
    # Descargar precios de acuerdo al closetime de la primera operacion (la ganadora)          
    precios = [
                [
                f_precios(
                    f_instrument(pos_ocu_concat[j]['symbol'][i+1]), 
                    pos_ocu_concat[j]['closetime'][0]
                    )
                for i in range(len(pos_ocu_concat[j]) - 1)
                ]
            for j in range(len(pos_ocu_concat))
            ]
    
    # Concatenar los precios
    prec_posibles_ocu = [pd.concat(
                                [ 
                                    pos_ocu_concat[i],
                                     pd.concat(
                                                 [
                                                    pd.DataFrame([0], columns=['price_on_close']), 
                                                    pd.DataFrame(precios[i], columns=['price_on_close'])
                                                    ], sort=False, ignore_index = True)
                                    ], axis = 1, sort=False)
                        for i in range(len(pos_ocu_concat))]
                
    # Llenar lista con Diccionarios
    df = []
    k = 0
    for j in range(len(precios)):
        profits, indices = [],  []
        for i in range(len(precios[j])):
            if precios[j][i] < pos_ocu_concat[j]['openprice'][
                    i+1] and pos_ocu_concat[j]['type'][i+1] == 'buy' or precios[
                            j][i] > pos_ocu_concat[j]['openprice'][
                                    i+1] and pos_ocu_concat[j]['type'][i+1] == 'sell':
                # Guardar el profit para tomar el maximo
                profits.append(pos_ocu_concat[j]['profit'][i+1])
                indices.append(i+1)
        #print(profits, indices)
        
        if profits != []:
            ind = profits.index(max(profits))  
            k +=1
            df.append([{ 'ocurrencia %d'%k:
                                [
                                    { 'timestamp':
                                        [pos_ocu_concat[j]['closetime'][0]],
                                        
                                      'operaciones':
                                          [
                                             { 'ganadora':
                                                 [
                                                    {
                                                        'instrumento':
                                                            [pos_ocu_concat[j]['symbol'][0]],
                                                        'profit':
                                                            [pos_ocu_concat[j]['profit'][0]],
                                                        'sentido':
                                                            [pos_ocu_concat[j]['type'][0]],
                                                        'capital_ganadora':
                                                            [pos_ocu_concat[j]['capital_acm'][0]],
                                                        'resultado':
                                                            [pos_ocu_concat[j]['resultado'][0]]
                                                         }
                                                    ],
                                                     
                                               'perdedora':
                                                  [
                                                    {
                                                        'instrumento':
                                                            [pos_ocu_concat[j]['symbol'][indices[ind]]],
                                                        'profit':
                                                            [pos_ocu_concat[j]['profit'][indices[ind]]],
                                                        'sentido':
                                                            [pos_ocu_concat[j]['type'][indices[ind]]],
                                                        'capital_perdedora':
                                                            [pos_ocu_concat[j]['capital_acm'][indices[ind]]],
                                                        'resultado':
                                                            [pos_ocu_concat[j]['resultado'][indices[ind]]],
                                                        'precio_apertura':
                                                            [pos_ocu_concat[j]['openprice'][indices[ind]]],
                                                        'precio_cierre':
                                                            [pos_ocu_concat[j]['closeprice'][indices[ind]]],
                                                        'precio_on_close':
                                                            [prec_posibles_ocu[j]['price_on_close'][indices[ind]]]
                                                           
                                                            }
                                                       ]
                                                  }
                                             ]
                                        }
                                    ]
                                }
                            ]
                        )
            
    
                
    return df


#%%










