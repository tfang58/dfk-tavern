from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import tavern, herocheck

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Tavern Data |', href='/taverndata'),
        dcc.Link(' Hero Price Check', href='/heroprice'),
    ], className="row"),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/taverndata':
        return tavern.layout
    if pathname == '/heroprice':
        return herocheck.layout
    else:
        return tavern.layout


if __name__ == '__main__':
    app.run_server(debug=True)