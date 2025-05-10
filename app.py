import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

from maps import update_map
from form import form_layout

# Establish a connection to the SQLite database
conn = sqlite3.connect('database_kryteria_after_preprocesing.db')

# Read the entire table into a DataFrame
df = pd.read_sql_query("SELECT * FROM kryteria", conn)
df_mapa_test = pd.read_csv("mapa_test_IBA.csv")


# Close the connection
conn.close()


# Initialize the Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions=True



# Layout for the main menu
menu_layout = html.Div([
    html.H1("IBA baza danych"),
    #html.Label("Wybierz stronę:"),
    html.Div([
        dcc.Link('Tabela', href='/table'),
        html.Br(),
        dcc.Link('Wykres', href='/plot'),
        html.Br(),
        dcc.Link('Mapa', href='/map'),
        html.Br(),
        dcc.Link('Formularz', href='/form'),
        html.Br(),
        dcc.Link('Nowe dane', href='/new_data'),
    ], style={"display":'flex', 'gap':'10px'}),
    html.Br(),
    dcc.Location(id="url", refresh=False),
    html.Div(id='page-content')
])

# Layout for the table page
table_layout = html.Div([
    html.H1("Tabela"),
    html.Label("Wybierz nazwę ostoi:"),
    dcc.Dropdown(
        id='nazwa_ostoi_dropdown',
        options=[{'label': i, 'value': i} for i in df['nazwa_ostoi'].unique()],
        multi=True
    ),
    html.Br(),
    html.Label("Wybierz nazwę polską:"),
    dcc.Dropdown(
        id='nazwa_polska_dropdown',
        options=[{'label': i, 'value': i} for i in df['nazwa_polska'].unique()],
        multi=True
    ),
    html.Br(),
    html.Label("Wybierz rok:"),
    dcc.Dropdown(
        id='rok_dropdown',
        options=[i for i in range(1990, 2020)],
        multi=True
    ),
    html.Br(),
    # TO DO add in table filter
    html.Label("Wybierz rok poczatkowy:"),
    dcc.Dropdown(
        id='rok_start',
        options=[i for i in range(1990, 2025)],
        multi=False
    ),
    html.Br(),
    html.Label("Wybierz rok końcowy:"),
    dcc.Dropdown(
        id='rok_end',
        options=[i for i in range(1990, 2025)],
        multi=False
    ),
    html.Div(id='tabela_div'),
    dcc.Link('Powrót do menu', href='/')
])


# Layout for the plot page
plot_layout = html.Div([
    html.H1("Wykres"),
    html.Label('Wybierz ostoje:'),
    dcc.Dropdown(
        id='nazwa_ostoi_dropdown_bar_plot',
        options=[{'label': i, 'value': i} for i in df['nazwa_ostoi'].unique()],
        value='Zalew Szczeciński'
    ),
    html.Label('Wybierz nazwę ptaka:'),
    dcc.Dropdown(
        id='nazwa_polska_dropdown_bar_plot'
    ),
    html.Label('Wybierz status:'),
    dcc.Dropdown(
        id='status_dropdown_bar_plot'
    ),
    dcc.Graph(id='bar-graph'),
    dcc.Link('Powrót do menu', href='/')
])

map_layout = html.Div(
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'height': '100vh',
        'padding': 20
    },
    children=[
        html.H1("Mapa"),
        html.Div(
            style={
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
                'width': '100%',
                'margin-bottom': '20px'
            },
            children=[
                html.Div(
                    style={'margin': '0 10px'},
                    children=[
                        html.Label('Wybierz nazwę ptaka:'),
                        dcc.Dropdown(
                            id='nazwa_polska_map',
                            options=[{'label': i, 'value': i} for i in df_mapa_test['nazwa_polska'].unique()],
                            style={'width': '200px'},
                            value="bielik"
                        )
                    ]
                ),
                html.Div(
                    style={'margin': '0 10px'},
                    children=[
                        html.Label('Wybierz status:'),
                        dcc.Dropdown(
                            id='status_map',
                            style={'width': '200px'}
                        )
                    ]
                ),
                html.Div(
                    style={'margin': '0 10px'},
                    children=[
                        html.Label('Wybierz rok:'),
                        dcc.Dropdown(
                            id='rok_map',
                            options=[i for i in range(1990, 2020)],
                            style={'width': '200px'}
                        )
                    ]
                ),
                html.Div(
                    style={'margin': '0 10px'},
                    children=[
                        html.Label('Wybierz liczbę:'),
                        dcc.Dropdown(
                            id='mod_map',
                            options=['liczba_par_min', 'liczba_par_max'],
                            value='liczba_par_min',
                            style={'width': '200px'}
                        )
                    ]
                )
            ]
        ),
        dcc.Graph(id='map-graph', style={'width': '60%', 'height': '50vh'}),
        html.Br(),
        html.Div(id='tabela_mapa', style={'width': '60%', 'height': '25vh', 'overflowY': 'scroll', 'margin': '10px auto'}),
        dcc.Link('Powrót do menu', href='/')
    ]
)

