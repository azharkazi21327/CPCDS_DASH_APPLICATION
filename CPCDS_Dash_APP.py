import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# =========================================

df = pd.read_csv('Claims.csv')
# Yearly Payout Progress with (Diagnosis_Description)
df['year'] = pd.to_datetime(df['Claim paid date']).dt.strftime("%Y-%m-%d")
df["Procedure description"] = df["Procedure description"].fillna("Without Procedure description")
df["Diagnosis description"] = df["Diagnosis description"].fillna("Without Diagnosis description")
year = sorted(list(dict.fromkeys(df['year'])))
diagnosis_description = sorted(list(dict.fromkeys(df['Diagnosis description'])))
payout_progress_header = ['year']
payout_progress_header.extend(diagnosis_description)
progress_data_frame = []
for i in year:
    payout_data = []
    payout_data += [i, ]
    for j in diagnosis_description:
        df_filter = df[(df['year'] == i) & (df['Diagnosis description'] == j)]
        payout = df_filter["Claim payment amount"].sum(axis=0, skipna=True)
        payout_data += [payout, ]
    progress_data_frame += [payout_data, ]
payout_progress_DD = pd.DataFrame(progress_data_frame, columns=payout_progress_header)

payout_progress1 = payout_progress_DD

row, col = payout_progress_DD.shape

# print(payout_progress.iat[0,1])
for i in range(1, row):
    for j in range(1, col):
        payout_progress_DD.iat[i, j] = payout_progress_DD.iat[i, j] + payout_progress_DD.iat[i - 1, j]

# +++++++***************+++++++++++++++++**************
# Yearly Payout Progress with (Procedure description)
procedure_description = sorted(list(dict.fromkeys(df['Procedure description'])))
payout_progress_header = ['year']
payout_progress_header.extend(procedure_description)
progress_data_frame = []
for i in year:
    payout_data = []
    payout_data += [i, ]
    for j in procedure_description:
        df_filter = df[(df['year'] == i) & (df['Procedure description'] == j)]
        payout = df_filter["Claim payment amount"].sum(axis=0, skipna=True)
        payout_data += [payout, ]
    progress_data_frame += [payout_data, ]
payout_progress_PD = pd.DataFrame(progress_data_frame, columns=payout_progress_header)

payout_progress2 = payout_progress_PD

row, col = payout_progress_PD.shape

# print(payout_progress.iat[0,1])
for i in range(1, row):
    for j in range(1, col):
        payout_progress_PD.iat[i, j] = payout_progress_PD.iat[i, j] + payout_progress_PD.iat[i - 1, j]

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# The App Layout

app.layout = html.Div([
    html.Div([
        html.Label(["CPCDS Sample Data Set Analysis"]),
        html.Div([
            dcc.Graph(id='CPCDS_DD_Graph')
        ], className='nine columns'),

        html.Div([
            html.Br(),
            html.Label(['Choose 3 Diagnosis description to compare:'],
                       style={'font-weight': 'bold', 'text-align': 'center'}),
            dcc.Dropdown(id='Diagnosis_description_one',
                         options=[{'label': x, 'value': x} for x in diagnosis_description
                                  ],
                         value='COVID-19',
                         multi=False,
                         disabled=False,
                         clearable=True,
                         searchable=True,
                         placeholder='Choose Diagnosis description',
                         className='from-dropdown',

                         persistence='string',
                         persistence_type='memory'),

            dcc.Dropdown(id='Diagnosis_description_two',
                         options=[{'label': x, 'value': x} for x in diagnosis_description
                                  ],
                         value='Cystitis',
                         multi=False,
                         clearable=False,
                         persistence='string',
                         persistence_type='local'),

            dcc.Dropdown(id='Diagnosis_description_three',
                         options=[{'label': x, 'value': x} for x in diagnosis_description
                                  ],
                         value='Fracture of ankle',
                         multi=False,
                         clearable=False,
                         persistence='string',
                         persistence_type='local'),

        ], className='two columns'),

        # For Procedure Description

        html.Div([
            dcc.Graph(id='CPCDS_PD_Graph')
        ], className='nine columns'),
        html.Div([
            html.Br(),
            html.Label(['Choose 3 Procedure description to compare:'],
                       style={'font-weight': 'bold', 'text-align': 'center'}),
            dcc.Dropdown(id='Procedure_description_one',
                         options=[{'label': x, 'value': x} for x in procedure_description
                                  ],
                         value='Ankle X-ray',
                         multi=False,
                         disabled=False,
                         clearable=True,
                         searchable=True,
                         placeholder='Choose Procedure description',
                         className='from-dropdown',

                         persistence='string',
                         persistence_type='memory'),

            dcc.Dropdown(id='Procedure_description_two',
                         options=[{'label': x, 'value': x} for x in procedure_description
                                  ],
                         value='Bone immobilization',
                         multi=False,
                         clearable=False,
                         persistence='string',
                         persistence_type='local'),

            dcc.Dropdown(id='Procedure_description_three',
                         options=[{'label': x, 'value': x} for x in procedure_description
                                  ],
                         value='Colonoscopy',
                         multi=False,
                         clearable=False,
                         persistence='string',
                         persistence_type='local'),

        ], className='two columns'),
    ])
])


# The Call Back

@app.callback(
    Output('CPCDS_DD_Graph', 'figure'),
    [Input('Diagnosis_description_one', 'value'),
     Input('Diagnosis_description_two', 'value'),
     Input('Diagnosis_description_three', 'value')]
)
def build_graph(diagnosis_description_one, diagnosis_description_two, diagnosis_description_three):
    dff1 = payout_progress_DD

    fig1 = px.line(dff1, x="year", y=[diagnosis_description_one, diagnosis_description_two,
                                      diagnosis_description_three], height=600)
    fig1.update_layout(yaxis={'title': 'Claim payment amount'},
                       title={'text': 'CPCDS Analysis Line Chart for Diagnosis Description',
                              'font': {'size': 28}, 'x': 0.5, 'xanchor': 'center'})
    return fig1


@app.callback(
    Output('CPCDS_PD_Graph', 'figure'),
    [Input('Procedure_description_one', 'value'),
     Input('Procedure_description_two', 'value'),
     Input('Procedure_description_three', 'value')]
)
def build_graph(procedure_description_one, procedure_description_two, procedure_description_three):
    dff2 = payout_progress_PD

    fig2 = px.line(dff2, x="year",
                   y=[procedure_description_one, procedure_description_two, procedure_description_three],
                   height=600)
    fig2.update_layout(yaxis={'title': 'Claim payment amount'},
                       title={'text': 'CPCDS Analysis Line Chart for Procedure Description',
                              'font': {'size': 28}, 'x': 0.5, 'xanchor': 'center'})
    return fig2


# -----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)
