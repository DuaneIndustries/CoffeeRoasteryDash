import dash
import dash_bootstrap_components.themes
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import pandas as pd
import plotly
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


green = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/CoffeeRoasteryDash/main/GreenInventory.csv")
roastlog = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/CoffeeRoasteryDash/main/Roastlog.csv")
wb = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/CoffeeRoasteryDash/main/WholeBeanInventory.csv")
rcpie = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/CoffeeRoasteryDash/main/rcpie.csv")




rcpie['Lbs'] = rcpie['Lbs'].astype('int')

wb['Qty (Lbs)'] = wb['Qty (Lbs)'].astype('int')
wb['Qty Units (12oz bags)'] = wb['Qty Units (12oz bags)'].astype('int')
wb['Sales-Daily'] = wb['Sales-Daily'].astype('int')
wb['Sales-Weekly'] = wb['Sales-Weekly'].astype('int')
wb['Sales-Monthly Forecast)'] = wb['Sales-Monthly Forecast)'].astype('int')

roastlog['Colombia-1'] = roastlog['Colombia-1'].astype('int')
roastlog['Colombia-2'] = roastlog['Colombia-2'].astype('int')
roastlog['Ethiopia-1'] = roastlog['Ethiopia-1'].astype('int')
roastlog['Ethiopia-2'] = roastlog['Ethiopia-2'].astype('int')
roastlog['Ethiopia-3'] = roastlog['Ethiopia-3'].astype('int')
roastlog['Brazil-1'] = roastlog['Brazil-1'].astype('int')
roastlog['Brazil-2'] = roastlog['Brazil-2'].astype('int')
roastlog['RTime'] = roastlog['RTime'].astype('int')


green['Bin'] = green['Bin'].astype('int')
green['Lbs.'] = green['Lbs.'].astype('int')
green['25% Full'] = green['25% Full'].astype('int')
green['50% Fill'] = green['50% Fill'].astype('int')
green['75% Full'] = green['75% Full'].astype('int')
green['Green Bin Capacity '] = green['Green Bin Capacity '].astype('int')

#Line Graph for Roasted Coffee
fig = go.Figure()

# Create and style traces
fig.add_trace(go.Scatter(x=roastlog['RTime'], y=roastlog['Colombia-1'], name='Colombia Batch 1',
                         line=dict(color='indianred', width=4)))
fig.add_trace(go.Scatter(x=roastlog['RTime'], y=roastlog
['Ethiopia-1'], name = 'Ethiopia Batch 1',
                         line=dict(color='goldenrod', width=4)))
fig.add_trace(go.Scatter(x=roastlog['RTime'], y=roastlog['Brazil-1'], name='Brazil Batch 1',
                         line=dict(color='darkslategray', width=4)
))
fig.add_trace(go.Scatter(x=roastlog['RTime'], y=roastlog['Colombia-2'], name='Colombia Batch 2',
                        line = dict(color='indianred', width=4, dash='dot')))
fig.add_trace(go.Scatter(x=roastlog['RTime'], y=roastlog['Ethiopia-2'], name='Ethiopia Batch 2',
                         line = dict(color='goldenrod', width=4, dash='dot')))
fig.add_trace(go.Scatter(x=roastlog['RTime'], y=roastlog['Brazil-2'], name='Brazil Batch 2',
                        line=dict(color='darkslategray', width=4, dash='dot')))

# Edit the layout
fig.update_layout(title='Daily Roast Log',
                  title_x=0.45,
                   xaxis_title='Roast Time (Mins)',
                   yaxis_title='Temperature (degrees F)',
                  paper_bgcolor='black',
                  plot_bgcolor='linen',
                  font_color='linen')

#bar chart for whole bean
figb = go.Figure(go.Bar(x=wb['CoffeeType'], y=wb['Qty Units (12oz bags)'], name='Roasted Inventory',marker = dict(color='dimgrey')))
figb.add_trace(go.Bar(x=wb['CoffeeType'], y=wb['Sales-Daily'], name='Daily Sales', opacity=.5, marker = dict(color='burlywood')))
figb.add_trace(go.Bar(x=wb['CoffeeType'], y=wb['Sales-Weekly'], name='Weekly Sales', opacity=.5, marker = dict(color='darkred')))
figb.add_trace(go.Bar(x=wb['CoffeeType'], y=wb['Sales-Monthly Forecast)'], name='Monthly Sales', opacity=.5, marker = dict(color='moccasin',pattern_shape='/')))

figb.update_layout(title='Roasted Inventory',
                   title_x=0.45,
                   barmode='overlay',
                   xaxis_title='Coffee Type',
                   yaxis_title='Units',
                   paper_bgcolor='black',
                   plot_bgcolor='linen',
                   font_color='linen')





