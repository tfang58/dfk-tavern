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

#not needed for pycharm
#%matplotlib inline

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline

# query = """query {
#    saleAuction(id: 2328) {
#    id
#    endedAt
#    endingPrice
#    }
# }"""

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

url = "https://graph.defikingdoms.com/subgraphs/name/defikingdoms/apiv5"
r = requests.post(url, json={"query": query})

if r.status_code == 200:
    print(json.dumps(r.json(), indent=2))
else:
    raise Exception(f"Query failed to run with a {r.status_code}.")

json_data = json.loads(r.text)

#getting timestamp for "last updated"
currentTime = datetime.datetime.utcnow()

df_data = json_data['data']['saleAuctions']
df = pd.DataFrame(df_data)

df['tokenId'].apply(pd.Series)

df2 = df['tokenId'].apply(pd.Series)

df2 = pd.concat([df2, df['purchasePrice']], axis=1)
df2 = pd.concat([df2, df['endedAt']], axis=1)

cols = ['id', 'rarity', 'generation', 'mainClass', 'subClass', 'statBoost1', 'statBoost2', 'profession', 'summons', 'maxSummons', 'purchasePrice', 'endedAt']

df2 = df2.reindex(columns=cols)

df2['rarity'] = df2['rarity'].replace([0, 1, 2, 3, 4], ['common', 'uncommon', 'rare', 'legendary', 'mythic'])
#print(df2)

#drop empty values from purchasePrice
df2.dropna(subset=['purchasePrice'])

soldPrice = []

for x in df['purchasePrice']:
    for y in x:
        priceLen = len(x)-16
    x = x[: priceLen]
    x = int(float(x))/100
    soldPrice.append(x)

df2['soldPrice'] = soldPrice
df2 = df2.drop(['purchasePrice'], axis=1)

genstr = []

for x in df2['generation']:
 x = str(x)
 genstr.append(x)

df2['generation'] = genstr

utcTime = []

for x in df['endedAt']:
 x = int(x)
 x = datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')
 utcTime.append(x)
 # print(utcTime)

df2['timeStamp'] = utcTime
# df2 = df2.drop(['endedAt'], axis=1)

###FILTER####

#df2[(df2['generation']==1) & (df2['rarity']=='uncommon')]
#df[(df["a"] > 2) & (df["b"] > 5)]

# gen0 = df2[(df2['generation']==0)]
# gen1 = df2[(df2['generation']==1)]
# gen2 = df2[(df2['generation']==2)]
# gen3 = df2[(df2['generation']==3)]
# gen4 = df2[(df2['generation']==4)]
# genbeyond = df2[(df2['generation']>4)]

#warrior = df2[(df2['mainClass']=='Warrior') & (df2["generation"]=='1')]
#knight = df2[(df2['mainClass']=='Knight') & (df2["generation"]=='1')]

#fishing = df2[(df2['profession']=='fishing') & (df2["generation"]=='1')]

# warrior = df2[(df2['mainClass']=='Warrior')]
#
# warriorC = df2[(df2['mainClass']=='Warrior') & (df2["rarity"]=='common')]
# warriorU = df2[(df2['mainClass']=='Warrior') & (df2["rarity"]=='uncommon')]
# warriorR = df2[(df2['mainClass']=='Warrior') & (df2["rarity"]=='rare')]
# warriorL = df2[(df2['mainClass']=='Warrior') & (df2["rarity"]=='legendary')]
# warriorM = df2[(df2['mainClass']=='Warrior') & (df2["rarity"]=='mythic')]

warrior = df2

warriorC = df2[(df2["rarity"] == 'common')]
warriorU = df2[(df2["rarity"] == 'uncommon')]
warriorR = df2[(df2["rarity"] == 'rare')]
warriorL = df2[(df2["rarity"] == 'legendary')]
warriorM = df2[(df2["rarity"] == 'mythic')]

fig = go.Figure()

# px.scatter(warriorC, x="timeStamp", y="soldPrice",
#                 hover_name="id", hover_data={'rarity'})])

fig.add_trace(go.Scatter(x=warriorC.timeStamp, y=warriorC.soldPrice, mode='markers', name='Common',
                         hovertemplate=
                         '<b>ID</b>: %{text}<br>' +
                         '<b>Price</b>: %{y} Jewels' +
                         '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                         text=warriorC['id'] + '<br>' +
                              '<b>Rarity</b>: ' + warriorC['rarity'] + '<br>' +
                              '<b>Generation</b>: ' + warriorC['generation'] + '<br>' + '<br>' +
                              '<b>Main Class</b>: ' + warriorC['mainClass'] + '<br>' +
                              '<b>Sub Class</b>: ' + warriorC['subClass'] + '<br>' +
                              '<b>Primary Boost</b>: ' + warriorC['statBoost1'] + '<br>' +
                              '<b>Secondary Boost</b>: ' + warriorC['statBoost2'] + '<br>' +
                              '<b>Profession</b>: ' + warriorC['profession'] + '<br>',
                         marker=dict(color='rgba(219, 217, 222, 1)', size=7)

                         ))

