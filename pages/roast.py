import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__)

roastlog = pd.read_csv("https://raw.githubusercontent.com/DuaneIndustries/CoffeeRoasteryDash/main/Roastlog.csv")

roastlog['Colombia-1'] = roastlog['Colombia-1'].astype('int')
roastlog['Colombia-2'] = roastlog['Colombia-2'].astype('int')
roastlog['Ethiopia-1'] = roastlog['Ethiopia-1'].astype('int')
roastlog['Ethiopia-2'] = roastlog['Ethiopia-2'].astype('int')
roastlog['Ethiopia-3'] = roastlog['Ethiopia-3'].astype('int')
roastlog['Brazil-1'] = roastlog['Brazil-1'].astype('int')
roastlog['Brazil-2'] = roastlog['Brazil-2'].astype('int')
roastlog['RTime'] = roastlog['RTime'].astype('int')


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
                  paper_bgcolor='#353839',
                  plot_bgcolor='linen',
                  font_color='linen')

layout = html.Div(
    [
        html.Br(),
        dcc.Graph(figure=fig,style={"border" : "2px linen solid"})
        ])

