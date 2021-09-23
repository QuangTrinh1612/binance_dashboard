import dash
from layout import summary_page
from callbacks import graph_callbacks

app = dash.Dash(__name__)
app.title = 'Cryptocurrency App'

# App Layout
app.layout = summary_page
graph_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)