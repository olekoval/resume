import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import plotly.express as px
import polars as pl
from utils.data_loader import dataset_loader

# Directory containing the dataset files to read for packet_21
base_lf = dataset_loader("packet_21") # turn DataFrame into LazyFrame

area = (
        base_lf.select(pl.col("residence_area"))
        .unique()
        .sort("residence_area")
        # Execute the lazy query plan and materialize the DataFrame
        .collect()
        .to_series()
        .to_list()
        )


dash.register_page(__name__,
                   path='/portfolio/page-packet_21',
                   name="Пацієнти з ВІЛ та діагнозом B20"
                   )

layout = dbc.Container(
        children=[
            html.Div([
                html.H1('This is page_packet_21 page'),
                html.Div('This is page_packet_21 page content.')
                ]),
            dbc.Tabs(active_tab="graph-tab",
                children=[
                    dbc.Tab(label="Графік",
                            tab_id="graph-tab",
                            active_label_class_name="bg-primary text-white",
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                               options=area,
                                               value=area, # All values selected by default
                                               id='areas',
                                               closeOnSelect=False,
                                               multi=True
                                               ), 
                                            width=4),
                                        dbc.Col(dcc.Graph(id="main-chart"), width=8),
                                    ]),
                                #dbc.Row(
                                    #[
                                        #dbc.Col(dcc.Graph(id="sub-chart"), width=10),
                                    #]),
                                ]
                            ),
                    dbc.Tab(label="Опис",
                            tab_id="description-tab"),
                    ])
            ]
    )    


@callback(
        Output('main-chart', 'figure'),
        Input('areas', 'value')
)
def update_area(selected_areas):
    df = (
            base_lf # LazyFrame loaded at the start of the script
            .filter(pl.col("residence_area").is_in(selected_areas or area))
            .group_by("residence_area")
            .agg(
                pl.col("edrpou").n_unique().alias("edrpou_count"),
                pl.col("patient_id").n_unique().alias("patient_count"),
                pl.col("event_id").count().alias("event_count")
            )
            .sort("residence_area")
            .collect()
    )
    fig = px.scatter(
        df,
        x="patient_count",
        y="edrpou_count",
        size="event_count",
        color="residence_area",
        hover_name="residence_area",
        size_max=60,
        labels={
            "patient_count": "Кількість пацієнтів",
            "edrpou_count": "Кількість закладів (ЄДРПОУ)",
            "event_count": "Кількість подій",
            "residence_area": "Область",
        },
    )
    fig.update_layout(legend_title_text="Область")
    return fig
