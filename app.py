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

# not needed for pycharm
# %matplotlib inline

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)
cf.go_offline

# Initialize
# Setup the style from the link:
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Embed the style to the dashabord:

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

PAGE_SIZE = 20

app.layout = html.Div(
    children=[
        html.H1(children="DeFi Kingdom Tavern Dashboards", ),
        html.Div(
            children="Random playground for various tavern dashboards."),

        html.Div(id='last_timestamp',
                 children=[]),

        html.Div(
            children=[
                html.Div(children='Dashboard Selection', style={'fontSize': "14px"}, className='menu-title'),
                dcc.Dropdown(
                    id='dash-selection',
                    options=[
                        {'label': 'Heroes Sold', 'value': 'HeroesSold'},
                        {'label': 'Heroes Hired', 'value': 'HeroesHired'}

                    ],
                    value='HeroesSold',
                    clearable=False,
                    searchable=False,
                    className='dropdown', style={'fontSize': "12px", 'textAlign': 'left'},
                ),
            ],
            className='menu',
            style={'padding': 10, "width": "20%"}
        ),  # the dropdown function

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

        dcc.Store(id='intermediate-value', storage_type='memory'),
        # dcc.Store(id='intermediate-value-h'),

        html.Div(
            children=[
                html.Div(children='Main Class', style={'fontSize': "14px"}, className='menu-title'),
                dcc.Dropdown(
                    id='main-class',
                    options=[
                        {'label': 'Archer', 'value': 'Archer'},
                        {'label': 'DarkKnight', 'value': 'DarkKnight'},
                        {'label': 'Dragoon', 'value': 'Dragoon'},
                        {'label': 'Knight', 'value': 'Knight'},
                        {'label': 'Monk', 'value': 'Monk'},
                        {'label': 'Ninja', 'value': 'Ninja'},
                        {'label': 'Paladin', 'value': 'Paladin'},
                        {'label': 'Pirate', 'value': 'Pirate'},
                        {'label': 'Priest', 'value': 'Priest'},
                        {'label': 'Sage', 'value': 'Sage'},
                        {'label': 'Summoner', 'value': 'Summoner'},
                        {'label': 'Thief', 'value': 'Thief'},
                        {'label': 'Warrior', 'value': 'Warrior'},
                        {'label': 'Wizard', 'value': 'Wizard'},
                    ],
                    clearable=True,
                    searchable=False,
                    className='dropdown', style={'fontSize': "12px", 'textAlign': 'left'},
                ),
            ],
            className='menu',
            style={'padding': 10, "width": "20%"}
        ),  # the dropdown function

        html.Div(
            children=[
                html.Div(children='Profession', style={'fontSize': "14px"}, className='menu-title'),
                dcc.Dropdown(
                    id='prof-filter',
                    options=[
                        {'label': 'Mining', 'value': 'mining'},
                        {'label': 'Gardening', 'value': 'gardening'},
                        {'label': 'Fishing', 'value': 'fishing'},
                        {'label': 'Foraging', 'value': 'foraging'},

                    ],
                    clearable=True,
                    searchable=False,
                    className='dropdown', style={'fontSize': "12px", 'textAlign': 'left'},
                ),
            ],
            className='menu',
            style={'padding': 10, "width": "20%"}
        ),  # the dropdown function

        html.Div(
            children=[
                html.Div(children='Generation', style={'fontSize': "14px"}, className='menu-title'),
                dcc.RangeSlider(
                    id='gen-slider',  # any name you'd like to give it
                    marks={
                        0: '0',  # key=position, value=what you see
                        1: '1',
                        2: '2',
                        3: '3',
                        4: '4',
                        5: '5',
                        6: '6',
                        7: '7',
                        8: '8',
                        9: '9',
                        10: '10',
                        11: '11',
                    },
                    step=1,  # number of steps between values
                    min=0,
                    max=11,
                    value=[0, 11],  # default value initially chosen
                    dots=True,  # True, False - insert dots, only when step>1
                    allowCross=False,  # True,False - Manage handle crossover
                    disabled=False,  # True,False - disable handle

                    className='None',
                    tooltip={'always visible': False,  # show current slider values
                             'placement': 'bottom'},

                ),
            ],
            className='menu',
            style={'padding': 10}
        ),  # the dropdown function

        html.Div(
            children=[
                html.Div(children='Summons Remaning (11 is used for Gen 0 Heroes)', style={'fontSize': "14px"},
                         className='menu-title'),
                dcc.RangeSlider(
                    id='summon-slider',  # any name you'd like to give it
                    marks={
                        0: '0',  # key=position, value=what you see
                        1: '1',
                        2: '2',
                        3: '3',
                        4: '4',
                        5: '5',
                        6: '6',
                        7: '7',
                        8: '8',
                        9: '9',
                        10: '10',
                        11: '11',
                    },
                    step=1,  # number of steps between values
                    min=0,
                    max=11,
                    value=[0, 11],  # default value initially chosen
                    dots=True,  # True, False - insert dots, only when step>1
                    allowCross=False,  # True,False - Manage handle crossover
                    disabled=False,  # True,False - disable handle

                    className='None',
                    tooltip={'always visible': False,  # show current slider values
                             'placement': 'bottom'},

                ),
            ],
            className='menu',
            style={'padding': 10}
        ),  # the dropdown function

        dcc.Loading(id='loading-graph', children=[html.Div(dcc.Graph(id='main-chart'))], type='default'),

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
                                      {"name": 'Max Summons', "id": 'maxSummons'},
                                      {"name": 'Price', "id": 'soldPrice'},
                                      # {"name": 'Timestamp', "id": 'Timestamp'},
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


# put raw data into storage
@app.callback(
    Output("intermediate-value", "data"),
    Input("interval-component", "n_intervals"),
    Input("start-num", "value")
)
def queryHeroes(n, start_num):
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

    query_h = """query getHeroInfos($input: Int){
      assistingAuctions(skip: $input first:1000 orderBy: endedAt orderDirection: desc 
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
    if int(start_num) == 1:
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

    # change 'generation' to string for hover tooltip on main graph
    genstr = []

    for x in df2['generation']:
        x = str(x)
        genstr.append(x)

    df2['generationStr'] = genstr

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

    ####HIRED DATA####
    if int(start_num) == 1:
        data = []
        dataLength = 0

    while int(dataLength) < 2000:
        v = {'input': int(dataLength)}
        r = requests.post(url, json={"query": query_h, 'variables': v})
        json_data = json.loads(r.text)

        df_data = json_data['data']['assistingAuctions']

        newdata = pd.DataFrame(df_data)
        dataLength += 1000
        data.append(newdata)
        # dataLength = len(data)

    df = pd.DataFrame(df_data)

    df2 = df['tokenId'].apply(pd.Series)

    df2 = pd.concat([df2, df['purchasePrice']], axis=1)
    df2 = pd.concat([df2, df['endedAt']], axis=1)

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

    # change 'generation' to string for hover tooltip on main graph
    genstr = []

    for x in df2['generation']:
        x = str(x)
        genstr.append(x)

    df2['generationStr'] = genstr

    utcTime = []

    for x in df['endedAt']:
        x = int(x)
        x = datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')
        utcTime.append(x)
        # print(utcTime)

    df2['timeStamp'] = utcTime
    df2 = df2.drop(['endedAt'], axis=1)

    ###FILTER###

    # base data
    cleaned_df2 = df2.to_dict()

    datasets = {
        'cleaned_df': cleaned_df,
        'cleaned_df2': cleaned_df2
    }

    return json.dumps(datasets)


# update timestamp
@app.callback(
    [Output("last_timestamp", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_timestamp(n):
    currentTime = datetime.datetime.utcnow()
    return ["Data last updated: {}.".format(currentTime)]


@app.callback(
    [Output("main-table", "data")],
    [Input("main-class", "value"),
     Input("prof-filter", "value"),
     Input("gen-slider", "value"),
     Input("summon-slider", "value"),
     Input("interval-component", "n_intervals"),
     Input('intermediate-value', 'data'),
     Input('dash-selection', 'value')]
)
def update_tables(option_selected, prof_filter, gen_slider, summon_slider, n, jsonified_cleaned_data, value):
    # go through each of the dropdowns and initialize a list if any of them are None
    if value == 'HeroesSold':
        datasets = json.loads(jsonified_cleaned_data)
        warrior = pd.DataFrame(datasets['cleaned_df'])

        # make boolean tables from selections
        if option_selected is None:
            option_list = list(set(warrior['mainClass']))
            option_selected = warrior.mainClass.isin(option_list)
        else:
            option_selected = warrior.mainClass.isin([option_selected])

        if prof_filter is None:
            prof_list = list(set(warrior['profession']))
            prof_filter = warrior.profession.isin(prof_list)
        else:
            prof_filter = warrior.profession.isin([prof_filter])

        # zip the booleans together
        xy = [a and b for a, b in zip(option_selected, prof_filter)]

        filtered_df = warrior[xy]
        filtered_df = filtered_df[
            (filtered_df['generation'] >= gen_slider[0]) & (filtered_df['generation'] <= gen_slider[1])
            & (filtered_df['summons'] >= summon_slider[0]) & (filtered_df['summons'] <= summon_slider[1])]
        filtered_df = filtered_df.drop(['generationStr'], axis=1)

        return [filtered_df.to_dict('records')]

    if value == 'HeroesHired':
        datasets = json.loads(jsonified_cleaned_data)
        warrior_h = pd.DataFrame(datasets['cleaned_df2'])

        # make boolean tables from selections
        if option_selected is None:
            option_list = list(set(warrior_h['mainClass']))
            option_selected = warrior_h.mainClass.isin(option_list)
        else:
            option_selected = warrior_h.mainClass.isin([option_selected])

        if prof_filter is None:
            prof_list = list(set(warrior_h['profession']))
            prof_filter = warrior_h.profession.isin(prof_list)
        else:
            prof_filter = warrior_h.profession.isin([prof_filter])

        # zip the booleans together
        xy = [a and b for a, b in zip(option_selected, prof_filter)]

        filtered_df = warrior_h[xy]
        filtered_df = filtered_df[
            (filtered_df['generation'] >= gen_slider[0]) & (filtered_df['generation'] <= gen_slider[1])
            & (filtered_df['summons'] >= summon_slider[0]) & (filtered_df['summons'] <= summon_slider[1])]
        filtered_df = filtered_df.drop(['generationStr'], axis=1)

        return [filtered_df.to_dict('records')]


@app.callback(
    Output("main-chart", "figure"),
    [Input("main-class", "value"),
     Input("prof-filter", "value"),
     Input("gen-slider", "value"),
     Input("summon-slider", "value"),
     Input("interval-component", "n_intervals"),
     Input('intermediate-value', 'data'),
     Input('dash-selection', 'value')]
)
def update_charts(option_selected, prof_filter, gen_slider, summon_slider, n, jsonified_cleaned_data, value):
    if value == 'HeroesSold':
        datasets = json.loads(jsonified_cleaned_data)
        warrior = pd.DataFrame(datasets['cleaned_df'])
        # warrior.to_excel("testdata.xlsx", index=False)

        # make boolean tables from selections
        if option_selected is None:
            option_list = list(set(warrior['mainClass']))
            option_selected = warrior.mainClass.isin(option_list)
        else:
            option_selected = warrior.mainClass.isin([option_selected])

        if prof_filter is None:
            prof_list = list(set(warrior['profession']))
            prof_filter = warrior.profession.isin(prof_list)
        else:
            prof_filter = warrior.profession.isin([prof_filter])

        # zip the booleans together
        xy = [a and b for a, b in zip(option_selected, prof_filter)]

        # working dataset
        filtered_df = warrior[xy]

        filtered_df = filtered_df[
            (filtered_df['generation'] >= gen_slider[0]) & (filtered_df['generation'] <= gen_slider[1])
            & (filtered_df['summons'] >= summon_slider[0]) & (filtered_df['summons'] <= summon_slider[1])]

        filtered_dataC = filtered_df[(filtered_df['rarity'] == 'common')]
        filtered_dataU = filtered_df[(filtered_df['rarity'] == 'uncommon')]
        filtered_dataR = filtered_df[(filtered_df['rarity'] == 'rare')]
        filtered_dataL = filtered_df[(filtered_df['rarity'] == 'legendary')]
        filtered_dataM = filtered_df[(filtered_df['rarity'] == 'mythic')]

        trace1 = go.Scatter(x=filtered_dataC.timeStamp, y=filtered_dataC.soldPrice, mode='markers', name='Common',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataC['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataC['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataC['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataC['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataC['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataC['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataC['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataC['profession'] + '<br>',
                            marker=dict(color='rgba(219, 217, 222, 1)', size=7)

                            )

        trace2 = go.Scatter(x=filtered_dataU.timeStamp, y=filtered_dataU.soldPrice, mode='markers', name='Uncommon',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataU['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataU['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataU['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataU['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataU['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataU['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataU['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataU['profession'] + '<br>',
                            marker=dict(color='rgba(115, 191, 131, 1)', size=7)
                            )

        trace3 = go.Scatter(x=filtered_dataR.timeStamp, y=filtered_dataR.soldPrice, mode='markers', name='Rare',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataR['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataR['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataR['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataR['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataR['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataR['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataR['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataR['profession'] + '<br>',
                            marker=dict(color='rgba(53, 147, 183, 1)', size=7)
                            )

        trace4 = go.Scatter(x=filtered_dataL.timeStamp, y=filtered_dataL.soldPrice, mode='markers', name='Legendary',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataL['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataL['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataL['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataL['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataL['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataL['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataL['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataL['profession'] + '<br>',
                            marker=dict(color='rgba(255, 164, 62, 1)', size=7)
                            )

        trace5 = go.Scatter(x=filtered_dataM.timeStamp, y=filtered_dataM.soldPrice, mode='markers', name='Mythic',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataM['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataM['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataM['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataM['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataM['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataM['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataM['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataM['profession'] + '<br>',
                            marker=dict(color='rgba(178, 109, 216, 1)', size=7)
                            )

        data = [trace1, trace2, trace3, trace4, trace5]
        newfig = go.Figure(data=data)
        newfig.update_traces(marker=dict(line=dict(width=.5)))
        newfig.update_layout(title='Tavern Sales - Last 2000 Heroes Sold',
                             titlefont=dict(family='Arial', size=24),
                             xaxis=dict(showgrid=True, ticks='outside'),
                             xaxis_title='Date in UTC',
                             yaxis_title='Jewel',
                             plot_bgcolor='white'
                             )

        newfig.update_xaxes(showspikes=True)
        newfig.update_yaxes(showspikes=True)

        return newfig

    if value == 'HeroesHired':
        datasets = json.loads(jsonified_cleaned_data)
        warrior_h = pd.DataFrame(datasets['cleaned_df2'])
        # warriors_h.to_excel("testdata2.xlsx", index=False)

        # make boolean tables from selections
        if option_selected is None:
            option_list = list(set(warrior_h['mainClass']))
            option_selected = warrior_h.mainClass.isin(option_list)
        else:
            option_selected = warrior_h.mainClass.isin([option_selected])

        if prof_filter is None:
            prof_list = list(set(warrior_h['profession']))
            prof_filter = warrior_h.profession.isin(prof_list)
        else:
            prof_filter = warrior_h.profession.isin([prof_filter])

        # zip the booleans together
        xy = [a and b for a, b in zip(option_selected, prof_filter)]

        # working dataset
        filtered_df = warrior_h[xy]

        filtered_df = filtered_df[
            (filtered_df['generation'] >= gen_slider[0]) & (filtered_df['generation'] <= gen_slider[1])
            & (filtered_df['summons'] >= summon_slider[0]) & (filtered_df['summons'] <= summon_slider[1])]

        filtered_dataC = filtered_df[(filtered_df['rarity'] == 'common')]
        filtered_dataU = filtered_df[(filtered_df['rarity'] == 'uncommon')]
        filtered_dataR = filtered_df[(filtered_df['rarity'] == 'rare')]
        filtered_dataL = filtered_df[(filtered_df['rarity'] == 'legendary')]
        filtered_dataM = filtered_df[(filtered_df['rarity'] == 'mythic')]

        trace1 = go.Scatter(x=filtered_dataC.timeStamp, y=filtered_dataC.soldPrice, mode='markers', name='Common',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataC['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataC['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataC['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataC['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataC['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataC['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataC['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataC['profession'] + '<br>',
                            marker=dict(color='rgba(219, 217, 222, 1)', size=7)

                            )

        trace2 = go.Scatter(x=filtered_dataU.timeStamp, y=filtered_dataU.soldPrice, mode='markers', name='Uncommon',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataU['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataU['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataU['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataU['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataU['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataU['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataU['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataU['profession'] + '<br>',
                            marker=dict(color='rgba(115, 191, 131, 1)', size=7)
                            )

        trace3 = go.Scatter(x=filtered_dataR.timeStamp, y=filtered_dataR.soldPrice, mode='markers', name='Rare',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataR['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataR['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataR['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataR['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataR['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataR['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataR['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataR['profession'] + '<br>',
                            marker=dict(color='rgba(53, 147, 183, 1)', size=7)
                            )

        trace4 = go.Scatter(x=filtered_dataL.timeStamp, y=filtered_dataL.soldPrice, mode='markers', name='Legendary',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataL['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataL['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataL['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataL['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataL['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataL['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataL['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataL['profession'] + '<br>',
                            marker=dict(color='rgba(255, 164, 62, 1)', size=7)
                            )

        trace5 = go.Scatter(x=filtered_dataM.timeStamp, y=filtered_dataM.soldPrice, mode='markers', name='Mythic',
                            hovertemplate=
                            '<b>ID</b>: %{text}<br>' +
                            '<b>Price</b>: %{y} Jewels' +
                            '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                            text=filtered_dataM['id'] + '<br>' +
                                 '<b>Rarity</b>: ' + filtered_dataM['rarity'] + '<br>' +
                                 '<b>Generation</b>: ' + filtered_dataM['generationStr'] + '<br>' + '<br>' +
                                 '<b>Main Class</b>: ' + filtered_dataM['mainClass'] + '<br>' +
                                 '<b>Sub Class</b>: ' + filtered_dataM['subClass'] + '<br>' +
                                 '<b>Primary Boost</b>: ' + filtered_dataM['statBoost1'] + '<br>' +
                                 '<b>Secondary Boost</b>: ' + filtered_dataM['statBoost2'] + '<br>' +
                                 '<b>Profession</b>: ' + filtered_dataM['profession'] + '<br>',
                            marker=dict(color='rgba(178, 109, 216, 1)', size=7)
                            )

        data = [trace1, trace2, trace3, trace4, trace5]
        newfig = go.Figure(data=data)
        newfig.update_traces(marker=dict(line=dict(width=.5)))
        newfig.update_layout(title='Tavern Sales - Last 2000 Heroes Sold',
                             titlefont=dict(family='Arial', size=24),
                             xaxis=dict(showgrid=True, ticks='outside'),
                             xaxis_title='Date in UTC',
                             yaxis_title='Jewel',
                             plot_bgcolor='white'
                             )

        newfig.update_xaxes(showspikes=True)
        newfig.update_yaxes(showspikes=True)

        return newfig


if __name__ == "__main__":
    app.run_server()