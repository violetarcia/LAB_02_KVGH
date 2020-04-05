
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
import bisect
import datos as dat

#%%
# PART II
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Leer archivo - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

''' Funcion para leer archivo de datos
        f_leer_archivo :
            Lee tu archivo historico de operaciones, 
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
        param_archivo = 'archivo_tradeview_2.xlsx'

    """

    # Leer archivo de datos y guardalo en un DataFrame
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Hoja1')

    # Convertir en minusculas el nombre de las columnas
    df_data.columns = [df_data.columns[i].lower() for i in range(len(df_data.columns))]

    # Asegurar que ciertas columnas son del tipo numerico
    num_col = ['order', 'size', 'openprice', 's/l', 't/p', 'closeprice', 'taxes', 'swap', 'profit']
    df_data[num_col] = df_data[num_col].apply(pd.to_numeric)
    
    # Acomodar por closetime
    df_data.sort_values(by=['closetime'], inplace = True)
    df_data.reset_index(inplace = True, drop = True)

    return df_data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: pip de instrumento - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
''' Función de pip por instrumento
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
    
''' Función que mide el tiempo el closetime y opentime
        f_columnas_tiempos:
            Agregar columna de transformaciones de tiempo
'''
def f_columna_tiempos(param_data):
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

'''Funcion f_columnas_pips: Agregar nuevas columnas: 
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

''' Funcion f_estadisticas_ba: 
        Una función cuya salida es un diccionario, 
        ese diccionario de salida debe de tener 2 llaves, 
        'df_1_tabla' y 'df_2_ranking'
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
                index = ['Valor', 'Descripcion']
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
    
    return { 'estadisticas': df_1_tabla, 'ranking': df_2_ranking}


# - - - - - - - - - - - - - - - - - - - - - - -
#%%
# PART III

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Capital acumulado - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion f_columna_capital_acm:
        Es la columna de evolución de capital en la cuenta de trading, 
        inicializalizandola con el capital de datos (inicial - 5,000)
        y va sumando las ganancias (restando perdidas) de la columna 'profit_acm'.
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
    
    # Quitar los sabados
    df_profit = df_profit[df_profit.timestamp.dt.weekday != 5]
    df_profit.reset_index(drop=True, inplace=True)
    df_profit['timestamp'] = df_profit['timestamp'].dt.date
    
    # Agregar el profit acumulado diario
    df_profit['profit_acm'] = round(dat.cap + np.cumsum(df_profit['profit_d']), 2)
        
    return df_profit


# - - - - - - - - - - - - - - - - - - - - - FUNCION: Columna de rendimientos logaritmicos - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion log_dailiy_rends:
        Funcion para calcular rendimientos logaritmicos de la columna especificada
'''
def log_dailiy_rends(param_profit, col):
    """
    Parameters
    ---------
    :param:
        param_profit: DataFrame : rendimientos de las operaciones diarias
        col : str : nombre de la columna a la que se le calcula tales rendimientos

    Returns
    ---------
    :return: 
        param_profit: DataFrame

    Debuggin
    ---------
        param_profit = f_profit_diario(f_leer_archivo('archivo_tradeview_1.xlsx'))
        col = 'profit_acm'
    """
    param_profit['rends'] = np.log(
                param_profit[col]/
                param_profit[col].shift(1)).iloc[1:]
    
    return param_profit


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Para calcular drawdown - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion f_drawdown 
        para calcular drawdown de la columna especificada del DataFrame
        Tal DF debe tener una columna 'timestamp' para que regrese la fecha
        de inicio y fin del Drawdown y Drawup
'''

def f_drawdown(param_profit, col, string = True):
    """
    Parameters
    ---------
    :param:
        param_profit: DataFrame : rendimientos de las operaciones diarias
        col: str : nombre de la columna para calcular drawdown
        string: bol : para salida tipo string

    Returns
    ---------
    :return: 
        param_profit: DataFrame

    Debuggin
    ---------
        param_profit = f_profit_diario(f_leer_archivo('archivo_tradeview_1.xlsx'))
        col = 'profit_acm'
    """
    down = (param_profit[col] - param_profit[col].cummax()) #/ param_profit[col].cummax()
    
    up = (param_profit[col] - param_profit[col].cummin()) #/ param_profit[col].cummin()
    
    # DOWN
    ans_down = round(down.min(), 3)
    fin_down = down.idxmin()
    
    ceros_down = down.loc[down == 0].index.tolist()
    bisect.insort(ceros_down, fin_down)
    
    inicio_down = ceros_down[ceros_down.index(fin_down) - 1]
    
    # UP
    ans_up = round(up.max(), 3)
    fin_up = up.idxmax()
    
    ceros_up = up.loc[up == 0].index.tolist()
    bisect.insort(ceros_up, fin_up)
    
    inicio_up = ceros_up[ceros_up.index(fin_up) - 1]
    
    if string: # [Up | fi | ff], [Down | fi | ff]
        return [str(ans_up) +" | "+ fecha(
                param_profit.timestamp[inicio_up]) + " | " +fecha(
                    param_profit.timestamp[fin_up])], [
                str(ans_down)+ " | " + fecha(
                        param_profit.timestamp[inicio_down]) + " | "+fecha(
                            param_profit.timestamp[fin_down])]
        
    else:
        return [ans_up, inicio_up, fin_up], [
                ans_down, inicio_down, fin_down]

