from failedapp import app
import time
import datetime
import requests
import json
import pandas as pd

import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import seaborn as sns

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)
cf.go_offline

PAGE_SIZE = 20

layout = html.Div([
    html.Div(
    children=[
        html.H1(children="DeFi Kingdom Tavern Dashboards", ),
        html.Div(
            children="Random playground for various tavern dashboards."),

        html.Div(id='last_timestamp',
                 children=[]),

        dcc.Interval(
            id='interval-component',
            interval=60 * 60 * 1000,
            n_intervals=0),

        html.Div([
            # Create element to hide/show, in this case an 'Input Component'
            dcc.Input(
                id='start-num',
                value='1',
            )
        ], style={'display': 'none'}  # <-- This is the line that will be changed by the dropdown callback
        ),

        html.Div([
            # Create element to hide/show, in this case an 'Input Component'
            dcc.Input(
                id='hero-num',
                type="number",
                min=1,
                debounce=True,
            )
        ],
            style={'padding': 10, "width": "20%"}
        ),

        dcc.Store(id='intermediate-value', storage_type='session'),
        dcc.Store(id='hero-data', storage_type='session'),

        dash_table.DataTable(id='main-table',
                             columns=[{"name": 'ID', "id": 'id'},
                                      {"name": 'Rarity', "id": 'rarity'},
                                      {"name": 'Generation', "id": 'generation'},
                                      {"name": 'Main Class', "id": 'mainClass'},
                                      {"name": 'Sub Class', "id": 'subClass'},
                                      {"name": 'Primary Boost', "id": 'statBoost1'},
                                      {"name": 'Secondary Boost', "id": 'statBoost2'},
                                      {"name": 'Profession Boost', "id": 'profession'},
                                      {"name": 'Summons Remaining', "id": 'summons'},
                                      {"name": 'Max Summons', "id": 'maxSummons'}],
                             data=[],
                             page_current=0,
                             page_size=PAGE_SIZE,
                             style_as_list_view=True,
                             style_cell={'padding': '5px', 'textAlign': 'left'},
                             style_header={
                                 'backgroundColor': 'white',
                                 'fontWeight': 'bold'
                             },
                             ),

        html.Div(
            children=[
                html.Div(children='Tavern Filters', style={'fontSize': "14px"}, className='menu-title'),
                dcc.Dropdown(
                    id='tavern-filter',
                    options=[
                        {"label": 'Rarity', "value": 'rarity'},
                        {"label": 'Generation', "value": 'generation'},
                        {"label": 'Main Class', "value": 'mainClass'},
                        {"label": 'Sub Class', "value": 'subClass'},
                        {"label": 'Primary Boost', "value": 'statBoost1'},
                        {"label": 'Secondary Boost', "value": 'statBoost2'},
                        {"label": 'Profession Boost', "value": 'profession'},
                        {"label": 'Summons Remaining', "value": 'summons'},
                        {"label": 'Max Summons', "value": 'maxSummons'}],
                    multi=True,
                    clearable=False,
                    searchable=False,
                    className='dropdown', style={'fontSize': "12px", 'textAlign': 'left'},
                ),
            ],
            className='menu',
            style={'padding': 10, "width": "33%"}
        ),  # the dropdown function

        dash_table.DataTable(id='tavern-table',
                             columns=[{"name": 'ID', "id": 'id'},
                                      {"name": 'Rarity', "id": 'rarity'},
                                      {"name": 'Generation', "id": 'generation'},
                                      {"name": 'Main Class', "id": 'mainClass'},
                                      {"name": 'Sub Class', "id": 'subClass'},
                                      {"name": 'Primary Boost', "id": 'statBoost1'},
                                      {"name": 'Secondary Boost', "id": 'statBoost2'},
                                      {"name": 'Profession Boost', "id": 'profession'},
                                      {"name": 'Summons Remaining', "id": 'summons'},
                                      {"name": 'Max Summons', "id": 'maxSummons'},
                                      {"name": 'Price', "id": 'soldPrice'},
                                      {"name": 'Timestamp', "id": 'timeStamp'}],
                             data=[],
                             page_current=0,
                             page_size=PAGE_SIZE,
                             style_as_list_view=True,
                             style_cell={'padding': '5px', 'textAlign': 'left'},
                             style_header={
                                 'backgroundColor': 'white',
                                 'fontWeight': 'bold'
                             },
                             ),

        ####BOTTOM TEXT####
        html.Div(children="Tip jar: 0x71C52444b34fb9d99b3F3E0bD29084ba0EEe0436",
                 style={'fontSize': "12px", 'padding': 10}),

    ]
    )
]
)


