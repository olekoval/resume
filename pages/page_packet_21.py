import dash_bootstrap_components as dbc
import dash
from dash import html


dash.register_page(__name__,
                   path='/portfolio/page-packet_21',
                   name="Пацієнти з ВІЛ та діагнозом B20"
                   )


layout = dbc.Container(
    html.Div([
    html.H1('This is page_packet_21 page'),
    html.Div('This is page_packet_21 page content.')
    ])
    )    
