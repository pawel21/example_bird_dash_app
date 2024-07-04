import pandas as pd
import plotly.express as px
import sqlite3
from dash import callback
from dash.dependencies import Input, Output
#import dash


#dash.register_page(__name__)


# Establish a connection to the SQLite database
conn = sqlite3.connect('database_kryteria_after_preprocesing.db')

# Read the entire table into a DataFrame
df= pd.read_sql_query("SELECT * FROM kryteria", conn)

# Close the connection
conn.close()

def foo():
    print("Foo")


@callback(
    Output('map-graph', 'figure'),
     Input('nazwa_polska_map', 'value')
)
def update_map(selected_nazwa_polska):
    filtered_df = df.copy()

    if selected_nazwa_polska:
        filtered_df = filtered_df[filtered_df['nazwa_polska'].isin([selected_nazwa_polska])]

    print(filtered_df)
    foo()
    # Przykładowe dane
    df_map_example = pd.DataFrame({
        'RA': [52.1, 52.2, 52.3],
        'DEC': [21.0, 21.1, 21.2],
        'index': ['Point 1', 'Point 2', 'Point 3']
    })

    # Tworzenie wykresu scatter mapbox
    fig = px.scatter_mapbox(
        df_map_example ,
        lat="RA",
        lon="DEC",
        hover_name="index",
        zoom=6,
        center={"lat": 52.237049, "lon": 21.017532},
        mapbox_style="open-street-map"
    )

    return fig
