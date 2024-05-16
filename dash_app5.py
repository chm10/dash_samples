import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

def create_dash_application5():
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
    yearly_sales = df.groupby('Year')['Sales'].sum().reset_index()

    # Create a subplot with twin y-axes for the second subplot
    fig = make_subplots(rows=1, cols=2, 
                        specs=[[{"secondary_y": False}, {"secondary_y": True}]], 
                        shared_xaxes=True,
                        column_widths=[0.1, 0.9],
                        horizontal_spacing=0
                        )

    # Add yearly sales bar plot to the first subplot
    fig.add_trace(
        go.Bar(x=yearly_sales['Year'], y=yearly_sales['Sales'], name='Annual Sales'),
        row=1, col=1,
        secondary_y=False,
    )

    # Add monthly sales scatter plot to the second subplot, using the secondary y-axis
    fig.add_trace(
        go.Scatter(x=df['MonthYear'], y=df['Sales'], mode='lines+markers', name='Monthly Sales'),
        row=1, col=2,
        secondary_y=True,
    )

    # Update layout
    fig.update_layout(
        title_text="Sales Data Overview",
        xaxis2=dict(domain=[0.1, 1]),
        # Optional: Adjust the layout or appearance as needed
    )

    # Initialize Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True, requests_pathname_prefix='/dash5/')

    # App layout
    app.layout = html.Div([
        dcc.Graph(
            id='sales-graph',
            figure=fig,
            style={"width": "100%", "height": "100vh"
            
            }  # Make the graph occupy the full webpage
        )
    ])

    return app

# Main block to run the app
if __name__ == '__main__':
    app = create_dash_application5()
    app.run_server(debug=True, host='0.0.0.0')
