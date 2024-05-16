import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

def create_dash_application4():
    # Generate sample data
    np.random.seed(42)
    date_range = pd.date_range(start="2019-01-01", end="2021-12-31", freq='M')
    sales_data = np.random.randint(100, 500, size=len(date_range))

    df = pd.DataFrame({
        'Date': date_range,
        'Sales': sales_data
    })

    df['Year'] = df['Date'].dt.year
    df['MonthYear'] = df['Date'].dt.strftime('%b %Y')

    # Aggregate yearly sales data
    yearly_sales = df.groupby('Year')['Sales'].sum().reset_index()

    # Create the combined graph
    fig = make_subplots(
        rows=1, cols=2, 
        specs=[[{}, {}]], 
        shared_yaxes=True,
        subplot_titles=('Annual Sales', 'Monthly Sales'),
        column_widths=[0.1, 0.9],  # First plot smaller, second plot larger
        horizontal_spacing=0  # Minimal spacing between subplots
    )


    # Add plots to the figure as before
    fig.add_trace(
        go.Bar(x=yearly_sales['Year'], y=yearly_sales['Sales'], name='Annual Sales'),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=df['MonthYear'], y=df['Sales'], mode='lines+markers', name='Monthly Sales'),
        row=1, col=2
    )

    # Update layout for unified look, with adjusted margins if necessary
    fig.update_layout(
        #height=600, width=1000, 
        title_text="Sales Data Overview",
        autosize=True,
        margin=dict(l=20, r=20, t=100, b=20)  # Adjust margins if necessary
    )

    fig.update_xaxes(tickangle=45, tickfont=dict(size=10), col=2)
    # Initialize Dash app
    dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True, requests_pathname_prefix='/dash4/')

    # Set up the layout
    dash_app.layout = html.Div([
        dcc.Graph(
            id='combined-sales-graph',
            figure=fig,
            style={'height': '90vh', 'width': '100vw'}  # Use viewport units
        )
    ], style={'height': '100vh', 'width': '100vw', 'padding': '0', 'margin': '0'})

    return dash_app

# Main block to run the app
if __name__ == '__main__':
    app = create_dash_application4()
    app.run_server(debug=True, host='0.0.0.0')
