from dash import html
from dash import dcc
import datetime as dt
import data.binance_data as bd

######################## SUMMARY BINANCE LAYOUT ########################
summary_page = html.Div(
    children = [
        html.Div(
            className = 'row',
            children = [

                # Column for user control
                html.Div(
                    className = 'four columns div-user-controls',
                    children = [
                        html.H1('Cryptocurrency Analysis Dashboard'),
                        html.P(
                            '''
                            Select different days using the date picker or by selecting
                            different time frames on the histogram.
                            '''
                        ),
                        
                        # Dropdown to select date range
                        html.Div(
                            className = 'div-for-dropdown'
                            , children = [
                                dcc.DatePickerRange(
                                    id = 'cryto_date_picker',
                                    min_date_allowed = dt.datetime(2018, 1, 1),
                                    max_date_allowed = dt.datetime.today(),
                                    start_date = dt.datetime(2021, 1, 1),
                                    end_date = dt.datetime.today(),
                                    display_format = 'MMMM D, YYYY',
                                    style = {'border': '0px solid black'}
                                )
                            ]
                        ),
                        
                        # Dropdown to select crypto currency pair
                        html.Div(
                            className = 'div-for-dropdown',
                            children = [
                                dcc.Dropdown(
                                    id = 'crypto_pair_options',
                                    options = [
                                        {'label': currency, 'value': currency}
                                        for currency in bd.get_currency_pairs()
                                    ],
                                    multi = False,
                                    placeholder = 'Select a currency pair',
                                    value = 'BNBUSDT'
                                )
                            ]
                        ),
                        
                        # Dropdown to select kline interval
                        html.Div(
                            className = 'div-for-dropdown',
                            children = [
                                dcc.Dropdown(
                                    id = 'kline_intervals',
                                    options = bd.get_kline_intervals(),
                                    multi = False,
                                    placeholder = 'Select an interval',
                                    value = '1d'
                                )
                            ]
                        ),

                        # Submit button
                        html.Div(
                            className = 'div-for-button',
                            children = [
                                html.Button(
                                    id = 'submit_button',
                                    n_clicks = 0,
                                    children = 'Submit'
                                )
                            ]
                        )
                    ]
                ),

                # Column for app graphs and plots
                html.Div(
                    className = 'eight columns div-for-charts bg-grey',
                    children = [
                        html.Div(
                            children = [
                                html.H4('Historial Prices - Candlestick Chart'),
                                dcc.Graph(id = 'price_candlestick')
                            ]
                        ),
                        html.Div(
                            children = [
                                html.H4('Historial Volumes and Number of Trades'),
                                dcc.Graph(id = 'volume_bar')
                            ]
                        ),
                        html.Div(
                            children = [
                                html.H4('Historical Prices Change'),
                                dcc.Graph(id = 'price_change')
                            ]
                        )

                    ]
                )
            ]
        )
    ]
)

# summary_page = html.Div([
#     html.H1('Cryptocurrency Analysis Dashboard')
#     , html.Div(
#         className = 'app_slicer'
#         , children = [
#             html.H4('Enter a crypto currency pair:')
#             , dcc.Dropdown(
#                 id = 'crypto_pair_options'
#                 , options = currency_pair
#                 , value = 'BNBUSDT'
#                 , multi = False
#             )
#         ]
#     )
#     , html.Div(
#         className = 'app_slicer'
#         , children = [
#             html.H4('Select start and end dates:')
#             , dcc.DatePickerRange(
#                 id = 'cryto_date_picker'
#                 , min_date_allowed = dt.datetime(2018, 1, 1)
#                 , max_date_allowed = dt.datetime.today()
#                 , start_date = dt.datetime(2021, 1, 1)
#                 , end_date = dt.datetime.today()
#             )
#         ]
#         , style = {'marginLeft':'30px'}
#     )
#     , html.Div(
#         className = 'app_slicer'
#         , children = [
#             html.H4('Select intervals:')
#             , dcc.Dropdown(
#                 id = 'kline_intervals'
#                 , options = kline_intervals
#                 , value = '1d'
#                 , multi = False
#             )
#         ]
#         , style = {'marginLeft':'30px'}
#     )
#     , html.Div([
#         html.Button(
#             id = 'submit_button'
#             , n_clicks = 0
#             , children = 'Submit'
#             , style = {'fontSize':20, 'marginLeft':'30px'}
#         )
#     ], style={'display':'inline-block', 'marginLeft':'30px', 'marginTop':'60px'})
#     , html.Div(
#         className = 'chart_title'
#         , children = [
#             html.H3('Final report')
#         ]
#     )
#     , dcc.Graph(
#         id = 'volume_indicator'
#     )
#     , html.Div(
#         className = 'chart_title'
#         , children = [
#             html.H3('Historial Prices - Candlestick Chart')
#         ]
#     )
#     , dcc.Graph(
#         id = 'price_candlestick'
#     )
#     , html.Div(
#         className = 'chart_title'
#         , children = [
#             html.H3('Historial Volumes and Number of Trades')
#         ]
#     )
#     , dcc.Graph(
#         id = 'volume_bar'
#     )
#     , html.Div(
#         className = 'chart_title'
#         , children = [
#             html.H3('Historical Prices Change')
#         ]
#     )
#     , dcc.Graph(
#         id = 'price_change'
#     )
# ])
######################## END SUMMARY BINANCE LAYOUT ########################