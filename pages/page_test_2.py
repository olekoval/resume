import dash
from dash import html


dash.register_page(__name__,
                   path='/portfolio/page-test2'
                   )

layout = html.Div([
    html.H1('This is page_test_2'),
    html.Div('This is page_test_2 page content.')
    ])
