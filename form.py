import dash
from dash import dcc, html, Input, Output, State
from dash import callback
import dash.dash_table as dt
import pandas as pd
import os
import json

with open("nazwy_IBA.json", "r") as f:
    IBA_NAZWY = json.load(f)

NAZWY_OSTOI_LISTA  = IBA_NAZWY['Nazwy ostoi']
NAZWY_POLSKIE = IBA_NAZWY['Nazwy polskie']
# Strona z formularzem
form_layout =  html.Div([
    html.H2('Formularz', style={'text-align': 'center', 'margin-bottom': '30px'}),
    html.Div([
        html.Label('Nazwa ostoi:', style={'display': 'block', 'margin-bottom': '10px'}),
        dcc.Dropdown(
            id="input-nazwa-ostoi",
            options=NAZWY_OSTOI_LISTA,
            placeholder="Wybierz opcję",
            style={'width': '300px', 'height': '40px', 'font-size': '18px', 'margin-bottom': '20px'}
        ),
        html.Br(),
        html.Label('Nazwa polska:', style={'display': 'block', 'margin-bottom': '10px'}),
        #dcc.Input(id='input-nazwa-polska', type='text', placeholder='Wpisz nazwę polską',
        #          style={'width': '300px', 'height': '40px', 'font-size': '18px', 'margin-bottom': '20px'}),
        dcc.Dropdown(
            id="input-nazwa-polska",
            options=NAZWY_POLSKIE,
            placeholder="Wybierz opcję",
            style={'width': '300px', 'height': '40px', 'font-size': '18px', 'margin-bottom': '20px'}
        ),
        html.Br(),
        html.Label('Status:', style={'display': 'block', 'margin-bottom': '10px'}),
        dcc.Dropdown(
            id="input-status",
            options=["L", "M"],
            placeholder="Wybierz opcję",
            style={'width': '300px', 'height': '40px', 'font-size': '18px', 'margin-bottom': '20px'}
        ),
        html.Br(),
        html.Label('Liczba par (min):', style={'display': 'block', 'margin-bottom': '10px'}),
        dcc.Input(id='input-liczba-par-min', type='number', placeholder='Wpisz liczbę par minimalną',
                  style={'width': '300px', 'height': '40px', 'font-size': '18px', 'margin-bottom': '20px'}),
        html.Br(),
        html.Label('Liczba par (max):', style={'display': 'block', 'margin-bottom': '10px'}),
        dcc.Input(id='input-liczba-par-max', type='number', placeholder='Wpisz liczbę par maksymalną',
                  style={'width': '300px', 'height': '40px', 'font-size': '18px', 'margin-bottom': '20px'}),
        html.Br(),
        html.Label('Dokładność oszacowania:', style={'display': 'block', 'margin-bottom': '10px'}),
        dcc.Dropdown(
            id="input-dokladnosc-oszac",
            options=["dokładne liczenie", "przyblizony szacunek", "ekstrapolacja"],
            placeholder="Wybierz opcję",
            style={'width': '300px', 'height': '40px', 'font-size': '18px', 'margin-bottom': '20px'}
        ),
        html.Br(),
        html.Label('Rok:', style={'display': 'block', 'margin-bottom': '10px'}),
        dcc.Input(id='input-rok', type='number', placeholder='Wpisz rok',
                  style={'width': '300px', 'height': '40px', 'font-size': '18px', 'margin-bottom': '20px'}),
        html.Br(),
        html.Button('Zapisz', id='save-button', style={'width': '150px', 'height': '40px', 'font-size': '18px', 'margin-top': '10px'}),
        html.Div(id='output-message', style={'margin-top': '10px'})
    ], style={'text-align': 'center', 'display': 'inline-block', 'padding': '20px'}),

    # Tabela, która wyświetla zapisane dane
    html.Div(id='table-container', style={'margin-top': '40px'})
], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center', 'height': 'auto'})



# Callback do obsługi formularza i zapisywania danych do pliku CSV
@callback(
    [Output('output-message', 'children'),
     Output('table-container', 'children')],
    Input('save-button', 'n_clicks'),
    State('input-nazwa-ostoi', 'value'),
    State('input-nazwa-polska', 'value'),
    State('input-status', 'value'),
    State('input-liczba-par-min', 'value'),
    State('input-liczba-par-max', 'value'),
    State('input-dokladnosc-oszac', 'value'),
    State('input-rok', 'value')
)
def save_form(n_clicks, nazwa_ostoi, nazwa_polska, status, liczba_par_min, liczba_par_max, dokladnosc_oszac, rok):
    if n_clicks is not None:
        # Zapis danych do pliku CSV
        data = {
            'Nazwa ostoi': [nazwa_ostoi],
            'Nazwa polska': [nazwa_polska],
            'Status': [status],
            'Liczba par (min)': [liczba_par_min],
            'Liczba par (max)': [liczba_par_max],
            'Dokładność oszacowania': [dokladnosc_oszac],
            'Rok': [rok]
        }
        df = pd.DataFrame(data)
        file_exists = os.path.isfile('formularz_dane.csv')

        # Dodaj nagłówki tylko, gdy plik nie istnieje
        df.to_csv('formularz_dane.csv', mode='a', header=not file_exists, index=False)

        # Odczyt danych z pliku CSV, aby wyświetlić w tabeli
        df_all = pd.read_csv('formularz_dane.csv')

        # Tworzenie tabeli do wyświetlania
        table = dt.DataTable(
            data=df_all.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df_all.columns],
            style_table={'width': '80%', 'margin': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '10px'},
            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
        )

        return 'Dane zapisane pomyślnie!', table

    # Jeśli jeszcze nie było kliknięcia, nie wyświetlaj tabeli
    return '', html.Div()
