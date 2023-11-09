import dash
import dash_leaflet as dl
import dash.html as html
import json
import pandas as pd
import geopandas as gpd
from dash_extensions.javascript import arrow_function, assign, Namespace
import dash_leaflet.express as dlx

zipfile = "zip://D:/DATA/Scripting_App_WestHealth/pydataglobal-2021/data/cb_2018_us_state_20m.zip"
states = gpd.read_file(zipfile)

covid = pd.read_csv('D:/DATA/Scripting_App_WestHealth/pydataglobal-2021/data/10-19-2021.csv').astype({'FIPS': int})

# print(covid)

coviddf = states.astype({
    'STATEFP': int
}).merge(covid, how='left', left_on='STATEFP', right_on='FIPS')

# print(coviddf)

classes = [0, 10000, 30000, 100000, 300000, 1000000, 30000000, 10000000]
ctg = ['0+', '10k+', '30k+', '100k+', '300k+', '1M+', '3M+', '10M+']
colorscale = [
    '#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C',
    '#BD0026', '#800026'
]
# Create colorbar.
colorbar = dlx.categorical_colorbar(categories=ctg,
                                    colorscale=colorscale,
                                    width=300,
                                    height=30,
                                    position="bottomleft")

style_handle = arrow_function("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    console.log("Value:", value);  // Add this line for debugging
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}"""
                      )

# style_handle = Namespace('choropleth_demo', 'covid')('StyleHandler')

style = dict(weight=2,
             opacity=1,
             color='white',
             dashArray='3',
             fillOpacity=0.7)

geojson = dl.GeoJSON(
    data=json.loads(coviddf.to_json()),
    options=dict(style=style_handle),  # Here's the magic
    hideout=dict(colorscale=colorscale,
                 classes=classes,
                 style=style,
                 colorProp="Confirmed"),
    id="geojson")


app = dash.Dash()
app.layout = dl.Map(
        children=[dl.TileLayer(), geojson, colorbar],
                     center=[39, -98], zoom=4,
                      style={
                          'width': '1000px',
                          'height': '500px'
                      },
                      id="map")
                


app.run_server(debug=True)