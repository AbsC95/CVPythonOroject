import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  


app = Dash(__name__)

# -- (importing csv into pandas)

df = pd.read_csv("all-states-history.csv")
min_val = df['death'].min(),
max_val = df['death'].max()



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Abs web app", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                      {'label':'AZ','value': 'AZ'},
                      {'label':'CA','value': 'CA'},
                      {'label':'NY','value': 'NY'},
                      {'label':'FL','value': 'FL'},
                      {'label':'MA','value': 'MA'}],
                 multi=True,
                 #value=2015,
                 style={'width': "90%"}
                 ),
    
    dcc.RangeSlider(
        id='my-range-slider',
        min= min_val,
        max= max_val,
        value = [min_val, max_val],
        step=1000,
        ),
    

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_map', figure={})
    

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_map', component_property='figure')],
    
    [Input(component_id='slct_year', component_property='value'),
    Input(component_id='my-range-slider', component_property='value')]

)
def update_graph(option_selected,value_selected):
    #print(option_selected)
    #print(type(option_selected))

    container = "The state chosen by user was: {}".format(option_selected)
 
    dff = df.copy()
    dff =  dff[dff['death'].isin(value_selected)]
    
    if option_selected is not None:
        dff = dff[dff["state"].isin(option_selected)]
   


    

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state',
        scope="usa",
        color='death',
        hover_data=['state'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        
        template='plotly_dark'
    )


    return (container,fig)


# ------------------------------------------------------------------------------
if __name__ == '__main__':

    app.run_server(
        port=8050,
        host='0.0.0.0'
    )


