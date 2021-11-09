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

query = """query {
  saleAuctions(first:1000 orderBy: endedAt orderDirection: desc 
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

query_h = """query {
  assistingAuctions(first:1000 orderBy: endedAt orderDirection: desc 
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

url = "https://graph.defikingdoms.com/subgraphs/name/defikingdoms/apiv5"
r = requests.post(url, json={"query": query})
r_h = requests.post(url, json={"query": query_h})

# if r.status_code == 200:
#     print(json.dumps(r.json(), indent=2))
# else:
#     raise Exception(f"Query failed to run with a {r.status_code}.")

# if r_h.status_code == 200:
#     print(json.dumps(r_h.json(), indent=2))
# else:
#     raise Exception(f"Query failed to run with a {r_h.status_code}.")

json_data = json.loads(r.text)
json_data_h = json.loads(r_h.text)

# getting timestamp for "last updated"
# currentTime = datetime.datetime.utcnow()
# currentTime = ''

# df_data = json_data['data']['saleAuctions']
# df = pd.DataFrame(df_data)

# df_h_data = json_data_h['data']['assistingAuctions']
# df_h = pd.DataFrame(df_h_data)

# df['tokenId'].apply(pd.Series)
# df_h['tokenId'].apply(pd.Series)

# df2 = df['tokenId'].apply(pd.Series)
# df2_h = df['tokenId'].apply(pd.Series)

# df2 = pd.concat([df2, df['purchasePrice']], axis=1)
# df2 = pd.concat([df2, df['endedAt']], axis=1)
# df2_h = pd.concat([df2_h, df_h['purchasePrice']], axis=1)
# df2_h = pd.concat([df2_h, df_h['endedAt']], axis=1)

# cols = ['id', 'rarity', 'generation', 'mainClass', 'subClass', 'statBoost1', 'statBoost2', 'profession', 'summons',
#         'maxSummons', 'purchasePrice', 'endedAt']
# cols_h = ['id', 'rarity', 'generation', 'mainClass', 'subClass', 'statBoost1', 'statBoost2', 'profession', 'summons', 'maxSummons', 'purchasePrice', 'endedAt']

# df2 = df2.reindex(columns=cols)
# df2_h = df2_h.reindex(columns=cols_h)

# df2['rarity'] = df2['rarity'].replace([0, 1, 2, 3, 4], ['common', 'uncommon', 'rare', 'legendary', 'mythic'])
# df2_h['rarity'] = df2_h['rarity'].replace([0, 1, 2, 3, 4], ['common', 'uncommon', 'rare', 'legendary', 'mythic'])

# drop empty values from purchasePrice
# df2.dropna(subset=['purchasePrice'])
# df2_h.dropna(subset=['purchasePrice'])

# sold to purchase
soldPrice = []

# for x in df['purchasePrice']:
#     for y in x:
#         priceLen = len(x) - 16
#     x = x[: priceLen]
#     x = int(float(x)) / 100
#     soldPrice.append(x)

# df2['soldPrice'] = soldPrice
# df2 = df2.drop(['purchasePrice'], axis=1)


# change 'generation' to string for hover tooltip on main graph
# sold generation to str
# genstr = []

# for x in df2['generation']:
#     x = str(x)
#     genstr.append(x)

# df2['generationStr'] = genstr

# change 'timestamp' to utc time for hover tooltip on main graph
# utcTime = []

# for x in df['endedAt']:
#     x = int(x)
#     x = datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')
#     utcTime.append(x)
#     # print(utcTime)

# df2['timeStamp'] = utcTime
# df2 = df2.drop(['endedAt'], axis=1)

###FILTER####

# sold base data
# warrior = df2

# table data - drop 'generationStr' for readability
# knight = df2

# filtered_df = knight

# ###SOLD MAIN GRAPH####
# newfig = go.Figure()

# # px.scatter(warriorC, x="timeStamp", y="soldPrice",
# #                 hover_name="id", hover_data={'rarity'})])

# newfig.add_trace(go.Scatter(x=warriorC.timeStamp, y=warriorC.soldPrice, mode='markers', name='Common',
#                          hovertemplate=
#                          '<b>ID</b>: %{text}<br>' +
#                          '<b>Price</b>: %{y} Jewels' +
#                          '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
#                          text=warriorC['id'] + '<br>' +
#                               '<b>Rarity</b>: ' + warriorC['rarity'] + '<br>' +
#                               '<b>Generation</b>: ' + warriorC['generationStr'] + '<br>' + '<br>' +
#                               '<b>Main Class</b>: ' + warriorC['mainClass'] + '<br>' +
#                               '<b>Sub Class</b>: ' + warriorC['subClass'] + '<br>' +
#                               '<b>Primary Boost</b>: ' + warriorC['statBoost1'] + '<br>' +
#                               '<b>Secondary Boost</b>: ' + warriorC['statBoost2'] + '<br>' +
#                               '<b>Profession</b>: ' + warriorC['profession'] + '<br>',
#                          marker=dict(color='rgba(219, 217, 222, 1)', size=7)

#                          ))

# newfig.add_trace(go.Scatter(x=warriorU.timeStamp, y=warriorU.soldPrice, mode='markers', name='Uncommon',
#                          hovertemplate=
#                          '<b>ID</b>: %{text}<br>' +
#                          '<b>Price</b>: %{y} Jewels' +
#                          '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
#                          text=warriorU['id'] + '<br>' +
#                               '<b>Rarity</b>: ' + warriorU['rarity'] + '<br>' +
#                               '<b>Generation</b>: ' + warriorU['generationStr'] + '<br>' + '<br>' +
#                               '<b>Main Class</b>: ' + warriorU['mainClass'] + '<br>' +
#                               '<b>Sub Class</b>: ' + warriorU['subClass'] + '<br>' +
#                               '<b>Primary Boost</b>: ' + warriorU['statBoost1'] + '<br>' +
#                               '<b>Secondary Boost</b>: ' + warriorU['statBoost2'] + '<br>' +
#                               '<b>Profession</b>: ' + warriorU['profession'] + '<br>',
#                          marker=dict(color='rgba(115, 191, 131, 1)', size=7)
#                          ))

# newfig.add_trace(go.Scatter(x=warriorR.timeStamp, y=warriorR.soldPrice, mode='markers', name='Rare',
#                          hovertemplate=
#                          '<b>ID</b>: %{text}<br>' +
#                          '<b>Price</b>: %{y} Jewels' +
#                          '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
#                          text=warriorR['id'] + '<br>' +
#                               '<b>Rarity</b>: ' + warriorR['rarity'] + '<br>' +
#                               '<b>Generation</b>: ' + warriorR['generationStr'] + '<br>' + '<br>' +
#                               '<b>Main Class</b>: ' + warriorR['mainClass'] + '<br>' +
#                               '<b>Sub Class</b>: ' + warriorR['subClass'] + '<br>' +
#                               '<b>Primary Boost</b>: ' + warriorR['statBoost1'] + '<br>' +
#                               '<b>Secondary Boost</b>: ' + warriorR['statBoost2'] + '<br>' +
#                               '<b>Profession</b>: ' + warriorR['profession'] + '<br>',
#                          marker=dict(color='rgba(53, 147, 183, 1)', size=7)
#                          ))

# newfig.add_trace(go.Scatter(x=warriorL.timeStamp, y=warriorL.soldPrice, mode='markers', name='Legendary',
#                          hovertemplate=
#                          '<b>ID</b>: %{text}<br>' +
#                          '<b>Price</b>: %{y} Jewels' +
#                          '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
#                          text=warriorL['id'] + '<br>' +
#                               '<b>Rarity</b>: ' + warriorL['rarity'] + '<br>' +
#                               '<b>Generation</b>: ' + warriorL['generationStr'] + '<br>' + '<br>' +
#                               '<b>Main Class</b>: ' + warriorL['mainClass'] + '<br>' +
#                               '<b>Sub Class</b>: ' + warriorL['subClass'] + '<br>' +
#                               '<b>Primary Boost</b>: ' + warriorL['statBoost1'] + '<br>' +
#                               '<b>Secondary Boost</b>: ' + warriorL['statBoost2'] + '<br>' +
#                               '<b>Profession</b>: ' + warriorL['profession'] + '<br>',
#                          marker=dict(color='rgba(255, 164, 62, 1)', size=7)
#                          ))

# newfig.add_trace(go.Scatter(x=warriorM.timeStamp, y=warriorM.soldPrice, mode='markers', name='Mythic',
#                          hovertemplate=
#                          '<b>ID</b>: %{text}<br>' +
#                          '<b>Price</b>: %{y} Jewels' +
#                          '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
#                          text=warriorM['id'] + '<br>' +
#                               '<b>Rarity</b>: ' + warriorM['rarity'] + '<br>' +
#                               '<b>Generation</b>: ' + warriorM['generationStr'] + '<br>' + '<br>' +
#                               '<b>Main Class</b>: ' + warriorM['mainClass'] + '<br>' +
#                               '<b>Sub Class</b>: ' + warriorM['subClass'] + '<br>' +
#                               '<b>Primary Boost</b>: ' + warriorM['statBoost1'] + '<br>' +
#                               '<b>Secondary Boost</b>: ' + warriorM['statBoost2'] + '<br>' +
#                               '<b>Profession</b>: ' + warriorM['profession'] + '<br>',
#                          marker=dict(color='rgba(178, 109, 216, 1)', size=7)
#                          ))

# newfig.update_traces(marker=dict(line=dict(width=.5)))
# newfig.update_layout(title='Tavern Sales - Last 1000 Heroes Sold',
#                   titlefont=dict(family='Arial', size=24),
#                   xaxis=dict(showgrid=True, ticks='outside'),
#                   xaxis_title='Date in UTC',
#                   yaxis_title='Jewel',
#                   plot_bgcolor='white'
#                   )

# newfig.update_xaxes(showspikes=True)
# newfig.update_yaxes(showspikes=True)

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
            children="Dashboard updates in ~5 minute intervals."),

        html.Div(id='last_timestamp',
                 children=[]),

        html.Div(
            children=[
                html.Div(children='Dashboard Selection', style={'fontSize': "16px", 'width': '50%'},
                         className='menu-title'),
                dcc.Dropdown(
                    id='dash-selection',
                    options=[
                        {'label': 'Heroes Sold', 'value': 'HeroesSold'},
                        {'label': 'Heroes Hired', 'value': 'HeroesHired'}

                    ],
                    value='HeroesSold',
                    clearable=False,
                    searchable=False,
                    className='dropdown', style={'fontSize': "14px", 'textAlign': 'center'},
                ),
            ],
            className='menu',
        ),  # the dropdown function

        dcc.Interval(
            id='interval-component',
            interval= 5 * 60 * 1000,
            n_intervals=0),

        dcc.Store(id='intermediate-value', data=[], storage_type='memory'),
        # dcc.Store(id='intermediate-value-h'),

        ####SOLD SECTION####
        html.Div(
            children=[
                html.Div(children='Main Class', style={'fontSize': "16px", 'width': '50%'}, className='menu-title'),
                dcc.Dropdown(
                    id='main-class',
                    options=[
                        {'label': 'Archer', 'value': 'Archer'},
                        {'label': 'Darkknight', 'value': 'Darkknight'},
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

                    #                         {'label': MainClass, 'value': MainClass}
                    #                         for MainClass in warrior.mainClass.sort_values().unique()
                    #                     ],  # 'warrior' is the filter
                    clearable=True,
                    searchable=False,
                    className='dropdown', style={'fontSize': "14px", 'textAlign': 'center'},
                ),
            ],
            className='menu',
        ),  # the dropdown function

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
            # pushable=1,            # any number, or True with multiple handles
            # updatemode='drag',  # 'mouseup', 'drag' - update value method
            # included=True,         # True, False - highlight handle
            # vertical=False,        # True, False - vertical, horizontal slider
            # verticalHeight=900,    # hight of slider (pixels) when vertical=True
            className='None',
            tooltip={'always visible': False,  # show current slider values
                     'placement': 'bottom'},
        ),

        dcc.Graph(id='main-chart', figure={}),

        dash_table.DataTable(id='main-table',
                             columns=[{"name": 'ID', "id": 'id'},
                                      {"name": 'Rarity', "id": 'rarity'},
                                      {"name": 'Generation', "id": 'generation'},
                                      {"name": 'Main Class', "id": 'mainClass'},
                                      {"name": 'Sub Class', "id": 'subClass'},
                                      {"name": 'Primary Boost', "id": 'statBoost1'},
                                      {"name": 'Secondary Boost', "id": 'statBoost2'},
                                      {"name": 'Profession Boost', "id": 'profession'},
                                      {"name": 'Summons Used', "id": 'summons'},
                                      {"name": 'Max Summons', "id": 'maxSummons'},
                                      {"name": 'Price', "id": 'soldPrice'},
                                      # {"name": 'Timestamp', "id": 'Timestamp'},
                                      {"name": 'Timestamp', "id": 'timeStamp'}],
                             data=[],
                             # data=knight.to_dict('records'),
                             page_current=0,
                             page_size=PAGE_SIZE),

        ####BOTTOM TEXT####
        html.Div(children="Tip jar: 0x71C52444b34fb9d99b3F3E0bD29084ba0EEe0436"),

        html.Div(children="Tips are appreciated :D"),
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


# put clean data in storage
@app.callback(
    Output('intermediate-value', 'data'),
    Input("interval-component", "n_intervals")
)
def clean_data(n):
    # update dataframe
    r = requests.post(url, json={"query": query})
    json_data = json.loads(r.text)

    df_data = json_data['data']['saleAuctions']
    df = pd.DataFrame(df_data)

    df2 = df['tokenId'].apply(pd.Series)

    df2 = pd.concat([df2, df['purchasePrice']], axis=1)
    df2 = pd.concat([df2, df['endedAt']], axis=1)

    cols = ['id', 'rarity', 'generation', 'mainClass', 'subClass', 'statBoost1', 'statBoost2', 'profession', 'summons',
            'maxSummons', 'purchasePrice', 'endedAt']

    df2 = df2.reindex(columns=cols)

    df2['rarity'] = df2['rarity'].replace([0, 1, 2, 3, 4], ['common', 'uncommon', 'rare', 'legendary', 'mythic'])

    # drop empty values from purchasePrice
    df2.dropna(subset=['purchasePrice'])

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

    ###FILTER####

    # base data
    cleaned_df = df2.to_dict()

    # update dataframe
    r = requests.post(url, json={"query": query_h})
    json_data = json.loads(r.text)

    df_data = json_data['data']['assistingAuctions']
    df = pd.DataFrame(df_data)

    df2 = df['tokenId'].apply(pd.Series)

    df2 = pd.concat([df2, df['purchasePrice']], axis=1)
    df2 = pd.concat([df2, df['endedAt']], axis=1)

    df2 = df2.reindex(columns=cols)

    df2['rarity'] = df2['rarity'].replace([0, 1, 2, 3, 4], ['common', 'uncommon', 'rare', 'legendary', 'mythic'])

    # drop empty values from purchasePrice
    df2.dropna(subset=['purchasePrice'])

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

    ###FILTER####

    # base data
    cleaned_df2 = df2.to_dict()

    datasets = {
        'cleaned_df': cleaned_df,
        'cleaned_df2': cleaned_df2
    }

    return json.dumps(datasets)


@app.callback(
    [Output("main-table", "data")],
    [Input("main-class", "value"),
     Input("gen-slider", "value"),
     Input("interval-component", "n_intervals"),
     Input('intermediate-value', 'data'),
     Input('dash-selection', 'value')]
)
def update_tables(option_selected, gen_slider, n, jsonified_cleaned_data, value):
    if value == 'HeroesSold':
        datasets = json.loads(jsonified_cleaned_data)
        warrior = pd.DataFrame(datasets['cleaned_df'])

        if option_selected is None:
            filtered_df = warrior[(warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_df = filtered_df.drop(['generationStr'], axis=1)
        else:
            filtered_df = warrior[(warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_df = filtered_df[filtered_df['mainClass'] == option_selected]
            filtered_df = filtered_df.drop(['generationStr'], axis=1)
        return [filtered_df.to_dict('records')]

    if value == 'HeroesHired':
        datasets = json.loads(jsonified_cleaned_data)
        warrior_h = pd.DataFrame(datasets['cleaned_df2'])

        if option_selected is None:
            filtered_df = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_df = filtered_df.drop(['generationStr'], axis=1)
        else:
            filtered_df = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_df = filtered_df[filtered_df['mainClass'] == option_selected]
            filtered_df = filtered_df.drop(['generationStr'], axis=1)
        # return filtered_df.to_excel("testdata.xlsx", index=False)
        return [filtered_df.to_dict('records')]


@app.callback(
    Output("main-chart", "figure"),
    [Input("main-class", "value"),
     Input("gen-slider", "value"),
     Input("interval-component", "n_intervals"),
     Input('intermediate-value', 'data'),
     Input('dash-selection', 'value')]
)
def update_charts(option_selected, gen_slider, n, jsonified_cleaned_data, value):
    if value == 'HeroesSold':
        datasets = json.loads(jsonified_cleaned_data)
        warrior = pd.DataFrame(datasets['cleaned_df'])
        # warrior.to_excel("testdata.xlsx", index=False)

        if option_selected is None:
            filtered_dataC = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_dataU = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_dataR = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_dataL = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_dataM = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]

            filtered_dataC = filtered_dataC[(filtered_dataC['rarity'] == 'common')]
            filtered_dataU = filtered_dataU[(filtered_dataU['rarity'] == 'uncommon')]
            filtered_dataR = filtered_dataR[(filtered_dataR['rarity'] == 'rare')]
            filtered_dataL = filtered_dataL[(filtered_dataL['rarity'] == 'legendary')]
            filtered_dataM = filtered_dataM[(filtered_dataM['rarity'] == 'mythic')]

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

            trace4 = go.Scatter(x=filtered_dataL.timeStamp, y=filtered_dataL.soldPrice, mode='markers',
                                name='Legendary',
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
            newfig.update_layout(title='Tavern Sales - Last 1000 Heroes Sold',
                                 titlefont=dict(family='Arial', size=24),
                                 xaxis=dict(showgrid=True, ticks='outside'),
                                 xaxis_title='Date in UTC',
                                 yaxis_title='Jewel',
                                 plot_bgcolor='white'
                                 )

            newfig.update_xaxes(showspikes=True)
            newfig.update_yaxes(showspikes=True)

            return newfig

        else:
            filtered_dataC = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_dataU = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_dataR = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_dataL = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]
            filtered_dataM = warrior[
                (warrior['generation'] >= gen_slider[0]) & (warrior['generation'] <= gen_slider[1])]

            filtered_dataC = filtered_dataC[
                (filtered_dataC['mainClass'] == option_selected) & (warrior["rarity"] == 'common')]
            filtered_dataU = filtered_dataU[
                (filtered_dataU['mainClass'] == option_selected) & (warrior["rarity"] == 'uncommon')]
            filtered_dataR = filtered_dataR[
                (filtered_dataR['mainClass'] == option_selected) & (warrior["rarity"] == 'rare')]
            filtered_dataL = filtered_dataL[
                (filtered_dataL['mainClass'] == option_selected) & (warrior["rarity"] == 'legendary')]
            filtered_dataM = filtered_dataM[
                (filtered_dataM['mainClass'] == option_selected) & (warrior["rarity"] == 'mythic')]

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

            trace4 = go.Scatter(x=filtered_dataL.timeStamp, y=filtered_dataL.soldPrice, mode='markers',
                                name='Legendary',
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
            newfig.update_layout(title='Tavern Sales - Last 1000 Heroes Sold',
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

        if option_selected is None:
            filtered_dataC = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_dataU = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_dataR = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_dataL = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_dataM = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]

            filtered_dataC = filtered_dataC[(filtered_dataC['rarity'] == 'common')]
            filtered_dataU = filtered_dataU[(filtered_dataU['rarity'] == 'uncommon')]
            filtered_dataR = filtered_dataR[(filtered_dataR['rarity'] == 'rare')]
            filtered_dataL = filtered_dataL[(filtered_dataL['rarity'] == 'legendary')]
            filtered_dataM = filtered_dataM[(filtered_dataM['rarity'] == 'mythic')]

            trace1 = go.Scatter(x=filtered_dataC.timeStamp, y=filtered_dataC.soldPrice, mode='markers', name='Common',
                                hovertemplate=
                                '<b>ID</b>: %{text}<br>' +
                                '<b>Price</b>: %{y} Jewels' +
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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

            trace4 = go.Scatter(x=filtered_dataL.timeStamp, y=filtered_dataL.soldPrice, mode='markers',
                                name='Legendary',
                                hovertemplate=
                                '<b>ID</b>: %{text}<br>' +
                                '<b>Price</b>: %{y} Jewels' +
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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
            newfig.update_layout(title='Tavern Sales - Last 1000 Heroes Hired',
                                 titlefont=dict(family='Arial', size=24),
                                 xaxis=dict(showgrid=True, ticks='outside'),
                                 xaxis_title='Date in UTC',
                                 yaxis_title='Jewel',
                                 plot_bgcolor='white'
                                 )

            newfig.update_xaxes(showspikes=True)
            newfig.update_yaxes(showspikes=True)

            # warrior_h.to_excel("testdata2.xlsx", index=False)

            return newfig

        else:
            filtered_dataC = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_dataU = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_dataR = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_dataL = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]
            filtered_dataM = warrior_h[
                (warrior_h['generation'] >= gen_slider[0]) & (warrior_h['generation'] <= gen_slider[1])]

            filtered_dataC = filtered_dataC[
                (filtered_dataC['mainClass'] == option_selected) & (warrior["rarity"] == 'common')]
            filtered_dataU = filtered_dataU[
                (filtered_dataU['mainClass'] == option_selected) & (warrior["rarity"] == 'uncommon')]
            filtered_dataR = filtered_dataR[
                (filtered_dataR['mainClass'] == option_selected) & (warrior["rarity"] == 'rare')]
            filtered_dataL = filtered_dataL[
                (filtered_dataL['mainClass'] == option_selected) & (warrior["rarity"] == 'legendary')]
            filtered_dataM = filtered_dataM[
                (filtered_dataM['mainClass'] == option_selected) & (warrior["rarity"] == 'mythic')]

            trace1 = go.Scatter(x=filtered_dataC.timeStamp, y=filtered_dataC.soldPrice, mode='markers', name='Common',
                                hovertemplate=
                                '<b>ID</b>: %{text}<br>' +
                                '<b>Price</b>: %{y} Jewels' +
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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

            trace4 = go.Scatter(x=filtered_dataL.timeStamp, y=filtered_dataL.soldPrice, mode='markers',
                                name='Legendary',
                                hovertemplate=
                                '<b>ID</b>: %{text}<br>' +
                                '<b>Price</b>: %{y} Jewels' +
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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
                                '<br><b>Hired At</b>: %{x} UTC<br><extra></extra>',
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
            newfig.update_layout(title='Tavern Sales - Last 1000 Heroes Hired',
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