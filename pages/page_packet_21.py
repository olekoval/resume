import dash_bootstrap_components as dbc
import dash
from dash import html


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
                            active_label_class_name="bg-primary text-white "
                            ),
                    dbc.Tab(label="Опис",
                            tab_id="description-tab"),
                    ])
            ]
    )    
