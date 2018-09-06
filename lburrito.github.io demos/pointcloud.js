const colors = 
[
    [255,237,0],
    [232,169,12],
    [255,117,0],
    [232,61,32],
    [255,0,147]
]

var stroke = 4;

deckgl = new deck.DeckGL({
    container: 'container',
    mapboxApiAccessToken: 'pk.eyJ1IjoibHVjYWJvbW1hciIsImEiOiJjamphYzZxcDkzZzc0M3ZvNm45d3Y4NXd0In0.NW5KWw9ZJg6a0iQm5D7omw',
    mapStyle:'mapbox://styles/mapbox/dark-v9',      
    longitude: -122.017863,
    latitude: 37.430330,
    zoom: 9,
    layers: [        
        new deck.PointCloudLayer({
            id: 'point-cloud-layer',
            data: 'https://raw.githubusercontent.com/LBurrito/lburrito.github.io/master/deckLineVis.json',
            pickable: false,
            radiusPixels: 2,
            getPosition: d => {
                return [d.position[0], d.position[1], d.altitude]
            },
            getColor: d => (d.altitude < 0 ? [0,0,0] :
                (d.altitude < 2500 ? colors[0] : 
                    (d.altitude < 5000 ? colors[2] : 
                        (d.altitude < 7500 ? colors[2] : colors[3])
                    )
                )
            ), 
            getNormal: d => d.normal,
            opacity: 0.05,
            lightSettings: {},
            onHover: ({object}) => setTooltip(object.position.join(', '))

    })]
});


function refresh(){
    const layers = [
        new deck.LineLayer({
            id: 'flight-paths',
            data: 'https://raw.githubusercontent.com/LBurrito/lburrito.github.io/master/deckLineVis.json',
            getSourcePosition: d => {
                return [d.position[0], d.position[1], d.altitude]
            },
            getTargetPosition: d => {
                return [d.nextPos[0], d.nextPos[1], d.nextAlt]
            },
            getColor: d => {
                var color = (d.altitude < 0 ? [255,255,255] :
                    (d.altitude < 2500 ? colors[0] : 
                        (d.altitude < 5000 ? colors[2] : 
                            (d.altitude < 7500 ? colors[2] : colors[3])
                        )
                    )
                );
                
                if(d.time > tmin && d.time < tmax)
                {
                    return [color[0], color[1], color[2], 60];
                }
                else{
                    return [0, 0, 0, 0];
                }
                
            },
            getStrokeWidth: d=>{
                if(d.time > tmin && d.time < tmax)
                {
                    return parseInt(stroke);
                }
                else{
                    return 0;
                }
            },
            updateTriggers:{
                    getStrokeWidth: [stroke, tmin, tmax],
                    getColor: [tmin, tmax]
            }        
        })
    ]
    deckgl.setProps({layers})
}


        var unusedLayers = [
            new deck.ScatterplotLayer({
                id: 'scatter-plot',
                data: 'https://raw.githubusercontent.com/LBurrito/lburrito.github.io/master/deckLineVis.json',
                //radiusScale: 1,
                radius: 1,
                //getRadius: d => (d.altitude / 10000) * 300,//max altitude is 10000,
                getColor: d => (d.altitude < 0 ? [0,0,0] :
                                    (d.altitude < 2500 ? colors[0] : 
                                        (d.altitude < 5000 ? colors[2] : 
                                            (d.altitude < 7500 ? colors[2] : colors[3])
                                        )
                                    )
                                ),         
                radiusMinPixels: 0.5,
                getPosition: d => {
                    return [d.position[0], d.position[1], d.altitude]
                },
                opacity: 0.05
            }),

        ];

