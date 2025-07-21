import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output


# external css stylesheets
external_stylesheets = [
    {
    'href':'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Z527NXFoaoApmYm81iuXoPkFOJwJ8ERdknLMPO',
    'crossOrigin':'anonymous'
}
]

patients = pd.read_csv('IndividualDetails.csv')
total=patients.shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
deaths = patients[patients['current_status'] == 'Deceased'].shape[0]


options=[
    {'label':'All', 'value':'All'},
    {'label':'Hospitalized', 'value': 'Hospitalized'},
    {'label':'Recovered', 'value':'Recovered'},
    {'label':'Deceased', 'value':'Deceased'}
]



app = dash.Dash(__name__,external_stylesheets=external_stylesheets)


app.layout=html.Div([
    html.H1("Corona Virus Pandemic", style={'text-align':'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.H3('Total Cases'),
                html.H4(total)
            ], className='card-body')
        ], className='card bg-danger text-white col-md-3 m-2'),

        html.Div([
            html.Div([
                html.H3('Active'),
                html.H4(active)
            ],className='card-body')
        ], className='card bg-info text-white col-md-3 m-2'),

        html.Div([
            html.Div([
                html.H3('Recovered'),
                html.H4(recovered)
            ],className='card-body')
        ], className='card bg-warning text-white col-md-3 m-2'),

        html.Div([
            html.Div([
                html.H3('Deaths'),
                html.H4(deaths)
            ],className='card-body')
        ], className='card bg-success text-white col-md-3 m-2'),
    ], className='row justify-content-center'),

    html.Br(),


    html.Div([], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value='All'),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row')
], className='container')


@app.callback(Output('bar','figure'), Input('picker', 'value'))
def update_graph(status_type):
    if status_type=='All':
        pbar = patients['detected_state'].value_counts().reset_index()
        pbar.columns = ['State', 'Count']
        return {'data':[go.Bar(x=pbar['State'], y=pbar['Count'])],
                'layout': go.Layout(title='State Total Count')}
    else:
        npat = patients[patients['current_status'] == status_type]
        pbar = npat['detected_state'].value_counts().reset_index()
        pbar.columns = ['State', 'Count']
        return {'data': [go.Bar(x=pbar['State'], y=pbar['Count'])],
                'layout': go.Layout(title='State Total Count')}


if __name__ == '__main__':
    app.run(debug=True)