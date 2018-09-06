const colors = 
[
    [255,237,0],
    [232,169,12],
    [255,117,0],
    [232,61,32],
    [255,0,147]
]
const MINTIME = 1525244400.0
const MAXTIME = 1525330800.0
var tmin = 1525244400.0
var tmax  = tmin + 3600 //in seconds
var timeRange = [tmax, tmin]
var timeSlider = document.getElementById("timeSlider");
var timeControl = document.getElementById("sliceControl");
var playbackTime = document.getElementById("playback")
var timeOut = document.getElementById("time");
var strokeSlider = document.getElementById("strokeSlider");
var startDate = new Date(tmin*1000).toLocaleString('en-US');
var endDate = new Date(tmax*1000).toLocaleString('en-US');
var stroke = 4;
var animating = false;

deckgl = new deck.DeckGL({
    container: 'container',
    mapboxApiAccessToken: 'pk.eyJ1IjoibHVjYWJvbW1hciIsImEiOiJjamphYzZxcDkzZzc0M3ZvNm45d3Y4NXd0In0.NW5KWw9ZJg6a0iQm5D7omw',
    mapStyle:'mapbox://styles/mapbox/dark-v9',      
    longitude: -122.017863,
    latitude: 37.430330,
    zoom: 9,
    layers: []
});


refresh();
timeOut.innerHTML = "" + startDate + " <br> to <br> " + endDate; // Display the default slider value
timeControl.value = "Show 24hr"
timeSlider.value = tmin;

timeSlider.oninput = function() {
    console.log(new Date(this.value*1000));
    tmin = this.value;
    tmax = parseFloat(tmin) + 3600;
    refresh();
    updateTime();
    timeControl.value = "Show 24hr"
}
strokeSlider.oninput = function(){
    stroke = this.value;
    refresh();
}
timeControl.onclick = function(){
    tmin = MINTIME;
    tmax = MAXTIME;
    animating = false;
    playbackTime.value = "Animate";
    window.clearInterval(playbackTimer);
    refresh();
    updateTime();
}
function updateTime() {
    startDate = new Date(tmin*1000).toLocaleString('en-US');
    endDate = new Date(tmax*1000).toLocaleString('en-US');
    timeOut.innerHTML = "" + startDate + " <br> to <br> " + endDate; // Display the default slider value
}
function tick() {
    tmin = parseFloat(tmin) + 36.0;
    tmax = parseFloat(tmin) + 3600.0;
    if(parseFloat(tmin) > MAXTIME)
    {
        console.log("Reached end of animation.")
        tmin = MINTIME;
        tmax = tmin + 3600;
    }
    refresh();
    updateTime();
    timeSlider.value = tmin;
}

playbackTime.onclick = function(){
    if (!animating)
    {
        playbackTime.value = "Stop";
        playbackTimer = setInterval(tick, 10);
        animating = true;
    }
    else
    {
        animating = false;
        playbackTime.value = "Animate";
        window.clearInterval(playbackTimer);
    }
}

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
                data: 'https://ucea5430f9b964c0a270b35fb77e.dl.dropboxusercontent.com/cd/0/inline/AK9UEmmAkB-VCn4A90jVlia2VbPAkB3yFhZL0AphZf7U68UWFo18bJ6CNVrY16stgdB-DOzB40GRx4zeDux-Z5XF5ARA-SqH3fi-880URZdumOoWBQZjZV8VOtBG9tpqheTVUY-orjHuRyeIwb8BxELh5xylFuc6swr2vt2UohhwQpGw-ORMjY0S12xmugYSPdw/file',
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
        new deck.PointCloudLayer({
                id: 'point-cloud-layer',
                data: 'multiFlight.json',
                pickable: false,
                radiusPixels: 4,
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

            })
        ];

