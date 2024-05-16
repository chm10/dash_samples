import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import json
import dash_bootstrap_components as dbc
def create_dash_application2():
    # Sample DataFrame
    df = pd.DataFrame({
        'x': [1, 2, 3, 4],
        'y': [10, 11, 12, 13],
        'label': ['', '', '', '']  # Initially, labels are empty
    })

    # Create the Dash app
    dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True, requests_pathname_prefix='/dash2/')

    # Set up the layout
    dash_app.layout = html.Div([
        dcc.Graph(
            id='scatter-plot',
            figure=px.scatter(df, x='x', y='y', text='label'),
            style={'height': 400},
            config={'staticPlot': False, 'scrollZoom': False, 'doubleClick': 'reset'}
        ),
        html.Br(),
        html.Div("Click on a point to label it:"),
        dcc.Input(id='label-input', type='text'),
        html.Button('Update Label', id='update-label-btn'),
        html.Div(id='click-data', style={'display': 'none'})
    ])

    @dash_app.callback(
        Output('click-data', 'children'),
        Input('scatter-plot', 'clickData'),
        prevent_initial_call=True
    )
    def display_click_data(clickData):
        if clickData:
            return json.dumps(clickData['points'][0])
        return dash.no_update

    @dash_app.callback(
        Output('scatter-plot', 'figure'),
        Input('update-label-btn', 'n_clicks'),
        [State('click-data', 'children'), State('label-input', 'value')],
        prevent_initial_call=True
    )
    def update_label(n_clicks, click_data_json, label):
        if click_data_json and label:
            click_data = json.loads(click_data_json)
            point_index = click_data['pointIndex']
            df.loc[point_index, 'label'] = label  # Update the DataFrame

            # Update the figure
            fig = px.scatter(df, x='x', y='y', text='label')
            return fig
        return dash.no_update

    return dash_app
