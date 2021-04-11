import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from placa_fotovoltaica import main

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Layout
app.layout = html.Div(children=[
    html.H1(children='Placa Fotovoltaica'),
    html.Div(children='''
        Insira as entradas abaixo:
    '''),
    html.Div(["Digite o consumo médio mensal presente na conta de luz(kWh): ",
              dcc.Input(id='consumo', value=200, type='number')]),
    html.Br(),
    html.Div(["Digite valor pago com o consumo digitado acima: ",
              dcc.Input(id='valor_pago', value=300, type='number')]),
    html.Br(),
    html.Div(["Selecione o tipo de ligação: ",
              dcc.Dropdown(
                  id='tipo_ligacao',
                  options=[{'label': "Monofásico", 'value': 1},
                           {'label': "Bifásico", 'value': 2},
                           {'label': "Trifásico", 'value': 3}],
                  value=1
              )]),
    html.Br(),
    html.Div(["Digite a área disponível do telhado (área limite 30m²) ",
              dcc.Input(id='area_disp', value=30, type='number')]),
    html.Br(),
    dcc.Graph(id='example-graph',)
])

# Callbacks
@app.callback(Output('example-graph', 'figure'),
              [Input('consumo', 'value'),
               Input('valor_pago', 'value'),
               Input('tipo_ligacao', 'value'),
               Input('area_disp', 'value')])
def update_graph(consumo, valor_pago, tipo_ligacao, area_disp):
    results, results_df = main(consumo, valor_pago, tipo_ligacao, area_disp)
    fig = px.line(results_df, x="Tempo (anos)",
                  y="Economia (R$)", color="Taxa")
    fig.add_shape(type='line',
                x0=0,
                y0=results["preco_investimento"],
                x1=results_df["Tempo (anos)"].max(),
                y1=results["preco_investimento"],
                line=dict(color='Red',),
                xref='x',
                yref='y')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
