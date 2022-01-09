# Meng Si

import pandas as pd
import numpy as np
import re
import requests
from app_functions import *


import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px

rows = range(10)
labels = get_labels(rows)
images = get_images(rows)
urls = get_labels(rows)


app = dash.Dash(__name__)

# colors = {
#     'background': '#111111',
#     'text': '#000000'
# }

app.layout = html.Div(children=[
    html.H1(
        children='Board Game Recommendation System',
        style={
            'textAlign': 'center'
        }
    ),

    html.H3(
        children='Enter games you like and we will recommend games for your taste!',
        style={
            'textAlign': 'center',
        }),


    html.Div(children=[
        # Input box to take in game names
        dcc.Input(
            id="games",
            type='text',
            placeholder="",
            value='',
            debounce=True,
            style={'marginLeft': '440px', 'width': '50%',
                   'height': '30px', 'display': 'inline-block', 'align': 'center'}
        ),
        # html.Div(id='output-gamename')
    ]),

    html.Div([
        html.Div(children=[
            # Dropdown box to choose the game type
            html.Br(),
            html.Label('Game Type:'),
            dcc.Dropdown(id='type',
                         options=[{'label': k, 'value': k} for k in ['All', "Abstract Games", "Children's Games",
                                                                     'Customizable Games', 'Family Games', "Party Games", 'Strategy Games',  'Thematic Games', 'Wargames']],
                         value='All',
                         ),
            # html.Div(id='output-gametype'),

            # A slider to choose the number of players
            html.Br(),
            html.Label('Players:'),
            dcc.Slider(
                id='players',
                min=0,
                max=10,
                step=1,
                value=0,
                marks={i: '' if i == 0 else {'label': str(
                    i), 'style': {'color': '#000000'}} for i in range(0, 11)},
                included=False
            ),
            # html.Div(id='output-numplayers'),

            # A rangeslider to choose the playtime
            html.Br(),
            html.Label('Play Time (min):'),
            dcc.Slider(
                id='playtime',
                min=0,
                max=120,
                step=10,
                value=0,
                marks={i: '' if i == 0 else {'label': str(
                    i), 'style': {'color': '#000000'}} for i in range(0, 130, 10)},
                included=False
            ),
            # html.Div(id='output-playtime'),

            # A slider to filter the player age
            html.Br(),
            html.Label('Age+:'),
            dcc.Slider(
                id='age',
                min=0,
                max=18,
                step=2,
                value=0,
                marks={i: '' if i == 0 else {'label': str(
                    i), 'style': {'color': '#000000'}} for i in range(0, 20, 2)},
                included=False
            ),
            # html.Div(id='output-age'),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '40px', 'width': '40%'}
        ),

        html.Div(children=[

            # Dropdown box to choose the game type
            html.Br(),
            html.Label('Cooperative:'),
            dcc.Dropdown(id='cooperative',
                         options=[
                             {'label': "All", 'value': 0},
                             {'label': 'Only Cooperative', 'value': 1},
                             {'label': 'Only Competitive', 'value': 2},
                         ],
                         value=0,
                         ),
            # html.Div(id='output-cooperative'),

            # Slider to choose the range of ranking
            html.Br(),
            html.Label('BGG Rank:'),
            dcc.Slider(
                id='rank',
                min=100,
                max=1000,
                step=100,
                value=1000,
                marks={i: {'label': str(
                    i), 'style': {'color': '#000000'}} for i in range(100, 1100, 100)},
                included=True
            ),
            # html.Div(id='output-rank'),



            # A rangeslider to filter the complexity
            html.Br(),
            html.Label('Complexity:'),
            dcc.RangeSlider(
                id='complexity',
                min=0,
                max=5,
                step=0.1,
                value=[0, 5],
                tooltip={"placement": "bottom", "always_visible": True},
                # marks={i: '' if i == 0 else {'label': str(
                #     i), 'style': {'color': '#000000'}} for i in range(0, 5, 1)},
                allowCross=False
            ),
            # html.Div(id='output-complexity'),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '40px', 'width': '40%'}
        ), ], style={'display': 'flex', 'flex-direction': 'row'}),

    # Display the results
    html.Div(children=[

        # Add an image
        html.Div(children=[
            html.A(labels[0], id='l1', href=urls[0]),
            html.Br(),
            html.Img(id='image1', src=images[0]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '40px'}),

        # Add an image
        html.Div(children=[
            html.A(labels[1], id='l2', href=urls[1]),
            html.Br(),
            html.Img(id='image2', src=images[1]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '20px'}),

        # Add an image
        html.Div(children=[
            html.A(labels[2], id='l3', href=urls[2]),
            html.Br(),
            html.Img(id='image3', src=images[2]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '20px'}),

        # Add an image
        html.Div(children=[
            html.A(labels[3], id='l4', href=urls[3]),
            html.Br(),
            html.Img(id='image4', src=images[3]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '20px'}),

        # Add an image
        html.Div(children=[
            html.A(labels[4], id='l5', href=urls[4]),
            html.Br(),
            html.Img(id='image5', src=images[4]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '20px'}),

    ], style={'display': 'flex', 'flex-direction': 'row'}),

    # Display the results
    html.Div(children=[

        # Add an image
        html.Div(children=[
            html.A(labels[5], id='l6', href=urls[5]),
            html.Br(),
            html.Img(id='image6', src=images[5]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '40px'}),

        # Add an image
        html.Div(children=[
            html.A(labels[6], id='l7', href=urls[6]),
            html.Br(),
            html.Img(id='image7', src=images[6]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '20px'}),

        # Add an image
        html.Div(children=[
            html.A(labels[7], id='l8', href=urls[7]),
            html.Br(),
            html.Img(id='image8', src=images[7]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '20px'}),

        # Add an image
        html.Div(children=[
            html.A(labels[8], id='l9', href=urls[8]),
            html.Br(),
            html.Img(id='image9', src=images[8]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '20px'}),

        # Add an image
        html.Div(children=[
            html.A(labels[9], id='l10', href=urls[9]),
            html.Br(),
            html.Img(id='image10', src=images[9]),

        ], style={'padding': 10, 'flex': 1, 'marginLeft': '20px'}),

    ], style={'display': 'flex', 'flex-direction': 'row'}),

])


@app.callback(
    Output('l1', 'children'),
    Output('l2', 'children'),
    Output('l3', 'children'),
    Output('l4', 'children'),
    Output('l5', 'children'),
    Output('l6', 'children'),
    Output('l7', 'children'),
    Output('l8', 'children'),
    Output('l9', 'children'),
    Output('l10', 'children'),
    Output('l1', 'href'),
    Output('l2', 'href'),
    Output('l3', 'href'),
    Output('l4', 'href'),
    Output('l5', 'href'),
    Output('l6', 'href'),
    Output('l7', 'href'),
    Output('l8', 'href'),
    Output('l9', 'href'),
    Output('l10', 'href'),
    Output('image1', 'src'),
    Output('image2', 'src'),
    Output('image3', 'src'),
    Output('image4', 'src'),
    Output('image5', 'src'),
    Output('image6', 'src'),
    Output('image7', 'src'),
    Output('image8', 'src'),
    Output('image9', 'src'),
    Output('image10', 'src'),
    Input('games', 'value'),
    Input('type', 'value'),
    Input('players', 'value'),
    Input('playtime', 'value'),
    Input('age', 'value'),
    Input('cooperative', 'value'),
    Input('rank', 'value'),
    Input('complexity', 'value'),

)
def update(games, type, players, playtime, age, cooperative, rank, complexity):
    rows = recommend_indices(games)
    filtered_rows = filtered_indices(
        rows, type, players, playtime, age, cooperative, rank, complexity)
    labels = get_labels(filtered_rows)
    urls = get_urls(filtered_rows)
    images = get_images(filtered_rows)

    return labels[0], labels[1], labels[2], labels[3], labels[4], labels[5], labels[6], labels[7], labels[8], labels[9], urls[0], urls[1], urls[2], urls[3], urls[4], urls[5], urls[6], urls[7], images[8], urls[9], images[0], images[1], images[2], images[3], images[4], images[5], images[6], images[7], images[8], images[9]


if __name__ == '__main__':
    app.run_server(debug=True)
