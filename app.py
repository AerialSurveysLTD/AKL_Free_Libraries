import dash
import dash_leaflet as dl
from dash import dcc, html
import pandas as pd
import geopandas as gpd

app = dash.Dash(__name__)

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("FreeLibraries2.csv")

# Define the color mapping for the REGION categories
color_mapping = {
    "Auckland Central Little Libraries": "red",
    "North Auckland": "blue",
    "West Auckland" : "green",
    "South Auckland" : "orange",
    "East Auckland" : "yellow",
    "Franklin & beginning of Waikato" : "purple",
}

# Create a GeoDataFrame from the XY coordinates in NZTM format
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df["X"], df["Y"]), crs="EPSG:2193"
)

# Add a new column for the point color based on the REGION category
gdf["color"] = gdf["REGION"].map(color_mapping)

app.layout = dl.Map(style={
                          'width': '1000px',
                          'height': '500px'
                      },
            children=[dl.TileLayer(), 
                      dl.CircleMarker(
                        center=[row.geometry.y, row.geometry.x],
                        radius=5,
                        color=row["color"],
                    )
                    for _, row in gdf.iterrows()
                ]
            
            ),



if __name__ == "__main__":
    app.run_server(debug=True)
