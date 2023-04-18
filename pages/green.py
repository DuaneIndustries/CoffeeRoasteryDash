import dash
from dash import dcc, html, callback, Input,Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go


dash.register_page(__name__,path='/')


green = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/CoffeeRoasteryDash/main/GreenInventory.csv")
list = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/CoffeeRoasteryDash/main/GreenCoffeeList.csv")

green['Bin'] = green['Bin'].astype('int')
green['Lbs.'] = green['Lbs.'].astype('int')
green['25% Full'] = green['25% Full'].astype('int')
green['50% Fill'] = green['50% Fill'].astype('int')
green['75% Full'] = green['75% Full'].astype('int')
green['Green Bin Capacity '] = green['Green Bin Capacity '].astype('int')

card1 = dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("This is Text", className="card-title",id='card-id',style={'fontSize':30,'textAlign' : 'center','color' : 'linen'}),
                                        html.P("This is body text", className="card-text",id='body-text',style={'fontSize':15,'textAlign' : 'center','color' : 'linen'})
                                    ]
                                )
                            ]
                        )

card2 = dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P("This is Text", className="card-title",id='card-id2',style={'textAlign' : 'center','color' : 'linen'})
                                    ]
                                )
                            ]
                        )

button = dbc.Button("ORDER AT RED FOX COFFEE MERCHANTS",
                    color="primary",
                    href="https://redfoxcoffeemerchants.com/my-account/",
                    className='btn-danger',
                    style={'textAlign' : 'center','color' : 'linen','Align':'center'})



layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(['Bin Number'], style={'font-weight': 'bold', 'color':'linen'}),
                        dcc.Dropdown(
                            id='x-axis-dropdown',
                            style={'backgroundColor' : 'linen'},
                            options=[{'label': i, 'value': i} for i in green['Bin'].unique()],
                            value=green['Bin'].iloc[0])
                    ], xs=6, sm=6, md=4, lg=4, xl=4, xxl=4
                ),]),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='green-bar',figure={},style={"border" : "2px linen solid"})
                    ],xs=8, sm=8, md=6, lg=6, xl=6, xxl=6
                ),
                dbc.Col(
                    [
                      card1,
                      card2,
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        button
                    ],xs=4, sm=4, md=6, lg=6, xl=6, xxl=6
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dash_table.DataTable(
                            id='datatable-interactivity',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": True}
                                if i == "Start" or "End"
                                else {"name": i, "id": i, "deletable": False, "selectable": True}
                                for i in list.columns
                            ],
                            data=list.to_dict('records'),
                                        editable=False,
                                        filter_action="native",
                                        sort_action="native",
                                        sort_mode="single",
                                        column_selectable="multi",
                                        row_selectable="multi",
                                        row_deletable=False,
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action="native",
                                        page_current=0,
                                        page_size=20,
                                        style_cell={
                                            'minWidth': 95, 'maxWidth': 95, 'width': 95, "backgroundColor" : '#353839','color' : 'linen'},
                                style_cell_conditional=[
                                        {
                                            'if': {'column_id': c},
                                            'textAlign': 'left'
                                        } for c in ['ID','Name', 'Origin','warehouse', 'status','Status','Bag weight']
                                    ],
                                style_filter={"backgroundColor" : 'linen'},
                                    style_data={
                                        'whiteSpace': 'normal',
                                        'height': 'auto'}
                                                    )

                    ]
                )
            ]
        )
    ]
)


#
@callback(
    Output('green-bar', 'figure'),
    Input('x-axis-dropdown', 'value')
)
def update_figure(selected_x_value):
    filtered_df = green[green['Bin'] == selected_x_value]

    figx = go.Figure(go.Bar(x=filtered_df['Bin'], y=filtered_df['Green Bin Capacity '], name='Green Bin Capacity',marker = dict(color='dimgrey', pattern_shape='-')))
    figx.add_trace(go.Bar(x=filtered_df['Bin'],y=filtered_df['75% Full'], name='75& Full', opacity=1, marker = dict(color='green')))
    figx.add_trace(go.Bar(x=filtered_df['Bin'], y=filtered_df['50% Fill'], name='50% Full', opacity=.5, marker = dict(color='goldenrod')))
    figx.add_trace(go.Bar(x=filtered_df['Bin'], y=filtered_df['25% Full'], name='25% Full', opacity=.5, marker = dict(color='firebrick',pattern_shape='/')))

    figx.update_layout(barmode='overlay',
                       title='Green Inventory',
                       title_x=0.5,
                       xaxis_title='Bin Number',
                       yaxis_title='Amount Lbs',
                       paper_bgcolor='#353839',
                       plot_bgcolor='linen',
                       font_color='linen')
    return figx

@callback(
    Output('card-id','children'),
    Output('body-text','children'),
    Input('x-axis-dropdown', 'value')
)

def update_card(cardinfo):
    if cardinfo == 1:
        return ("Colombia","Aponte Village - Lot #0791")
    if cardinfo == 2:
        return ("Brazil","Fazenda Estate - Lot #3498")
    if cardinfo == 3:
        return ("Ethiopia", "Gera Estate - Lot # 3039")
    if cardinfo == 4:
        return ("Kenya", "Kagumo PB - Lot # 4567")
    if cardinfo == 5:
        return ("Sumatra", "Lintong - Lot# 7632")
    if cardinfo == 6:
        return ("Ethiopia - Decaf", "Modor Shantawene - Lot # 9008")


@callback(
    Output('card-id2','children'),
    Input('x-axis-dropdown', 'value')
)

def update_card(cardinfo):
    if cardinfo == 1:
        return ("1500 lbs | 250 lbs  scheduled for roast this week")
    if cardinfo == 2:
        return ("800 lbs | 300 lbs  scheduled for roast this week ")
    if cardinfo == 3:
        return ("1100 lbs | 150 lbs  scheduled for roast this week ")
    if cardinfo == 4:
        return ("1700 lbs | 500 lbs  scheduled for roast this week ")
    if cardinfo == 5:
        return ("323 lbs | 50 lbs  scheduled for roast this week ")
    if cardinfo == 6:
        return ("1005 lbs. | 100 lbs  scheduled for roast this week")