# Layout for the new data page
# Define the layout for the new_data page
new_data_layout = html.Div([
    dcc.Location(id='url_new_data', refresh=False),  # Detect page load
    html.H1("Tabela"),
    html.Br(),

    html.H2("Wyniki filtrowania:"),
    dash_table.DataTable(id='data-table',  # Table with dynamic data
                         style_table={'width': '80%', 'margin': 'auto'},
                         style_cell={'textAlign': 'center', 'padding': '10px'},
                         style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
                         ),
    dcc.Link('Powrót do menu', href='/')
])

@app.callback(
    Output('data-table', 'data'),
    Output('data-table', 'columns'),
    Input('url_new_data', 'pathname')  # Trigger when the user navigates to the page
)
def load_data(pathname):
    if pathname == "/new_data":  # Ensure it runs only when entering this page
        try:
            df_all = pd.read_csv('formularz_dane.csv')
            columns = [{"name": i, "id": i} for i in df_all.columns]
            return df_all.to_dict('records'), columns
        except Exception as e:
            return [], []  # Return empty data if file not found
    return dash.no_update, dash.no_update  # Do nothing if not on this page

@app.callback(
    Output('nazwa_polska_dropdown_bar_plot', 'options'),
    Input('nazwa_ostoi_dropdown_bar_plot', 'value')
)
def update_dropdown_nazwa_ptaka_wykres(selected_ostoja):
    if selected_ostoja is None:
        return []
    return [{'label': i, 'value': i} for i in df['nazwa_polska'][df['nazwa_ostoi'] == selected_ostoja].unique()]

@app.callback(
    Output('status_dropdown_bar_plot', 'options'),
    [Input('nazwa_ostoi_dropdown_bar_plot', 'value'),
    Input('nazwa_polska_dropdown_bar_plot', 'value')]
)
def update_dropdown_status_ptaka_wykres(selected_ostoja, selected_nazwa_polska):
    if selected_ostoja is None:
        return []
    return [{'label': i, 'value': i} for i in df['status'][(df['nazwa_ostoi'] == selected_ostoja) & (df['nazwa_polska'] == selected_nazwa_polska)].unique()]

# Main layout
app.layout = menu_layout

# Callback for rendering the appropriate page
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/table':
        return table_layout
    elif pathname == '/plot':
        return plot_layout
    elif pathname == '/map':
        return map_layout
    elif pathname == "/form":
        return form_layout
    elif pathname == "/new_data":
        return new_data_layout
    else:
        return html.Div("Wybierz stronę z menu powyżej.")

# Callback for updating the bar graph
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('nazwa_ostoi_dropdown_bar_plot', 'value'),
     Input('nazwa_polska_dropdown_bar_plot', 'value'),
     Input('status_dropdown_bar_plot', 'value')]
)
def update_bar(selected_nazwa_ostoi, selected_nazwa_polska, selected_status):
    filtered_df = df.copy()
    if selected_nazwa_ostoi:
        filtered_df = filtered_df[filtered_df['nazwa_ostoi'].isin([selected_nazwa_ostoi])]

    if selected_nazwa_polska:
        filtered_df = filtered_df[filtered_df['nazwa_polska'].isin([selected_nazwa_polska])]

    if selected_status:
        filtered_df = filtered_df[filtered_df['status'].isin([selected_status])]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=filtered_df["rok"], y=filtered_df["liczba_par_min"], name="Liczba par minimum"))
    fig.add_trace(go.Bar(x=filtered_df["rok"], y=filtered_df["liczba_par_max"], name="Liczba par maksimum"))
    # Customize x-axis title and font size
    fig.update_layout(
        xaxis_title="Rok",
        xaxis=dict(title_font=dict(size=18)),
        yaxis_title="Liczba Par",
        yaxis=dict(title_font=dict(size=18))
    )
    return fig

# Callback for updating the table
@app.callback(
    Output('tabela_div', 'children'),
    [Input('nazwa_ostoi_dropdown', 'value'),
     Input('nazwa_polska_dropdown', 'value'),
     Input('rok_dropdown', 'value')]
)
def update_table(selected_nazwa_ostoi, selected_nazwa_polska, selected_rok):
    filtered_df = df.copy()
    if selected_nazwa_ostoi:
        filtered_df = filtered_df[filtered_df['nazwa_ostoi'].isin(selected_nazwa_ostoi)]

    if selected_nazwa_polska:
        filtered_df = filtered_df[filtered_df['nazwa_polska'].isin(selected_nazwa_polska)]

    if selected_rok:
        filtered_df = filtered_df[filtered_df.apply(
        lambda row: any((row['rok_start'] <= year) &
        (row['rok_end'] >= year) for year in selected_rok), axis=1)]

    return html.Div([
        html.H2("Wyniki filtrowania:"),
        dash.dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            # Show first 13 columns, skip rok_poczatek i rok_end
            columns=[{'name': i, 'id': i} for i in filtered_df.columns[:13]],
            style_table={'overflowX': 'auto'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '5px'
            }
        )
    ])


@app.callback(
    Output('status_map', 'options'),
    Input('nazwa_polska_map', 'value')
)
def update_dropdown_status_ptaka_wykres(selected_nazwa_polska):
    # Filtruj DataFrame na podstawie wybranej wartości
    filtered_df = df_mapa_test[df_mapa_test['nazwa_polska'] == selected_nazwa_polska]

    # Tworzenie listy unikalnych wartości i przekształcenie ich w format słownikowy dla opcji dropdown
    options = [{'label': i, 'value': i} for i in filtered_df['status'].unique()]

    return options





if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
