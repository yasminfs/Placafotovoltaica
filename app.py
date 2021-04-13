import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from placa_fotovoltaica import main
import numpy as np

app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1(children='Placa Fotovoltaica'),
    html.Div(children='''Insira as entradas abaixo:'''),
    html.Div(["Digite o consumo médio mensal presente na conta de luz: ",
              dcc.Input(id='consumo', value=650, type='number'), " (kWh)"]),
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
    html.Div(["Digite a área disponível do telhado: ",
              dcc.Input(id='area_disp', value=30, type='number'), " (m²)"]),
    html.Br(),
    html.Div(id='results_info'),
    html.Div(dcc.Graph(id='economia-graph')),
])

# Callbacks


@app.callback([Output('economia-graph', 'figure'),
               Output('results_info', 'children')],
              [Input('consumo', 'value'),
               Input('tipo_ligacao', 'value'),
               Input('area_disp', 'value')])
def update_graph(consumo, tipo_ligacao, area_disp):
    results, results_df = main(consumo, tipo_ligacao, area_disp)
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
    vals = list(results.values())
    results_str = [f"Energia Geração {np.round(vals[0],2)} kWh", html.Br(),
                   f"Rendimento {np.round(vals[1],2)}", html.Br(),
                   f"Potência painéis {np.round(vals[2],2)} kW", html.Br(),
                   f"Número de painéis {np.round(vals[3],2)}", html.Br(),
                   f"Área necessária {np.round(vals[4],2)} m²", html.Br(),
                   f"Potência gerada {np.round(vals[5],2)} kW ", html.Br(),
                   f"Potência/dia {np.round(vals[6],2)} kW/dia", html.Br(),
                   f"Potência/mês {np.round(vals[7],2)} kW/mês ", html.Br(),
                   f"Valor investido {np.round(vals[8],2)} (R$)", html.Br()]
    return fig, results_str


if __name__ == '__main__':
    app.run_server(debug=True)
