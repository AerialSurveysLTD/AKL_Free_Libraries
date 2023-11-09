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
from dash_extensions.javascript import arrow_function, assign
from dash.exceptions import PreventUpdate

# Define the color mapping for the REGION categories

color_mapping = {
    "Auckland Central Little Libraries": "red",
    "North Auckland": "blue",
    "West Auckland" : "green",
    "South Auckland" : "orange",
    "East Auckland" : "yellow",
    "Franklin & beginning of Waikato" : "purple",
}

color_prop = "REGION"

# Convert Python color_mapping to a JavaScript object
color_mapping_js = json.dumps(color_mapping)

# Geojson rendering logic, must be JavaScript as it is executed in clientside.
on_each_feature = assign("""function(feature, layer, context){
    layer.bindTooltip(`${feature.properties.city} (${feature.properties.density})`)
}""")

# point_to_layer = assign("""function(feature, latlng, context){
#     log.console(context);
#     const {color_mapping, circleOptions, colorProp} = context.hideout;
#     circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop
#     return L.circleMarker(latlng, circleOptions);  // render a simple circle marker
# }""")

point_to_layer = assign(f"""function(feature, latlng, context){{
    const colorMapping = {color_mapping_js};
    const {{circleOptions, colorProp}} = context.hideout;
    circleOptions.fillColor = colorMapping[feature.properties[colorProp]] || 'gray';  // set color based on color prop
    return L.circleMarker(latlng, circleOptions);  // render a simple circle marker
}}""")

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("FreeLibraries2.csv")

# print(df)
# df['tooltip'] = df.NAME





# Create a GeoDataFrame from the XY coordinates in NZTM format
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df["LONGITUDE"], df["LATITUDE"]), crs="EPSG:4326"
)

hover_style = dict(fillColor='black', fillOpacity=1, stroke=False, radius=5)

gdf['tooltip'] = gdf.NAME

geojson = dl.GeoJSON(id='free_libs', data = json.loads(gdf.to_json()), 
                    pointToLayer=point_to_layer,  
                    zoomToBoundsOnClick=True, 
                    cluster=True, 
                    superClusterOptions=dict(radius=100), 
                    hideout=dict(colorProp='REGION', circleOptions=dict(fillOpacity=1, stroke=False, radius=5)),  
                     hoverStyle=arrow_function(hover_style))

app = dash.Dash()
app.layout = html.Div([
    dl.Map(children=[dl.TileLayer(), geojson],
           center=[-36.8485, 174.7633],
           zoom=9,
           style={
                          'width': '1000px',
                          'height': '500px'
                      }),
                      html.Button("North Auckland", id='Nor_btn'),
                      html.Button("West Auckland", id='Wst_btn'),
                      html.Button("Auckland Central", id='Cent_btn'),
                      html.Button("East Auckland", id='Est_btn'),
                      html.Button("South Auckland", id='Sth_btn'),
                      html.Button("Franklin & beginning of Waikato", id='Fwr_btn'),
],
                      style={
                          'width': '1000px',
                          'height': '500px'
                      },
                      
                      id="map",
                      )

@app.callback(Output('free_libs', 'data'), 
              [Input('Nor_btn', 'n_clicks'), 
               Input('Wst_btn', 'n_clicks'), 
               Input('Cent_btn', 'n_clicks'),
               Input('Est_btn', 'n_clicks'), 
               Input('Sth_btn', 'n_clicks'), 
               Input('Fwr_btn', 'n_clicks')
               ])
def filter_geojson(n_clicks_nor, n_clicks_wst, n_clicks_cent, n_clicks_est, n_clicks_sth, n_clicks_fwr):
    # Determine which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    button_id = ctx.triggered_id.split('.')[0]

    # Filter the GeoJSON data based on the clicked button
    if button_id == 'Nor_btn':
        filtered_data = filter_data_by_region(gdf, 'North Auckland')
    elif button_id == 'Wst_btn':
        filtered_data = filter_data_by_region(gdf, 'West Auckland')
    elif button_id == 'Cent_btn':
        filtered_data = filter_data_by_region(gdf, 'Auckland Central Little Libraries')
    elif button_id == 'Est_btn':
        filtered_data = filter_data_by_region(gdf, 'East Auckland')
    elif button_id == 'Sth_btn':
        filtered_data = filter_data_by_region(gdf, 'South Auckland')
    elif button_id == 'Fwr_btn':
        filtered_data = filter_data_by_region(gdf, 'Franklin & beginning of Waikato')
    else:
        raise PreventUpdate

    return json.loads(filtered_data.to_json())

def filter_data_by_region(df, region):
    return df[df['REGION'] == region]



app.run_server(debug=True)
