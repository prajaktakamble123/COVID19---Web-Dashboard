import numpy as np
import pandas as pd
import dash
from dash import html
from dash import dcc  # dash_core_components
from dash.dependencies import Output, Input
import plotly.graph_objects as go

df = pd.read_csv("C:/Users/LENOVO/Downloads/IndividualDetails.csv")

external_stylesheets = [
    {
        'href': "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH",
        "crossorigin": "anonymous"
    }
]

dropdown_options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalised', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]

app = dash.Dash(external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Corona Virus Dashboard", className='text-center text-light p-5'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Total Patients', className='text-center'),
                    html.H4(df.shape[0], className='text-center')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Total Hospitalised', className='text-center'),
                    html.H4(df['current_status'].value_counts()[0], className='text-center')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Total Recovered', className='text-center'),
                    html.H4(df['current_status'].value_counts()[1], className='text-center')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Total Deceased', className='text-center'),
                    html.H4(df['current_status'].value_counts()[2], className='text-center')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-3')
    ], className='row pb-5 px-5'),
    html.Div([
        html.Div([
            dcc.Graph(id='line', figure={
                'data': [
                    go.Scatter(x=df["diagnosed_date"].value_counts().index,
                               y=df["diagnosed_date"].value_counts().values)
                ],
                'layout': {'title': 'Date wise diagnose count'}
            })
        ], className='col-6'),
        html.Div([
            dcc.Graph(id='pie', figure={
                'data': [
                    go.Pie(values=df['gender'].value_counts().values,
                           text=['Male', 'Female'],
                           labels=['Male', 'Female'])
                ],
                'layout': {'title': 'Gender wise diagnose count'}
            })
        ], className='col-6')
    ], className='row pb-5 px-5'),
    html.Div([
        html.Div([
            dcc.Dropdown(id='dropdown', options=dropdown_options, value='All', className='mb-2'),
            dcc.Graph(id='bar')
        ], className='col-12')
    ], className='row px-5 pb-5')
], className='container-fluid bg-dark')


@app.callback(Output('bar', 'figure'), [Input('dropdown', 'value')])
def update(choice):
    if choice == 'All':
        return {
                'data': [
                    go.Bar(x=df['detected_state'].value_counts().index,
                           y=df['detected_state'].value_counts().values)
                ],
                'layout': {'title': 'State wise patient count'}
            }
    else:
        filter_df = df[df['current_status'] == choice]
        return {
            'data': [
                go.Bar(x=filter_df['detected_state'].value_counts().index,
                       y=filter_df['detected_state'].value_counts().values)
            ],
            'layout': {'title': 'State wise patient count'}
        }


app.run(debug=True)
