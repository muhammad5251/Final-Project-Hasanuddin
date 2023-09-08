import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Load data
data_url = "https://raw.githubusercontent.com/muhammad5251/DataVisualization/data/aggregate_data_2023-01-08.csv"
data = pd.read_csv(data_url)
data3 = data[['PARLIAMENTARY NAME', 'TOTAL ELECTORS', 'MALAY (%)', 'CHINESE (%)']]
data3 = data3.sort_values('TOTAL ELECTORS', ascending=False)

# Create figures
fig_bar = px.bar(data3, x='PARLIAMENTARY NAME', y='TOTAL ELECTORS', title='Total Electors by Constituency')

# Define custom elector ranges
elector_ranges = [
    (150001, 200000),
    (200001, 250000),
    (250001, 300000),
    (300001, 350000),
    (350001, 400000),
    (400001, 450000),
    (450001, 500000),
]

# Convert the elector_ranges to string labels with "k"
elector_range_labels = [
    f'{min_range//1000}k-{max_range//1000}k'
    for min_range, max_range in elector_ranges
]

# Convert the values to strings
elector_range_values = [
    f'{min_range}-{max_range}'
    for min_range, max_range in elector_ranges
]



fig_box = px.box(data3, x='TOTAL ELECTORS', title='Box Plot of Total Electors by Constituency')


# Given data
data = {
    'PARLIAMENTARY NAME': ['BANGI', 'KOTA RAJA', 'DAMANSARA', 'SUBANG', 'TEBRAU', 'ISKANDAR PUTERI',
                           'KLANG', 'GOMBAK', 'PASIR GUDANG', 'PETALING JAYA'],
    'TOTAL ELECTORS': [303430, 244712, 239103, 230940, 223301, 222437, 208913, 206744, 198485, 195148],
    'MALAY (%)': [48.43, 39.81, 20.66, 26.25, 44.96, 36.27, 26.65, 69.94, 46.13, 46.15],
    'CHINESE (%)': [36.96, 29.68, 66.14, 54.04, 38.77, 47.22, 52.77, 10.86, 36.17, 29.56]
}

# Create the DataFrame
data3 = pd.DataFrame(data)

# Create the pie chart for Malay population
fig_pie_malay = px.pie(data3, values='MALAY (%)', names='PARLIAMENTARY NAME', title='Malay Population (%) by Constituency')

# Create the pie chart for Chinese population
fig_pie_chinese = px.pie(data3, values='CHINESE (%)', names='PARLIAMENTARY NAME', title='Chinese Population (%) by Constituency')

# Define a callback to update the x-axis labels of the bar chart based on the dropdown value
@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
    dash.dependencies.Input('elector-range-dropdown', 'value')
)
def update_bar_chart(selected_elector_range):
    min_range, max_range = map(int, selected_elector_range.split('-'))
    filtered_data = data3[(data3['TOTAL ELECTORS'] >= min_range) & (data3['TOTAL ELECTORS'] <= max_range)]
    fig = px.bar(filtered_data, x='PARLIAMENTARY NAME', y='TOTAL ELECTORS', title='Total Electors by Constituency')
    fig.update_xaxes(title_text='PARLIAMENTARY NAME')
    return fig

# Define a callback to update the population chart based on the selected radio item
@app.callback(
    dash.dependencies.Output('population-chart', 'figure'),
    dash.dependencies.Input('population-radio', 'value')
)
def update_population_chart(selected_population):
    if selected_population == 'malay':
        return fig_pie_malay
    elif selected_population == 'chinese':
        return fig_pie_chinese
                          
# Define app layout with improved styling
app.layout = html.Div([
    html.H1("Hasanuddin Assignment 3", style={'text-align': 'center'}),
    
     dcc.Tabs([
        dcc.Tab(label='Bar Chart', children=[
            html.H3("Select range"),
            dcc.Dropdown(
                id='elector-range-dropdown',
                options=[
                    {'label': label, 'value': value}
                    for label, value in zip(elector_range_labels, elector_range_values)
                ],
                value=elector_range_values[0]  # Default value
            ),
            dcc.Graph(id='bar-chart', figure=fig_bar)
        ]),
        dcc.Tab(label='Box Plot', children=[
            dcc.Graph(figure=fig_box),
        ]),
        dcc.Tab(label='Population', children=[
            dcc.RadioItems(
                id='population-radio',
                options=[
                    {'label': 'Malay Population', 'value': 'malay'},
                    {'label': 'Chinese Population', 'value': 'chinese'}
                ],
                value='malay',  # Default value
                labelStyle={'display': 'block'}
            ), 
            html.Br(),
            dcc.Graph(id='population-chart')
        ]),
    ], style={'width': '80%', 'margin': '0 auto', 'padding': '20px'}),
], style={'background-color': '#f0f0f0', 'padding': '20px'})



if __name__ == '__main__':
    app.run_server(debug=True)
