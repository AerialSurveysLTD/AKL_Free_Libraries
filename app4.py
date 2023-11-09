import dash
import dash_leaflet as dl
import dash.dcc as dcc
import dash.html as html
from dash.dependencies import Input, Output
import fiona
import geopandas as gpd
import json

zipfile = "zip://D:/DATA/Scripting_App_WestHealth/pydataglobal-2021/data/cb_2018_us_state_20m.zip"
states = gpd.read_file(zipfile)

layer = dl.GeoJSON(id='borders', data=json.loads(states.to_json()),zoomToBoundsOnClick=True)

app = dash.Dash()

app.layout = html.Div([
    dl.Map([layer, dl.TileLayer()],
           center=[39, -98],
           zoom=4,
           style={
               'width': '1000px',
               'height': '500px'
           }),
    html.Button("Click Me!", id='btn')

])


@app.callback(Output('borders', 'data'), Input('btn', 'n_clicks'))
def filter(input_):
    if input_ and (input_ % 2 == 1):
        return json.loads(states[states.STATEFP == '06'].to_json())
    else:
        return json.loads(states.to_json())

app.run_server(debug = True)