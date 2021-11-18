from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connect to main failedapp.py file
from failedapp import app
from failedapp import server

# Connect to your app pages
from apps import taverndata, heroprice

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Tavern Data |', href='/taverndata'),
        dcc.Link(' Hero Price Checker', href='/heroprice'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/taverndata':
        return taverndata.layout
    if pathname == '/heroprice':
        return heroprice.layout
    else:
        return taverndata.layout
        #return "404 Page Error! Please choose a link"

if __name__ == '__main__':
    app.run_server()