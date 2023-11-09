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


# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("FreeLibraries2.csv")

# print(df)
# df['tooltip'] = df.NAME

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

# Create a GeoDataFrame from the XY coordinates in NZTM format
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df["LONGITUDE"], df["LATITUDE"]), crs="EPSG:4326"
)

style_callback = assign("""
function(feature, latlng, context) {
                        log.console.log(context);
    var region = feature.properties.REGION;
    var color = context.props.colorMapping[region] || 'gray'; // Default to gray if the region is not in the mapping
    return {
        radius: 8,  // Adjust the radius of the circle marker as needed
        color: 'black',  // Outline color of the circle
        weight: 1,  // Outline weight
        opacity: 1,  // Outline opacity
        fillColor: color,
        fillOpacity: 0.7  // Fill opacity of the circle
    };
}
""")


geojson = dl.GeoJSON(id='free_libs', data = json.loads(gdf.to_json()), 
                    #  style= {'radius': 8,  # Default radius for all features
                    #         'color': 'black',
                    #         'weight': 1,
                    #         'opacity': 1,
                    #         'fillColor': 'gray',
                    #         'fillOpacity': 0.7,
                    #         'circleMarker': 'function(feature, latlng, context) { return context.props.styleCallback(feature, latlng, context); }'
                    # },
                    style=style_callback, 
                    zoomToBoundsOnClick=True, 
                    cluster=True, 
                    superClusterOptions=dict(radius=100), 
                    hideout=dict(colorProp=color_prop),  
                     )
# geobuff = dlx.geojson_to_geobuf(geojson)

# point_To_Layer = assign("""function(feature, latlng) {const{colorscale, colorProp} = context.hideout;
#                         circleOptions.fillColor = colorscale[feature.properties[colorProp]];
#                         return L.circleMarker(latlng, circleOptions);""")

# free_libs = dl.GeoJSON(data=geojson,
#                        id="free_libs",
#                     #    options=dict(pointToLayer=point_To_Layer),
#                        cluster=True,
#                        zoomToBoundsOnClick = True,
#                        superClusterOptions=dict(radius=40),
#                        hideout=dict(colorProp=color_prop),
#                        )

# print(free_libs)

app = dash.Dash()
app.layout = html.Div([
    dl.Map(children=[dl.TileLayer(), geojson],
           center=[-36.8485, 174.7633],
           zoom=9,
           style={
                          'width': '1000px',
                          'height': '500px'
                      }),
                      html.Button("Click Me!", id='btn')
],
                      style={
                          'width': '1000px',
                          'height': '500px'
                      },
                      id="map",
                      )



app.run_server(debug=True)