app = dash.Dash(__name__,external_stylesheets=[dash_bootstrap_components.themes.CYBORG],
              meta_tags=[{'name':'viewport',
                          'content': 'width=device-width, intial-scale=1.0'}]
                )
#for deploying
server = app.server

# LAYOUT
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1(' - Roasting Terminal - ',
                        style={'textAlign' : 'center','color' : 'Linen'},
                        className='text-m-center mb-m-4'),
                width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Checklist(id='my-checklist', value=['Colombia','Brazil','Ethiopia','Sumatra'],
                inline=True,
                className="me-1",
                style={'color' : 'linen'},
                inputStyle={'margin-left': '10px'},
                options=[{'label': x, 'value': x}
                            for x in rcpie['Coffee'].unique()]),
            dcc.Graph(id='pie-fig',figure={}),
        html.Br(),
        ], width={'size' : 4}),
        dbc.Col([
            html.Br(),
            dcc.Graph(figure=fig)
        ], width={'size' : 8})
]),
    dbc.Row([
        dbc.Col([
            html.Label(['Bin Number'], style={'font-weight': 'bold', 'color':'linen'}),
            dcc.Dropdown(
                id='x-axis-dropdown',
                style={'backgroundColor' : 'linen'},
                options=[{'label': i, 'value': i} for i in green['Bin'].unique()],
                value=green['Bin'].iloc[0]),
            dcc.Graph(id='green-bar', figure={})
        ], width={'size': 4})
        ,
    dbc.Col([
            # dcc.Checklist(id='my-checklist2', value=['Sales-Daily','Sales-Weekly','Sales-Monthly Forecast)'],
            #     inline=True,
            #     className="mx-1",
            #     options=[{'label': x, 'value': x}
            #                 for x in wb.columns.unique()]),
        html.Br(),
        html.Br(),
        dcc.Graph(figure=figb)
        ], width={'size' : 8}),


]),
])

# Callback section: connecting the components
# ************************************************************************
# Line chart - Single
# @app.callback(
#     Output('rev-fig', 'figure'),
#     Input('my-dpdn', 'value')
# )
# def update_graph(year_slctd):
#     dff = rev[rev["Year"]==year_slctd]
#
#
# fig.show()
#     return (barchart)

# Pie Chart - Roast Completion
@app.callback(
    Output('pie-fig', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(cat_slctd):
    dff = rcpie[rcpie['Coffee'].isin(cat_slctd)]
    pie1 = px.pie(dff, values='Lbs', names='Status', title='Roast Completion', hole=.5, color_discrete_sequence=px.colors.sequential.RdBu)
    pie1.update_layout(paper_bgcolor='black',
                       title_x=0.5,
                       plot_bgcolor='linen',
                       font_color='linen')
    return (pie1)


# PROJECT HOURS BAR
@app.callback(
    Output('green-bar', 'figure'),
    Input('x-axis-dropdown', 'value')
)

def update_figure(selected_x_value):
    filtered_df = green[green['Bin'] == selected_x_value]
    # fig1 = px.bar(filtered_df, x='Bin', y=['25% Full','50% Fill','75% Full','Green Bin Capacity '],facet_col_spacing=1, title='Green Inventory', barmode='overlay', hover_data=["Type"])
    # fig1.update_layout(title='Green Inventory',
    #                xaxis_title='Bin Number',
    #                yaxis_title='Amount Lbs',
    #               paper_bgcolor='black',
    #                    font_color='ivory')
    #
    # return fig1

    figx = go.Figure(go.Bar(x=filtered_df['Bin'], y=filtered_df['Green Bin Capacity '], name='Green Bin Capacity',marker = dict(color='dimgrey', pattern_shape='-')))
    figx.add_trace(go.Bar(x=filtered_df['Bin'],y=filtered_df['75% Full'], name='75& Full', opacity=1, marker = dict(color='green')))
    figx.add_trace(go.Bar(x=filtered_df['Bin'], y=filtered_df['50% Fill'], name='50% Full', opacity=.5, marker = dict(color='goldenrod')))
    figx.add_trace(go.Bar(x=filtered_df['Bin'], y=filtered_df['25% Full'], name='25% Full', opacity=.5, marker = dict(color='firebrick',pattern_shape='/')))

    figx.update_layout(barmode='overlay',
                       title='Green Inventory',
                       title_x=0.5,
                       xaxis_title='Bin Number',
                       yaxis_title='Amount Lbs',
                       paper_bgcolor='black',
                       plot_bgcolor='linen',
                       font_color='linen')
    return figx



if __name__ == '__main__' :
    app.run_server(debug=True)