fig.add_trace(go.Scatter(x=warriorU.timeStamp, y=warriorU.soldPrice, mode='markers', name='Uncommon',
                         hovertemplate=
                         '<b>ID</b>: %{text}<br>' +
                         '<b>Price</b>: %{y} Jewels' +
                         '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                         text=warriorU['id'] + '<br>' +
                              '<b>Rarity</b>: ' + warriorU['rarity'] + '<br>' +
                              '<b>Generation</b>: ' + warriorU['generation'] + '<br>' + '<br>' +
                              '<b>Main Class</b>: ' + warriorU['mainClass'] + '<br>' +
                              '<b>Sub Class</b>: ' + warriorU['subClass'] + '<br>' +
                              '<b>Primary Boost</b>: ' + warriorU['statBoost1'] + '<br>' +
                              '<b>Secondary Boost</b>: ' + warriorU['statBoost2'] + '<br>' +
                              '<b>Profession</b>: ' + warriorU['profession'] + '<br>',
                         marker=dict(color='rgba(115, 191, 131, 1)', size=7)
                         ))

fig.add_trace(go.Scatter(x=warriorR.timeStamp, y=warriorR.soldPrice, mode='markers', name='Rare',
                         hovertemplate=
                         '<b>ID</b>: %{text}<br>' +
                         '<b>Price</b>: %{y} Jewels' +
                         '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                         text=warriorR['id'] + '<br>' +
                              '<b>Rarity</b>: ' + warriorR['rarity'] + '<br>' +
                              '<b>Generation</b>: ' + warriorR['generation'] + '<br>' + '<br>' +
                              '<b>Main Class</b>: ' + warriorR['mainClass'] + '<br>' +
                              '<b>Sub Class</b>: ' + warriorR['subClass'] + '<br>' +
                              '<b>Primary Boost</b>: ' + warriorR['statBoost1'] + '<br>' +
                              '<b>Secondary Boost</b>: ' + warriorR['statBoost2'] + '<br>' +
                              '<b>Profession</b>: ' + warriorR['profession'] + '<br>',
                         marker=dict(color='rgba(53, 147, 183, 1)', size=7)
                         ))

fig.add_trace(go.Scatter(x=warriorL.timeStamp, y=warriorL.soldPrice, mode='markers', name='Legendary',
                         hovertemplate=
                         '<b>ID</b>: %{text}<br>' +
                         '<b>Price</b>: %{y} Jewels' +
                         '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                         text=warriorL['id'] + '<br>' +
                              '<b>Rarity</b>: ' + warriorL['rarity'] + '<br>' +
                              '<b>Generation</b>: ' + warriorL['generation'] + '<br>' + '<br>' +
                              '<b>Main Class</b>: ' + warriorL['mainClass'] + '<br>' +
                              '<b>Sub Class</b>: ' + warriorL['subClass'] + '<br>' +
                              '<b>Primary Boost</b>: ' + warriorL['statBoost1'] + '<br>' +
                              '<b>Secondary Boost</b>: ' + warriorL['statBoost2'] + '<br>' +
                              '<b>Profession</b>: ' + warriorL['profession'] + '<br>',
                         marker=dict(color='rgba(255, 164, 62, 1)', size=7)
                         ))

fig.add_trace(go.Scatter(x=warriorM.timeStamp, y=warriorM.soldPrice, mode='markers', name='Mythic',
                         hovertemplate=
                         '<b>ID</b>: %{text}<br>' +
                         '<b>Price</b>: %{y} Jewels' +
                         '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                         text=warriorM['id'] + '<br>' +
                              '<b>Rarity</b>: ' + warriorM['rarity'] + '<br>' +
                              '<b>Generation</b>: ' + warriorM['generation'] + '<br>' + '<br>' +
                              '<b>Main Class</b>: ' + warriorM['mainClass'] + '<br>' +
                              '<b>Sub Class</b>: ' + warriorM['subClass'] + '<br>' +
                              '<b>Primary Boost</b>: ' + warriorM['statBoost1'] + '<br>' +
                              '<b>Secondary Boost</b>: ' + warriorM['statBoost2'] + '<br>' +
                              '<b>Profession</b>: ' + warriorM['profession'] + '<br>',
                         marker=dict(color='rgba(178, 109, 216, 1)', size=7)
                         ))

fig.update_traces(marker=dict(line=dict(width=.5)))
fig.update_layout(title='Tavern Sales - Last 1000 Heroes Sold',
                  titlefont=dict(family='Arial', size=24),
                  xaxis=dict(showgrid=True, ticks='outside'),
                  xaxis_title='Date in UTC',
                  yaxis_title='Jewel',
                  plot_bgcolor='white'
                  )

