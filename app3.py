import dash
import dash_leaflet as dl
import dash.dcc as dcc
import dash.html as html
from dash.dependencies import Input, Output
import fiona
import pandas as pd
import geopandas as gpd
import json
import pyproj
from shapely.geometry import Point
from dash_extensions.javascript import arrow_function

# Create a GeoDataFrame from the XY coordinates in NZTM format
# Replace this with your actual GeoDataFrame creation
df = pd.read_csv("FreeLibraries2.csv")
# print(df)

gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df["LONGITUDE"], df["LATITUDE"], crs = 'EPSG:4326')
)
# gdf.crs = 'EPSG:4326'

# print(gdf)

# # Define the color mapping for the REGION categories
# color_mapping = {
#     "Auckland Central Little Libraries": "red",
#     "North Auckland": "blue",
#     "West Auckland" : "green",
#     "South Auckland" : "orange",
#     "East Auckland" : "yellow",
#     "Franklin & beginning of Waikato" : "purple",
# }

# # Add a new column for the point color based on the REGION category
# gdf["color"] = gdf["REGION"].map(color_mapping)

gdf['tooltip'] = gdf.LABEL

# Convert the GeoDataFrame to GeoJSON format
layer = dl.GeoJSON(id='free_libraries', data=json.loads(gdf.to_json(to_wgs84= True)), zoomToBoundsOnClick=True)
app = dash.Dash()
app.layout = html.Div([
    dl.Map([layer, dl.TileLayer()],
           center=[-36.8485, 174.7633],
           zoom=10,
           style={
               'width': '1000px',
               'height': '500px'
           }),
    dcc.Location(id='url', refresh=False),
    html.Div(id='click-output')
])

@app.callback(
    Output('free_libraries', 'free_libraries'),
    Output('free_libraries', 'center'),
    Output('free_libraries', 'zoom'),
    Input('free_libraries', 'click_feature')
)
def zoom_to_point(click_feature):
    if click_feature:
        feature = click_feature['LABEL']
        center = [feature['LATITUDE'], feature['LONGITUDE']]
        zoom = 14  # You can adjust the zoom level as needed
    return feature, center, zoom

app.run_server(debug=True)
