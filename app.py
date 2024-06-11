import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data from the CSV file
df = pd.read_csv('data_test.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions=True

# Layout for the main menu
menu_layout = html.Div([
    html.H1("IBA baza danych"),
    #html.Label("Wybierz stronę:"),
    html.Br(),
    dcc.Link('Tabela', href='/table'),
    html.Br(),
    dcc.Link('Wykres', href='/plot'),
    html.Br(),
    dcc.Location(id='url', refresh=False),
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
    html.Label("Wybierz nazwę polską:"),
    dcc.Dropdown(
        id='nazwa_polska_dropdown',
        options=[{'label': i, 'value': i} for i in df['nazwa_polska'].unique()],
        multi=True
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
        id='nazwa_polska_dropdown_bar_plot',
        options=[{'label': i, 'value': i} for i in df['nazwa_polska'].unique()],
        value='Bielik'
    ),
    dcc.Graph(id='bar-graph'),
    dcc.Link('Powrót do menu', href='/')
])

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
    else:
        return html.Div("Wybierz stronę z menu powyżej.")

# Callback for updating the bar graph
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('nazwa_ostoi_dropdown_bar_plot', 'value'),
     Input('nazwa_polska_dropdown_bar_plot', 'value')]
)
def update_bar(selected_nazwa_ostoi, selected_nazwa_polska):
    filtered_df = df.copy()
    if selected_nazwa_ostoi:
        filtered_df = filtered_df[filtered_df['nazwa_ostoi'].isin([selected_nazwa_ostoi])]

    if selected_nazwa_polska:
        filtered_df = filtered_df[filtered_df['nazwa_polska'].isin([selected_nazwa_polska])]

    fig = px.bar(filtered_df, x="rok", y="liczba_par_min")

    # Customize x-axis title and font size
    fig.update_layout(
        xaxis_title="Rok",
        xaxis=dict(title_font=dict(size=18)),
        yaxis_title="Liczba Par Min",
        yaxis=dict(title_font=dict(size=18))
    )
    return fig

# Callback for updating the table
@app.callback(
    Output('tabela_div', 'children'),
    [Input('nazwa_ostoi_dropdown', 'value'),
     Input('nazwa_polska_dropdown', 'value')]
)
def update_table(selected_nazwa_ostoi, selected_nazwa_polska):
    filtered_df = df.copy()
    if selected_nazwa_ostoi:
        filtered_df = filtered_df[filtered_df['nazwa_ostoi'].isin(selected_nazwa_ostoi)]

    if selected_nazwa_polska:
        filtered_df = filtered_df[filtered_df['nazwa_polska'].isin(selected_nazwa_polska)]

    return html.Div([
        html.H2("Wyniki filtrowania:"),
        dash.dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in filtered_df.columns],
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

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
