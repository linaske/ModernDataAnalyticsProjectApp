import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objects as go

# Read predictions data from .csv
data = pd.read_csv('data.csv', parse_dates=['timestamp'])

# Read reference data from .csv
data_ref = pd.read_csv('data_ref.csv', parse_dates=['timestamp'])

# Initialize app
app = dash.Dash(__name__)

# Define the server variable
server = app.server

# Set up layout
app.layout = html.Div(
    style={'font-family': 'Arial'},
    children=[
        html.H1('Crowdedness at Oude Markt'),
        html.Div(id='noise-level', className='box'),
        html.Div(id='highest-value', className='box'),
        dcc.Graph(
            id='line-chart',
            style={'background-color': 'white'}
        ),
        dcc.RangeSlider(
            id='time-selector',
            marks={i: {'label': str(data.loc[i, 'timestamp'].time()), 'style': {
                'transform': 'rotate(-45deg)', 'white-space': 'nowrap'}} for i in range(0, len(data), len(data) // 8)},
            min=0,
            max=len(data) - 1,
            value=[0, len(data) - 1],
            allowCross=False,
            pushable=1,
            className='slider'
        ),
    ])

# Define callbacks
@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    dash.dependencies.Output('noise-level', 'children'),
    dash.dependencies.Output('highest-value', 'children'),
    dash.dependencies.Input('time-selector', 'value')
)
def update_data(selected_indices):
    selected_start = data.loc[selected_indices[0], 'timestamp']
    selected_end = data.loc[selected_indices[1], 'timestamp']

    filtered_data = data[
        (data['timestamp'] >= selected_start) &
        (data['timestamp'] <= selected_end)
    ]

    filtered_data_ref = data_ref[
        (data_ref['timestamp'] >= selected_start) &
        (data_ref['timestamp'] <= selected_end)
    ]

    fig = go.Figure()

    # Add the predicted noise level line
    fig.add_trace(go.Scatter(
        x=filtered_data['timestamp'], y=filtered_data['value'], mode='lines', name='Predicted Noise Level', line=dict(width=3)))

    # Add the reference line
    fig.add_trace(go.Scatter(
        x=filtered_data_ref['timestamp'], y=filtered_data_ref['laeq'], mode='lines', name='Reference', line=dict(width=2, dash='dot', color='darkgrey')))

    # Calculate some statistics
    max_value = round(filtered_data['value'].max(), 2)
    max_timestamp = filtered_data.loc[filtered_data['value'].idxmax(), 'timestamp']

    avg_predicted = filtered_data['value'].mean()
    avg_reference = filtered_data_ref['laeq'].mean()

    # Define box behavior
    if avg_predicted >= avg_reference:
        noise_level = 'Busier than usual'
        box_color = 'red'
    else:
        noise_level = 'Calmer than usual'
        box_color = 'green'

    noise_level_box = html.Div(
        style={'background-color': box_color, 'padding': '10px', 'color': '#FFFFFF'},
        children=['Situation at Oude: ' + noise_level]
    )

    highest_value_box = html.Div(
        style={'background-color': 'white', 'padding': '10px', 'color': 'black'},
        children=['Highest Value: ' + str(max_value) + ' (Time: ' + str(max_timestamp.time()) + ')']
    )

# Modify layout
    fig.update_layout(
        xaxis=dict(
            title='Time',
            tickformat='%H:%M',
            tickfont=dict(family='Arial'),
            title_font=dict(family='Arial')
        ),
        yaxis=dict(title='Decibels (dB)', tickfont=dict(family='Arial')),
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

# Add red dot
    fig.add_trace(go.Scatter(x=[max_timestamp], y=[max_value], mode='markers', name='Highest Value', marker=dict(color='red', size=12)))

    return fig, noise_level_box, highest_value_box

if __name__ == '__main__':
    app.run_server(debug=True)