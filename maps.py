import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from dash import callback
from dash.dependencies import Input, Output
from dash import html
import dash


#dash.register_page(__name__)



df = pd.read_csv("mapa_test_IBA.csv")


def foo():
    print("Foo")


@callback(
    Output('map-graph', 'figure'),
     [Input('nazwa_polska_map', 'value'),
      Input('status_map', 'value'),
      Input("rok_map", 'value')
     ]
)
def update_map(selected_nazwa_polska, selected_status, selected_rok):

    filtered_df = df.copy()
    df_ptak = filtered_df[(filtered_df['nazwa_polska'] == selected_nazwa_polska) &
                     (filtered_df['status'] == selected_status) &
                     (filtered_df['rok_start'] <= selected_rok) &
                     (filtered_df['rok_end'] >= selected_rok)]
    df_ptak = df_ptak[~df_ptak['liczba_par_max'].isna()]


    if selected_nazwa_polska:
        filtered_df = filtered_df[filtered_df['nazwa_polska'].isin([selected_nazwa_polska])]

    print(filtered_df)

    fig = go.Figure()
    # Add points from example_df
    fig.add_trace(go.Scattermapbox(
        lon=df_ptak['DEC'],
        lat=df_ptak['RA'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=15,
            color=df_ptak['liczba_par_max'],
            colorscale='Viridis',
            showscale=True
        ),
        text=df_ptak['nazwa_ostoi'],
        customdata=df_ptak['liczba_par_max'],
        hovertemplate='<b>%{text}</b><br>Max Pairs: %{customdata}<extra></extra>'
    ))

    # Update layout for better visualization
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": 52, "lon": 19},  # Center the map on Poland
        mapbox_zoom=5,
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend=False  # Show legend
    )

    return fig

@callback(
    Output('tabela_mapa', 'children'),
    [Input('nazwa_polska_map', 'value'),
     Input('status_map', 'value'),
     Input('rok_map', 'value')]
)
def update_table_map(selected_nazwa_polska, selected_status, selected_rok):
    filtered_df = df.copy()
    if selected_nazwa_polska and selected_status and selected_rok:
        df_ptak = filtered_df[(filtered_df['nazwa_polska'] == selected_nazwa_polska) &
                         (filtered_df['status'] == selected_status) &
                         (filtered_df['rok_start'] <= selected_rok) &
                         (filtered_df['rok_end'] >= selected_rok)]
        df_ptak = df_ptak[~df_ptak['liczba_par_max'].isna()]

        return html.Div([
            html.H2("Wyniki filtrowania:"),
            dash.dash_table.DataTable(
                data=filtered_df.to_dict('records'),
                # Show first 13 columns, skip rok_poczatek i rok_end
                columns=[{'name': i, 'id': i} for i in df_ptak.columns[:13]],
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
