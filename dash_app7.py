import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

def create_dash_application7():
    np.random.seed(42)
    date_range = pd.date_range(start="2019-01-01", end="2021-12-31", freq='M')
    sales_data = np.random.randint(100, 500, size=len(date_range))
    revenue_Z_data = np.random.randint(1000, 5000, size=len(date_range))  # Generate revenue Z data

    df = pd.DataFrame({
        'Date': date_range,
        'Sales': sales_data,
        'Revenue Z': revenue_Z_data  # Include revenue Z data in the dataframe
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
        go.Scatter(x=df['MonthYear'], y=df['Sales'], mode='lines+markers+text', name='Monthly Sales', text=df['Sales'], textposition="top center"),
        row=1, col=2,
        secondary_y=True,
    )

    # Add monthly revenue Z scatter plot to the second subplot, using the secondary y-axis
    fig.add_trace(
        go.Scatter(x=df['MonthYear'], y=df['Revenue Z'], mode='lines+markers+text', name='Revenue Z', text=df['Revenue Z'], textposition="top center"),
        row=1, col=2,
        secondary_y=True,
    )

    # Hide the secondary Y-axis (right side) completely
    fig.update_layout(
        yaxis2=dict(
            title="",                 # Remove the title
            showticklabels=False,     # Hide tick labels
            showgrid=False,           # Hide grid lines
            zeroline=False,           # Hide the zero line
            visible=False             # Hide the secondary y-axis entirely
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1, griddash='dash', showticklabels=False),  # Add light dashed grid and hide tick labels
        xaxis2=dict(showgrid=True, gridcolor='lightgray', gridwidth=1, griddash='dash'),  # Add light dashed grid
        yaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1, griddash='dash'),
    )

    # Hide the side number axis
    fig.update_yaxes(showticklabels=False, row=1, col=2)

    # Initialize Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True, requests_pathname_prefix='/dash7/')

    # App layout
    app.layout = html.Div([
        dcc.Graph(
            id='sales-graph',
            figure=fig,
            style={"width": "100%", "height": "100vh"},  # Make the graph occupy the full webpage
            config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'toggleSpikelines', 'resetViews', 'toggleHover', 'sendDataToCloud', 'toggleHoverClosestCartesian', 'toggleHoverCompareCartesian']} 
        )
    ])

    return app

# Main block to run the app
if __name__ == '__main__':
    app = create_dash_application7()
    app.run_server(debug=True, host='0.0.0.0')
