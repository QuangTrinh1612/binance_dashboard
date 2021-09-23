from dash import html
from dash import dcc
import datetime as dt
import data.binance_data as bd

# Get Defined Currency Pairs from binance_data.py file
currency_pair = [{'label': currency, 'value': currency} for currency in bd.get_currency_pairs()]
kline_intervals = bd.get_kline_intervals()

######################## SUMMARY BINANCE LAYOUT ########################
summary_page = html.Div([
    html.H1('Cryptocurrency Analysis Dashboard')
    , html.Div(
        className = 'app_slicer'
        , children = [
            html.H4('Enter a crypto currency pair:')
            , dcc.Dropdown(
                id = 'crypto_pair_options'
                , options = currency_pair
                , value = 'BNBUSDT'
                , multi = False
            )
        ]
    )
    , html.Div(
        className = 'app_slicer'
        , children = [
            html.H4('Select start and end dates:')
            , dcc.DatePickerRange(
                id = 'cryto_date_picker'
                , min_date_allowed = dt.datetime(2018, 1, 1)
                , max_date_allowed = dt.datetime.today()
                , start_date = dt.datetime(2021, 1, 1)
                , end_date = dt.datetime.today()
            )
        ]
        , style = {'marginLeft':'30px'}
    )
    , html.Div(
        className = 'app_slicer'
        , children = [
            html.H4('Select intervals:')
            , dcc.Dropdown(
                id = 'kline_intervals'
                , options = kline_intervals
                , value = '1d'
                , multi = False
            )
        ]
        , style = {'marginLeft':'30px'}
    )
    , html.Div([
        html.Button(
            id = 'submit_button'
            , n_clicks = 0
            , children = 'Submit'
            , style = {'fontSize':20, 'marginLeft':'30px'}
        )
    ], style={'display':'inline-block', 'marginLeft':'30px', 'marginTop':'60px'})
    , html.Div(
        className = 'chart_title'
        , children = [
            html.H3('Final report')
        ]
    )
    , dcc.Graph(
        id = 'volume_indicator'
    )
    , html.Div(
        className = 'chart_title'
        , children = [
            html.H3('Historial Prices - Candlestick Chart')
        ]
    )
    , dcc.Graph(
        id = 'price_candlestick'
    )
    , html.Div(
        className = 'chart_title'
        , children = [
            html.H3('Historial Volumes and Number of Trades')
        ]
    )
    , dcc.Graph(
        id = 'volume_bar'
    )
    , html.Div(
        className = 'chart_title'
        , children = [
            html.H3('Historical Prices Change')
        ]
    )
    , dcc.Graph(
        id = 'price_change'
    )
])
######################## END SUMMARY BINANCE LAYOUT ########################