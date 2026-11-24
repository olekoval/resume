import dash
from dash import html, dcc


dash.register_page(__name__,
                   path='/portfolio'
                   )

def layout():
    return  html.Div([
        html.H1('This is Portfolio page'),
        html.Div('This is Portfolio page content.'),
        html.Div([
            html.Div(
                dcc.Link(page['name'], href=page["path"]))
                for page in dash.page_registry.values() 
                if page["path"].startswith('/portfolio/')
          ])
    ])
