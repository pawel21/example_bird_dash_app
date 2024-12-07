import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import sqlite3
import plotly.express as px

# Stylizacja
styles = {
    "container": {
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "justifyContent": "center",
        "height": "100vh",
        "backgroundColor": "#f8f9fa"
    },
    "title": {"fontSize": "3em", "marginBottom": "0.5em"},
    "description": {"fontSize": "1.5em", "marginBottom": "1em"},
    "button": {
        "fontSize": "1.2em",
        "padding": "10px 20px",
        "color": "white",
        "backgroundColor": "#007bff",
        "border": "none",
        "borderRadius": "5px",
        "cursor": "pointer",
        "textDecoration": "none"
    }
}

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)

# Layout aplikacji
app.layout = html.Div([
    #html.H1("Witamy w naszej aplikacji!", style=styles["title"]),
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Witamy", href="/")),
            dbc.NavItem(dbc.NavLink("Tabela i Wykres", href="/table")),
            dbc.NavItem(dbc.NavLink("Formularz", href="/form")),
        ],
        brand="IBA",
        color="Green",
        dark=True,
    ),
    html.Div(id='page-content')
])


# Layout podstrony z tabelą i wykresem
table_page = html.Div([
    html.H2("Dane z bazy"),
    dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in ['id', 'name', 'value']], data=[]),
    #dcc.Graph(id='graph'),
    dbc.Button("Odśwież", id='refresh-button', color='primary', className='mt-2')
])

welcome_page = html.Div([
    html.H2("Witamy")
])

# Funkcja generująca stronę formularza
def form_page(options, title="Formularz"):
    return html.Div([
        html.H1(title, style={"textAlign": "center", "marginBottom": "20px"}),
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": option, "value": option} for option in options],
            placeholder="Wybierz opcję",
            style={"width": "50%", "margin": "0 auto", "marginBottom": "20px"}
        ),
        html.Button(
            "Prześlij",
            id="submit-button",
            n_clicks=0,
            style={
                "display": "block",
                "margin": "0 auto",
                "padding": "10px 20px",
                "fontSize": "16px",
                "backgroundColor": "#007bff",
                "color": "white",
                "border": "none",
                "borderRadius": "5px",
                "cursor": "pointer"
            }
        ),
        html.Div(id="output", style={"textAlign": "center", "marginTop": "20px", "fontSize": "18px"})
    ])

# Callback obsługujący wynik formularza
@app.callback(
    Output("output", "children"),
    Input("dropdown", "value"),
    Input("submit-button", "n_clicks")
)
def update_output(selected_option, n_clicks):
    if n_clicks > 0:
        if selected_option:
            return f"Wybrano: {selected_option}"
        else:
            return "Proszę wybrać opcję przed przesłaniem."
    return ""

# Obsługa routingu
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/form':
        return form_page(["Opcja 1", "Opcja 2", "Opcja 3"], title="Formularz")
    if pathname == '/table':
        return table_page
    else:
        return welcome_page

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run_server(debug=True)
