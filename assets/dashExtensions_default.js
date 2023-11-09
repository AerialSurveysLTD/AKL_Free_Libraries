window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, layer, context) {
            layer.bindTooltip(`${feature.properties.city} (${feature.properties.density})`)
        },
        function1: function(feature, latlng, context) {
            const colorMapping = {
                "Auckland Central Little Libraries": "red",
                "North Auckland": "blue",
                "West Auckland": "green",
                "South Auckland": "orange",
                "East Auckland": "yellow",
                "Franklin & beginning of Waikato": "purple"
            };
            const {
                circleOptions,
                colorProp
            } = context.hideout;
            circleOptions.fillColor = colorMapping[feature.properties[colorProp]] || 'gray'; // set color based on color prop
            return L.circleMarker(latlng, circleOptions); // render a simple circle marker
        }
    }
});