def fecha(date):
    """
    Parameters
    ---------
    :param:
        date : timestamp : fecha

    Returns
    ---------
    :return: 
        str(date)

    Debuggin
    ---------
        date = pd.date()
    """
    return str(date)[:10]


# - - - - - - - - - - - - - - - - - - - - - - FUNCION: Medidas de Atribución al Desempeño - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion para sacar las Medidas de Atribución al Desempeño
    1.- Sharpe Ratio: (rp - rf)/std
    2.- Sortino Ratio: (rp - mar)/std(-)
'''
def f_estadisticas_mad(param_data):
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
    # -- DATOS --
    # Tasa libre de riesgo
    rf = dat.rf/360
    # Minimum Acceptable Return
    mar = dat.mar/360
    
    # Sacar el rend de profit diario de las Operaciones
    param_profit = log_dailiy_rends(f_profit_diario(param_data), 'profit_acm')
        # Solo de compra
    param_profit_compra = log_dailiy_rends(f_profit_diario(
                                            param_data[
                                                    param_data['type'] == 'buy']),
                                    'profit_acm')
        # Solo de venta
    param_profit_venta = log_dailiy_rends(f_profit_diario(
                                            param_data[
                                                    param_data['type'] == 'sell']), 
                                    'profit_acm')
    
    # Rendimientos
    rp = param_profit['rends']
    rp_c = param_profit_compra['rends']
    rp_v = param_profit_venta['rends']
    
    # Target Downside Deviation (sortinos)
    tdd_c = rp_c - mar
    tdd_c[tdd_c > 0] = 0
    
    tdd_v = rp_v - mar
    tdd_v[tdd_v > 0] = 0
    
    
    # -- BENCHMARK --
    # Descarga de datos
    sp500= f_precios(dat.benchmark, param_profit['timestamp'].min(), param_profit['timestamp'].max())
    # Rendimientos
    sp500_rends = log_dailiy_rends(sp500, 'Close')
    # Media de Benchmark
    benchmark = sp500_rends['rends'].mean()
    # Merge por fechas
    merge_ben = sp500_rends.merge(pd.DataFrame(param_profit), 
                        right_on='timestamp', left_on='timestamp')
    # Agregar columna de diferencia
    merge_ben['dif'] = merge_ben['rends_y'] - merge_ben['rends_x']
    
    
    # -- DRAWDOWN --
    draw_up, draw_down = f_drawdown(param_profit, 'profit_acm')

    # Crear DataFrame con estadisticas
    df_estadistic = pd.DataFrame(
            {
                    'Sharpe':
                        [(rp.mean() - rf) / rp.std()],
                        
                    'Sortino_c':
                        [(rp_c.mean() - mar) / (((tdd_c**2).mean())**(0.5))],
                        
                    'Sortino_v':
                        [(rp_v.mean() - mar) / (((tdd_v**2).mean())**(0.5))],
                        
                    'Drawdown_capi':
                        draw_down,
                    
                    'Drawup_capi':
                        draw_up,
                        
                    'Information':
                        [(rp.mean() - benchmark)/merge_ben.dif.std()]
                        
                        }, index = ['values']
                )
                        
    return df_estadistic.T

    
# - - - - - - - - - - - - - - - - - - - - - - -
#%%
# PART IV
    
# - - - - - - - - - - - - - - - - - - - - - - FUNCION: Descargar el precio dado timestamp - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion para descargar el precio de apertura en dado timestamp
    Especificar el instrumentos 'eurusd'
    Y el timestamp pd.to_datetime("2019-08-27 09:16:01").tz_localize('GMT')
'''
    
