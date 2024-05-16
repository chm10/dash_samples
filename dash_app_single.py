import dash
from dash import Dash, html, dcc  # Updated imports
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
def create_dash_application():

    df = pd.DataFrame({
        "Product": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Sales": [100, 150, 200, 250, 300, 350],
        "Region": ["East", "East", "East", "West", "West", "West"]
    })

    # Create a Plotly figure
    fig = px.bar(df, x="Product", y="Sales", color="Region", barmode="group",
                color_discrete_map={"East": "#007aff", "West": "#5ac8fa"})  # Colors inspired by Apple's color scheme

    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    # Dash app setup
    dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True, requests_pathname_prefix='/dash/')

    dash_app.layout = dbc.Container([
        dbc.Row(dbc.Col(html.H1("Sales Insights", style={'color': '#1d1d1f', 'fontFamily': 'Helvetica Neue, sans-serif', 'fontWeight': 'bold', 'fontSize': 40, 'marginTop': '2rem', 'textAlign': 'center'}), width=12)),
        dbc.Row(dbc.Col(html.Div("An interactive visualization of sales data.", style={'color': '#6e6e73', 'fontFamily': 'Helvetica Neue, sans-serif', 'fontSize': 20, 'textAlign': 'center'}))),
        dbc.Row([
            dbc.Col(dcc.Graph(id='sales-bar-chart', figure=fig), md=12),
        ])
    ], fluid=True, style={'maxWidth': '1200px'})

    return dash_app
