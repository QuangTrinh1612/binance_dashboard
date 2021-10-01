import plotly.graph_objs as go
import data.binance_data as bd
from dash.dependencies import Input, Output, State

def graph_callbacks(app):
    ######################## Binance Summary Page Callbacks ########################
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
            , increasing_line_color= '#90EE90', decreasing_line_color= '#FF7F7F'
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
            , marker_color = '#FF7F7F'
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
            , layout = go.Layout(
                title = {
                    'text': currency_pair + ' Candlestick Graph'
                    , 'font': {'color': '#d3d3d3'}
                }
                , paper_bgcolor = '#232533'
                , plot_bgcolor = '#232533'
                , xaxis = {'showgrid': False, 'color': '#d3d3d3'}
                , yaxis = {'showgrid': False, 'zeroline': False, 'color': '#d3d3d3'}
            )
        )
        volume_fig = go.Figure(
            data = [trace_volume, trace_num_trade]
            , layout = go.Layout(
                title = {
                    'text': currency_pair + ' Volume Bar Chart'
                    , 'font': {'color': '#d3d3d3'}
                }
                , paper_bgcolor = '#232533'
                , plot_bgcolor = '#232533'
                , xaxis = {'showgrid': False, 'color': '#d3d3d3'}
                , yaxis = {'title':'Trade Volume', 'showgrid': False, 'zeroline': False, 'color': '#d3d3d3'}
                , yaxis2 = {'title':'Number of Trades', 'overlaying':'y', 'side':'right', 'showgrid': False, 'zeroline': False, 'color': '#d3d3d3'}
                , legend = {'yanchor':'top', 'xanchor':'left', 'font':{'color': '#d3d3d3'}}
            )
        )
        price_change_fig = go.Figure(
            data = trace_price_change
            , layout = go.Layout(
                title = {
                    'text': currency_pair + ' Price Change - Line Graph'
                    , 'font': {'color': '#d3d3d3'}
                }
                , paper_bgcolor = '#232533'
                , plot_bgcolor = '#232533'
                , xaxis = {'showgrid': False, 'color': '#d3d3d3'}
                , yaxis = {'showgrid': False, 'zeroline': False, 'color': '#d3d3d3'}
            )
        )

        return price_fig, volume_fig, price_change_fig