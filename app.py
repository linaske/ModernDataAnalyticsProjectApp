import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Generate sample noise data for one day in 10-minute intervals
timestamps = pd.date_range(start='2023-01-01 00:00:00', end='2023-01-01 23:50:00', freq='10T')
values = np.random.randn(len(timestamps))  # Random noise values

# Create a DataFrame
data = pd.DataFrame({'timestamp': timestamps, 'value': values})

# Initialize the Dash app
app = dash.Dash(__name__)

# Set up the Dash app layout
app.layout = html.Div(children=[
    html.H1('MDA Data Visualization: pilot run'),
    html.Div(id='noise-level', className='box'),
    html.Div(id='highest-value', className='box'),
    dcc.Graph(id='line-chart'),
    dcc.RangeSlider(
        id='time-selector',
        marks={i: {'label': str(timestamps[i].time()), 'style': {'transform': 'rotate(-45deg)', 'white-space': 'nowrap'}} for i in range(0, len(timestamps), len(timestamps)//8)},
        min=0,
        max=len(timestamps) - 1,
        value=[0, len(timestamps) - 1],
        allowCross=False,
        pushable=1
    ),
])

# Define the callback function
@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    dash.dependencies.Output('noise-level', 'children'),
    dash.dependencies.Output('highest-value', 'children'),
    dash.dependencies.Input('time-selector', 'value')
)
def update_data(selected_indices):
    selected_start = timestamps[selected_indices[0]].time()
    selected_end = timestamps[selected_indices[1]].time()
    
    filtered_data = data[
        (data['timestamp'].dt.time >= selected_start) &
        (data['timestamp'].dt.time <= selected_end)
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data['timestamp'], y=filtered_data['value'], mode='lines', name='Predicted Noise Level'))
    
    max_value = round(filtered_data['value'].max(), 2)
    max_timestamp = filtered_data.loc[filtered_data['value'].idxmax(), 'timestamp']
    
    median_of_day = data['value'].median()
    avg_value = round(filtered_data['value'].mean(), 2)
    
    if avg_value >= 1.3 * median_of_day:
        noise_level = 'Busy'
        box_color = 'red'
    elif avg_value <= 0.7 * median_of_day:
        noise_level = 'Calm'
        box_color = 'green'
    else:
        noise_level = 'Mild'
        box_color = 'orange'
    
    noise_level_box = html.Div(
        style={'background-color': box_color, 'padding': '10px', 'color': '#FFFFFF'},
        children=['Situation at Oude: ' + noise_level]
    )
    
    highest_value_box = html.Div(
        style={'background-color': 'white', 'padding': '10px', 'color': 'black'},
        children=['Highest Value: ' + str(max_value) + ' (Time: ' + str(max_timestamp.time()) + ')']
    )
    
    fig.add_trace(go.Scatter(x=[max_timestamp], y=[max_value], mode='markers', name='Highest Value', marker=dict(color='red', size=8)))
    
    return (
        {
            'data': [go.Scatter(x=filtered_data['timestamp'], y=filtered_data['value'], mode='lines', name='Predicted Noise Level'),
                    go.Scatter(x=[max_timestamp], y=[max_value], mode='markers', name='Highest Value', marker=dict(color='red', size=8))],
            'layout': go.Layout(xaxis=dict(title='Time'), yaxis=dict(title='Decibels'), showlegend=True)
        },
        noise_level_box,
        highest_value_box
    )

if __name__ == '__main__':
    app.run_server(debug=True)