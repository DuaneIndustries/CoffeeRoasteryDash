import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SLATE],use_pages=True)
server=app.server
app.config.suppress_callback_exceptions=True
sidebar=dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"],className="ms-2",style={'textAlign' : 'center', 'color':'linen'}),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className="btn-outline-light",
)


app.layout = dbc.Container([
        dbc.Row([
        dbc.Col(html.Div("Roasting Terminal",
                 style={'fontSize':50,'textAlign' : 'center','color' : 'linen'},
                 className='text-m-center mb-m-4')),
        ]),
        # html.Div([
        #     dcc.Link(page['name']+" | ",href=page['path'])
        #     for page in dash.page_registry.values()
        # ]),
        html.Hr(),
    dbc.Row(
        [
            dbc.Col([
                sidebar
            ],xs=4,sm=4,md=2,lg=2,xl=2,xxl=2),
            dbc.Col(
                [
                    dash.page_container
                ],xs=8,sm=8,md=10,lg=10,xl=10,xxl=10)


        ]
    )

    ], fluid=True)


if __name__ == '__main__' :
    app.run_server(debug=True)