def f_precios(*args):
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
        DataFram: precios del indice

    Debuggin
    ---------
        instrument = 'EUR_USD'
        date = pd.to_datetime("2019-07-06 00:00:00")
    """ 
    # Parametros 
    param = args
    # Inicializar api de OANDA
    api = API(environment = "practice", access_token = dat.OANDA_ACCESS_TOKEN)
    
    # Para los precios de la parte 4 y buscar ocurrencias
    if len(param) == 2:
        # Convertir en string la fecha
        fecha = param[1].strftime('%Y-%m-%dT%H:%M:%S')
        # Parametros
        parameters = {"count": 1, "granularity": 'M1', "price": "M", "dailyAlignment": 16, "from": fecha}
        # Definir el instrumento del que se quiere el precio
        r = instruments.InstrumentsCandles(instrument = param[0], params = parameters)
        # Descargarlo de OANDA
        response = api.request(r)
        # En fomato candles 'open, low, high, close'
        prices = response.get("candles")
        # Regresar el precio de apertura
        return float(prices[0]['mid']['o'])
    
    # Para el benchmark
    if len(param) == 3:
        # Fechas del rango que se quieren
        fecha_inicio = param[1].strftime('%Y-%m-%dT%H:%M:%S')
        fecha_final = param[2].strftime('%Y-%m-%dT%H:%M:%S')
        # Parametros
        parameters = {"granularity": 'D', "price": "M", "dailyAlignment": 16, 
                      "from": fecha_inicio, "to": fecha_final}
        # Definir el instrumento del que se quiere el precio
        r = instruments.InstrumentsCandles(instrument = param[0], params = parameters)
        # Descargarlo de OANDA
        response = api.request(r)
        # En fomato candles 'open, low, high, close'
        prices = response.get("candles")
        # Regresar el precio de apertura
        return pd.DataFrame([ [pd.to_datetime(i['time']).date(), float(i['mid']['c'])] for i in prices ], 
                            columns = ['timestamp', 'Close'])


# - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Cambiar string para adaptarlo - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
'''Funcion que cambia el formato del string del instrumento
    en el archivo el symbol es de forma 'eurusd'
    pero para poder descargar el precio de tal es necesario que este en
    forma de 'EUR_USD', y es lo que hace esta funcion
'''
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
                                     
    # Agregar perdida flotante
    for i in range(len(prec_posibles_ocu)):
        # (Precio on close - Precio de apertura) *
        # Profit / (Precio de cierre - Precio de apertura)
        prec_posibles_ocu[i]['perdida_flot'] = (prec_posibles_ocu[i][
                'price_on_close'] - prec_posibles_ocu[i][
                        'openprice']) * (prec_posibles_ocu[i][
                                'profit'] / (prec_posibles_ocu[i][
                                        'closeprice'] - prec_posibles_ocu[i][
                                                'openprice'])) 
                
    # Llenar lista con Diccionarios
    ocu = []
    k = 0
    for j in range(len(precios)):
        # Para guardar la perdida flotante y tomar la mayor
        profits, indices = [],  []
        for i in range(len(precios[j])):
            ''' Si el precio en closetime ganador es menor al precio de apertura 
                 de la operacion de compra, o que el precio en closetime sea mayor
                 y la operacion es de tipo venta'''
            if precios[j][i] < pos_ocu_concat[j]['openprice'][
                    i+1] and pos_ocu_concat[j]['type'][i+1] == 'buy' or precios[
                            j][i] > pos_ocu_concat[j]['openprice'][
                                    i+1] and pos_ocu_concat[j]['type'][i+1] == 'sell':
                
                # Guardar el profit para tomar el maximo (abs)
                profits.append((prec_posibles_ocu[j]['perdida_flot'][i+1]))
                # Guardar el indice del profit
                indices.append(i+1)
        #print(profits, indices)
        
        if profits != []:
            ind = profits.index(min(profits))
            k +=1
            new_profit = round((prec_posibles_ocu[j]['price_on_close'][indices[ind]] - 
                                pos_ocu_concat[j]['openprice'][indices[ind]]) *
                                ((pos_ocu_concat[j]['profit'][indices[ind]]) /
                                 ( pos_ocu_concat[j]['closeprice'][indices[ind]] - 
                                  pos_ocu_concat[j]['openprice'][indices[ind]])), 3)
                            
            ocu.append({ 'ocurrencia %d'%k:
                                
                                    { 'timestamp':
                                        pos_ocu_concat[j]['closetime'][0],
                                        
                                      'operaciones':
                                          
                                             { 'ganadora':
                                                 
                                                    {
                                                        'instrumento':
                                                            pos_ocu_concat[j]['symbol'][0],
                                                        'sentido':
                                                            pos_ocu_concat[j]['type'][0],
                                                        'volumen':
                                                            pos_ocu_concat[j]['size'][0],
                                                        'capital_ganadora':
                                                            pos_ocu_concat[j]['profit'][0],
                                                        'capital_acm':
                                                            pos_ocu_concat[j]['capital_acm'][0]
                                                         },
                                                     
                                               'perdedora':
                                                    {
                                                        'instrumento':
                                                            pos_ocu_concat[j]['symbol'][indices[ind]],
                                                        'sentido':
                                                            pos_ocu_concat[j]['type'][indices[ind]],
                                                        'volumen':
                                                            pos_ocu_concat[j]['size'][indices[ind]],
                                                        'profit':
                                                            pos_ocu_concat[j]['profit'][indices[ind]],
                                                        'capital_perdedora':
                                                            new_profit
                                                         }
                                                 },
        
                                      'ratio_cp_capital_acm':
                                            round(abs(new_profit/pos_ocu_concat[j]['capital_acm'][0])*100, 3),
                                            
                                      'ratio_cg_capital_acm': 
                                            round(abs(pos_ocu_concat[j]['profit'][0]/
                                             pos_ocu_concat[j]['capital_acm'][0])*100, 3),
                                      'ratio_cp_cg':
                                            round(abs(new_profit/pos_ocu_concat[j]['profit'][0]), 3)
                                        }
                                }
                        )
                            
            
    datos = pd.concat([
            pd.DataFrame([
            ocu[i-1]['ocurrencia %d'%i]['ratio_cp_capital_acm'],
            ocu[i-1]['ocurrencia %d'%i]['ratio_cg_capital_acm'],
            ocu[i-1]['ocurrencia %d'%i]['ratio_cp_cg'],
            ocu[i-1]['ocurrencia %d'%i]['operaciones']['ganadora']['capital_acm']
                    ])
            for i in range(1, len(ocu)+1)], axis=1, ignore_index = True).T
    '''
    - Status_quo:  % de ocurrencias donde capital_perdedora/capital_acm < capital_ganadora/capital_acm.
    - Aversion_perdida: % de ocurrencias donde capital_perdedora/capital_ganadora es > 1.5 ​
    - Sensibilidad_decreciente: dado que observes que  el último valor de capital_ganadora 
    fue mayor que el primer valor de capital_ganadora y que  el último capital_perdedora fue mayor 
    que el primer valor de capital_perdedora.
    '''
    first_last = pd.concat([datos.iloc[0,:], datos.iloc[len(datos)-1, :]], axis=1, ignore_index=True).T
    resultados = pd.DataFrame(
                            { 
                                    'ocurrencias':
                                        [len(datos)],
                                        
                                    'status_quo':
                                        [len([1 for i in range(len(datos)) 
                                            if datos.iloc[i,0] < datos.iloc[i,1]]) /
                                         len(datos)],
    
                                    'aversion_perdida':
                                        [len([1 for i in range(len(datos)) 
                                            if datos.iloc[i,2] > 1.5]) / 
                                        len(datos)],
    
                                    'sensibilidad_decreciente':
                                        ['si' if first_last.iloc[0,3] < first_last.iloc[
                                                1,3] and first_last.iloc[1,2] > 1.5 and (
                                                    first_last.iloc[0,0] < first_last.iloc[1,0] or 
                                                    first_last.iloc[0,1] < first_last.iloc[1,1]
                                        ) else 'no']
                                    }, index = ['Valor']
                                ).T
                
    return {'ocurrencias': ocu, 'resultados':resultados}


def dataframe_ocurrencias(operaciones):
    datos = pd.concat([
            pd.DataFrame([       
                    operaciones[i-1]['ocurrencia %d'%i]['timestamp'],
                    operaciones[i-1]['ocurrencia %d'%i]['operaciones']['ganadora']['capital_acm'],
                    operaciones[i-1]['ocurrencia %d'%i]['operaciones']['ganadora']['instrumento'],
                    operaciones[i-1]['ocurrencia %d'%i]['operaciones']['ganadora']['capital_ganadora'],
                    operaciones[i-1]['ocurrencia %d'%i]['ratio_cg_capital_acm'],
                    operaciones[i-1]['ocurrencia %d'%i]['operaciones']['perdedora']['instrumento'],
                    operaciones[i-1]['ocurrencia %d'%i]['operaciones']['perdedora']['capital_perdedora'],
                    operaciones[i-1]['ocurrencia %d'%i]['ratio_cp_capital_acm'],
                    operaciones[i-1]['ocurrencia %d'%i]['operaciones']['perdedora']['profit'],
                    operaciones[i-1]['ocurrencia %d'%i]['ratio_cp_cg']])
            for i in range(1, len(operaciones)+1)], axis=1, ignore_index = True).T


    datos.columns = ['CloseTime', 'Capital_acm', 'Ganadora', 'Gan_Profit', 'Gan/Cap_acm',
                    'Perdedora', 'Perdida_flotante', 'Perd/Cap_acm', 'Perd_Tot',
                    'Ratio cp/cg']
    return datos




                                       