# update timestamp
@app.callback(
    [Output("last_timestamp", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_timestamp(n):
    currentTime = datetime.datetime.utcnow()
    return ["Data last updated: {}.".format(currentTime)]


@app.callback(
    Output("main-table", "data"),
    Input("hero-num", "value"),
    Input("hero-data", "data")
)
def queryHeroes(hero_num, hero_data):
    if hero_num is None:
        pass
    else:
        datasets = json.loads(hero_data)
        df = pd.DataFrame(datasets)

        hero_table = df.to_dict('records')
        return hero_table


@app.callback(
    Output("tavern-table", "data"),
    Input("intermediate-value", "data"),
    Input("hero-data", "data"),
    Input("tavern-filter", "value"),
)
def getTaverntable(sales_data, hero_data, tavern_filter):
    if tavern_filter is None:
        pass
    else:
        sales_df = json.loads(sales_data)
        sales_df = pd.DataFrame(sales_df)

        hero_df = json.loads(hero_data)
        hero_df = pd.DataFrame(hero_df)

        for x in tavern_filter:
            f_value = hero_df[x][0]
            sales_df = sales_df[(sales_df[x] == f_value)]

        return sales_df.to_dict('records')


@app.callback(
    Output("hero-data", "data"),
    Input("hero-num", "value")
)
def queryHeroesdata(hero_num):
    if hero_num is None:
        pass
    else:
        ###QUERY AND URL####
        query = """query getHeroInfos($input: Int) {
          hero(
            id:$input

      )

      {
              id
              rarity
              generation
              mainClass
              subClass
              statBoost1
              statBoost2
              profession
              summons
              maxSummons
      }
    }
        """

        url = "http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/apiv5"
        v = {'input': int(hero_num)}
        r = requests.post(url, json={"query": query, 'variables': v})

        json_data = json.loads(r.text)
        df_data = json_data['data']
        df = pd.DataFrame(df_data).transpose()

        cols = ['id', 'rarity', 'generation', 'mainClass', 'subClass', 'statBoost1', 'statBoost2', 'profession',
                'summons',
                'maxSummons']

        df['rarity'] = df['rarity'].replace([0, 1, 2, 3, 4], ['common', 'uncommon', 'rare', 'legendary', 'mythic'])

        # reverse summons so it shows summons remaining instead of used
        df['summons'] = df.apply(lambda x: 11 if x['generation'] == 0 else x['maxSummons'] - x['summons'], axis=1)

        hero_df = df.reset_index(drop=True).reindex(columns=cols).to_dict()

        return json.dumps(hero_df)


@app.callback(
    Output("intermediate-value", "data"),
    Input("interval-component", "n_intervals"),
    Input("start-num", "value")
)
def queryData(n, start_num):
    ###QUERY AND URL####
    query = """query getHeroInfos($input: Int){
      saleAuctions(skip: $input first:1000 orderBy: endedAt orderDirection: desc 
            where: {
            open: false
            purchasePrice_not: null
          }


            ) {
        id
        tokenId {
          id
          rarity
          generation
          mainClass
          subClass
          statBoost1
          statBoost2
          profession
          summons
          maxSummons
        }
        endedAt
        purchasePrice
      }
    }
    """

    url = "http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/apiv5"

    ####SOLD DATA####
    # if int(start_num) == 1:
    data = []
    dataLength = 0

    while int(dataLength) < 2000:
        v = {'input': int(dataLength)}
        r = requests.post(url, json={"query": query, 'variables': v})
        json_data = json.loads(r.text)

        df_data = json_data['data']['saleAuctions']

        newdata = pd.DataFrame(df_data)
        dataLength += 1000
        data.append(newdata)
        # dataLength = len(data)

    df = pd.concat(data).reset_index(drop=True)
    df2 = df['tokenId'].apply(pd.Series)

    df2 = pd.concat([df2, df['purchasePrice']], axis=1)
    df2 = pd.concat([df2, df['endedAt']], axis=1)

    cols = ['id', 'rarity', 'generation', 'mainClass', 'subClass', 'statBoost1', 'statBoost2', 'profession', 'summons',
            'maxSummons', 'purchasePrice', 'endedAt']

    df2 = df2.reindex(columns=cols)

    df2['rarity'] = df2['rarity'].replace([0, 1, 2, 3, 4], ['common', 'uncommon', 'rare', 'legendary', 'mythic'])

    # drop empty values from purchasePrice
    df2.dropna(subset=['purchasePrice'])

    # reverse summons so it shows summons remaining instead of used
    df2['summons'] = df2.apply(lambda x: 11 if x['generation'] == 0 else x['maxSummons'] - x['summons'], axis=1)

    soldPrice = []

    for x in df['purchasePrice']:
        for y in x:
            priceLen = len(x) - 16
        x = x[: priceLen]
        x = int(float(x)) / 100
        soldPrice.append(x)

    df2['soldPrice'] = soldPrice
    df2 = df2.drop(['purchasePrice'], axis=1)

    utcTime = []

    for x in df['endedAt']:
        x = int(x)
        x = datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')
        utcTime.append(x)
        # print(utcTime)

    df2['timeStamp'] = utcTime
    df2 = df2.drop(['endedAt'], axis=1)

    # base data
    cleaned_df = df2.to_dict()

    return json.dumps(cleaned_df)
