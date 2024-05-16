import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

def create_dash_application():
    # Generate sample data
    df = pd.DataFrame({
        "Product": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Sales": [100, 150, 200, 250, 300, 350],
        "Region": ["East", "East", "East", "West", "West", "West"],
        "Date": pd.date_range(start="2021-01-01", periods=6, freq='M')
    })
    df['Month'] = df['Date'].dt.month

    # Initialize Dash app
    dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True, requests_pathname_prefix='/dash/')

    dash_app.layout = dbc.Container([
        dcc.RangeSlider(
            id='date-range-slider',
            min=0,
            max=len(df) - 1,
            value=[0, len(df) - 1],
            marks={i: {'label': date.strftime('%Y-%m'), 'style': {'transform': 'rotate(45deg)'}} for i, date in enumerate(df['Date'])},
            step=None,
        ),
        dcc.Graph(id='sales-bar-chart'),
        dcc.Graph(id='sales-line-chart'),
        dcc.Graph(id='region-pie-chart'),
        dcc.Graph(id='sales-scatter-plot'),
    ])

    @dash_app.callback(
        [Output('sales-bar-chart', 'figure'),
         Output('sales-line-chart', 'figure'),
         Output('region-pie-chart', 'figure'),
         Output('sales-scatter-plot', 'figure')],
        [Input('date-range-slider', 'value')]
    )
    def update_graphs(selected_date_range):
        filtered_df = df.iloc[selected_date_range[0]:selected_date_range[1]+1]

        # Bar chart for sales
        bar_fig = px.bar(filtered_df, x="Product", y="Sales", color="Region", title="Sales by Product and Region")

        # Line chart for sales over time
        line_fig = px.line(filtered_df, x="Date", y="Sales", color="Product", title="Sales Over Time")

        # Pie chart for region distribution
        pie_fig = px.pie(filtered_df, names="Region", values="Sales", title="Sales Distribution by Region")

        # Scatter plot for sales vs. month
        scatter_fig = px.scatter(filtered_df, x="Month", y="Sales", color="Product", title="Sales by Month")

        return bar_fig, line_fig, pie_fig, scatter_fig

    return dash_app

# If this script is executed as the main program, run the Dash app server
if __name__ == '__main__':
    app = create_dash_application()
    app.run_server(debug=True, host='0.0.0.0')
