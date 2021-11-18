import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import taverndata, heroprice


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Tavern Data |', href='/apps/taverndata'),
        dcc.Link('Hero Price Checker', href='/apps/pricecheck'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/taverndata':
        return taverndata.layout
    if pathname == '/apps/pricecheck':
        return heroprice.layout
    else:
        return taverndata.layout


if __name__ == '__main__':
    app.run_server(debug=False)