import dash
from dash import dcc, html, callback, Input,Output
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

dash.register_page(__name__)

wb = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/CoffeeRoasteryDash/main/WholeBeanInventory.csv")

wb['Qty (Lbs)'] = wb['Qty (Lbs)'].astype('int')
wb['Qty Units (12oz bags)'] = wb['Qty Units (12oz bags)'].astype('int')
wb['Sales-Daily'] = wb['Sales-Daily'].astype('int')
wb['Sales-Weekly'] = wb['Sales-Weekly'].astype('int')
wb['Sales-Monthly Forecast)'] = wb['Sales-Monthly Forecast)'].astype('int')



layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Checklist(id='my-checklist2', value=['Daily Sales'],
                            inline=True,
                            className="mx-1",
                            inputStyle={'margin-left': '10px'},
                            options=['Daily Sales','Weekly Sales','Monthly Sales']),
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='i-chart',figure={},style={"border" : "2px linen solid"})
                    ], width=12
                )
            ]
        )

        ]
)

@callback(
    Output('i-chart', 'figure'),
    Input('my-checklist2', 'value')
)

def update_figure(selected_value):
    # filtered_df = wb[wb[['Qty Units (12oz bags)','Sales-Daily','Sales-Weekly','Sales-Monthly Forecast)']] == selected_value]
    filtered_df= wb

    figb = go.Figure(
        go.Bar(x=filtered_df['CoffeeType'], y=filtered_df['Qty Units (12oz bags)'], name='Roasted Inventory',
               marker=dict(color='dimgrey')))

    if 'Weekly Sales' in selected_value:
        figb.add_trace(
            go.Bar(x=filtered_df['CoffeeType'], y=filtered_df['Sales-Weekly'], name='Weekly Sales', opacity=.5,
                   marker=dict(color='darkred')))
    if 'Daily Sales' in selected_value:
        figb.add_trace(go.Bar(x=filtered_df['CoffeeType'], y=filtered_df['Sales-Daily'], name='Daily Sales', opacity=.5, marker = dict(color='burlywood')))

    if 'Monthly Sales' in selected_value:
        figb.add_trace(go.Bar(x=filtered_df['CoffeeType'], y=filtered_df['Sales-Monthly Forecast)'], name='Monthly Sales', opacity=.5, marker = dict(color='moccasin',pattern_shape='/')))

    figb.update_layout(title='Roasted Inventory',
                       title_x=0.45,
                       barmode='overlay',
                       xaxis_title='Coffee Type',
                       yaxis_title='Units (12oz bags)',
                       paper_bgcolor='#353839',
                       plot_bgcolor='linen',
                       font_color='linen',
                       )
    return figb