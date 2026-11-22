import dash
import dash_bootstrap_components as dbc
from dash import Dash, html


app = Dash(__name__, 
           use_pages=True,
           external_stylesheets=[dbc.themes.FLATLY]
           )

server = app.server

navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Резюме", href="/", active="exact")),
            dbc.NavItem(dbc.NavLink("Портфоліо", href="/portfolio", active="exact")),
            ],
        brand="Олег Коваль",
        brand_href="/",
        color="primary",
        dark=True,
        expand="md",
        className="shadow-sm mb-3",
        )

app.layout = html.Div([
    navbar,
    dbc.Container(
    dash.page_container
    ),
])

if __name__ == '__main__':
    app.run(debug=True)