fig.update_xaxes(showspikes=True)
fig.update_yaxes(showspikes=True)

# Initialize
# Setup the style from the link:
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Embed the style to the dashabord:
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    children=[
        html.H1(children="DeFi Kingdom Tavern Dashboards", ),
        html.Div(
            children="Random playground for various tavern dashboards."),

        html.Div(
            children="Data last updated: {}.".format(currentTime)),

        html.Div(
            children=[
                html.Div(children='Main Class', style={'fontSize': "16px", 'width': '50%'}, className='menu-title'),
                dcc.Dropdown(
                    id='main-class',
                    options=[
                        {'label': MainClass, 'value': MainClass}
                        for MainClass in warrior.mainClass.sort_values().unique()
                    ],  # 'warrior' is the filter
                    clearable=True,
                    searchable=False,
                    className='dropdown', style={'fontSize': "14px", 'textAlign': 'center'},
                ),
            ],
            className='menu',
        ),  # the dropdown function

        dcc.Graph(id='main-chart', figure=fig),

        dash_table.DataTable(id='main-table',
                             columns=[{"name": i, "id": i} for i in warrior.columns],
                             data=warrior.to_dict('records'))

    ]
)


@app.callback(
    [Output("main-table", "data")],
    [Input("main-class", "value")]
)
def update_tables(option_selected):
    if option_selected is None:
        filtered_df = warrior
    else:
        filtered_df = warrior[warrior['mainClass'] == option_selected]
    return [filtered_df.to_dict('records')]


@app.callback(
    Output("main-chart", "figure"),
    [Input("main-class", "value")]
)
def update_charts(option_selected):
    if option_selected is None:
        filtered_dataC = warrior[(warrior['rarity'] == 'common')]
        filtered_dataU = warrior[(warrior['rarity'] == 'uncommon')]
        filtered_dataR = warrior[(warrior['rarity'] == 'rare')]
        filtered_dataL = warrior[(warrior['rarity'] == 'legendary')]
        filtered_dataM = warrior[(warrior['rarity'] == 'mythic')]
    else:
        filtered_dataC = warrior[(warrior['mainClass'] == option_selected) & (warrior["rarity"] == 'common')]
        filtered_dataU = warrior[(warrior['mainClass'] == option_selected) & (warrior["rarity"] == 'uncommon')]
        filtered_dataR = warrior[(warrior['mainClass'] == option_selected) & (warrior["rarity"] == 'rare')]
        filtered_dataL = warrior[(warrior['mainClass'] == option_selected) & (warrior["rarity"] == 'legendary')]
        filtered_dataM = warrior[(warrior['mainClass'] == option_selected) & (warrior["rarity"] == 'mythic')]

    trace1 = go.Scatter(x=filtered_dataC.timeStamp, y=filtered_dataC.soldPrice, mode='markers', name='Common',
                        hovertemplate=
                        '<b>ID</b>: %{text}<br>' +
                        '<b>Price</b>: %{y} Jewels' +
                        '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                        text=filtered_dataC['id'] + '<br>' +
                             '<b>Rarity</b>: ' + filtered_dataC['rarity'] + '<br>' +
                             '<b>Generation</b>: ' + filtered_dataC['generation'] + '<br>' + '<br>' +
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
                             '<b>Generation</b>: ' + filtered_dataU['generation'] + '<br>' + '<br>' +
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
                             '<b>Generation</b>: ' + filtered_dataR['generation'] + '<br>' + '<br>' +
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
                             '<b>Generation</b>: ' + filtered_dataL['generation'] + '<br>' + '<br>' +
                             '<b>Main Class</b>: ' + filtered_dataL['mainClass'] + '<br>' +
                             '<b>Sub Class</b>: ' + filtered_dataL['subClass'] + '<br>' +
                             '<b>Primary Boost</b>: ' + filtered_dataL['statBoost1'] + '<br>' +
                             '<b>Secondary Boost</b>: ' + filtered_dataL['statBoost2'] + '<br>' +
                             '<b>Profession</b>: ' + filtered_dataL['profession'] + '<br>',
                        marker=dict(color='rgba(255, 164, 62, 1)', size=7)
                        )

    trace5 = go.Scatter(x=filtered_dataM.timeStamp, y=warriorM.soldPrice, mode='markers', name='Mythic',
                        hovertemplate=
                        '<b>ID</b>: %{text}<br>' +
                        '<b>Price</b>: %{y} Jewels' +
                        '<br><b>Sold At</b>: %{x} UTC<br><extra></extra>',
                        text=filtered_dataM['id'] + '<br>' +
                             '<b>Rarity</b>: ' + filtered_dataM['rarity'] + '<br>' +
                             '<b>Generation</b>: ' + filtered_dataM['generation'] + '<br>' + '<br>' +
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


if __name__ == "__main__":
    app.run_server()