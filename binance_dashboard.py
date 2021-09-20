import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import datetime as dt
import talib as ta
import binance_data as bd

app = dash.Dash()
app.title = 'Cryptocurrency App'

# Get Defined Currency Pairs from binance_data.py file
currency_pair = [{'label': currency, 'value': currency} for currency in bd.get_currency_pairs()]
kline_intervals = bd.get_kline_intervals()

# App Layout
app.layout = html.Div([
    html.H1('Cryptocurrency Analysis Dashboard')
    , html.Div(
        className = 'app_slicer'
        , children = [
            html.H3('Enter a crypto currency pair:', style={'paddingRight':'30px'})
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
            html.H3('Select start and end dates:')
            , dcc.DatePickerRange(
                id = 'cryto_date_picker'
                , min_date_allowed = dt.datetime(2018, 1, 1)
                , max_date_allowed = dt.datetime.today()
                , start_date = dt.datetime(2021, 1, 1)
                , end_date = dt.datetime.today()
            )
        ]
    )
    , html.Div(
        className = 'app_slicer'
        , children = [
            html.H3('Select intervals:')
            , dcc.Dropdown(
                id = 'kline_intervals'
                , options = kline_intervals
                , value = '1d'
                , multi = False
            )
        ]
    )
    , html.Div([
        html.Button(
            id = 'submit_button'
            , n_clicks = 0
            , children = 'Submit'
            , style = {'fontSize':24, 'marginLeft':'30px'}
        )
    ], style={'display':'inline-block'})
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

@app.callback(
    [
        Output(component_id='price_candlestick', component_property='figure')
        , Output(component_id='volume_bar', component_property='figure')
        , Output(component_id='price_change', component_property='figure')
    ]
    , [Input('submit_button', 'n_clicks')]
    , [
        State('crypto_pair_options', 'value')
        , State('cryto_date_picker', 'start_date')
        , State('cryto_date_picker', 'end_date')
        , State('kline_intervals', 'value')
    ]
)
def update_graph(n_clicks:int, currency_pair:str, start_date:str, end_date:str, interval:list) -> dict:
    df = bd.get_historical_ohlc_data(
        symbol = currency_pair
        , start_str = start_date
        , end_str = end_date
        , interval = interval
    )

    # Create dash traces
    trace_price = go.Candlestick(
        x = df.open_date
        , open = df.open, high = df.high
        , low = df.low, close = df.close
        , increasing_line_color= 'cyan', decreasing_line_color= 'gray'
    )
    trace_volume = go.Bar(
        x = df.open_date
        , y = df.volume
        , hovertemplate = 'Date %{x}: Volume as %{y}'
        , name = 'Trade Volume'
        , offsetgroup = 0
        , yaxis = 'y1'
    )
    trace_num_trade = go.Bar(
        x = df.open_date
        , y = df.num_trades
        , hovertemplate = 'Date %{x}: Number of Trades as %{y}'
        , name = 'Number of trades'
        , offsetgroup = 1
        , yaxis = 'y2'
    )
    trace_price_change = go.Scatter(
        x = df.open_date
        , y = df.open - df.close
        , mode = 'lines'
        , name = 'Price Changes'
    )

    # Dash Plotly Figures
    price_fig = go.Figure(
        data = trace_price
        , layout = go.Layout(title=currency_pair+' Candlestick Graph')
    )
    volume_fig = go.Figure(
        data = [trace_volume, trace_num_trade]
        , layout = go.Layout(
            title=currency_pair+' Volume Bar Chart'
            , yaxis={'title':'Trade Volume'}
            , yaxis2={'title':'Number of Trades', 'overlaying':'y', 'side':'right'}
            , legend={'yanchor':'top', 'xanchor':'left'}
        )
    )
    price_change_fig = go.Figure(
        data = trace_price_change
        , layout = go.Layout(title=currency_pair+' Price Change - Line Graph')
    )

    return price_fig, volume_fig, price_change_fig

if __name__ == '__main__':
    app.run_server(debug=True)