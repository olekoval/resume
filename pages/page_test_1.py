import dash
from dash import html


dash.register_page(__name__,
                   path='/portfolio/page-test1'
                   )


layout = html.Div([
    html.H1('This is page_test_1'),
    html.Div('This is page_test_1 page content.')
    ])
