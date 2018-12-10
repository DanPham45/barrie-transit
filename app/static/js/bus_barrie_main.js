function createScatterPlot(inputData, options, place) {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable(inputData);
        var chart = new google.visualization.ScatterChart(document.getElementById(place));
        chart.draw(data, options);
    }
}

function createBubbleChart(inputData, options, place) {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawBubble);

    function drawBubble() {
        var data = google.visualization.arrayToDataTable(inputData);
        var chart = new google.visualization.BubbleChart(document.getElementById(place));
        chart.draw(data, options);
    }
}

function createComboChart(inputData, options, place) {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawBubble);

    function drawBubble() {
        var data = google.visualization.arrayToDataTable(inputData);
        var chart = new google.visualization.ComboChart(document.getElementById(place));
        chart.draw(data, options);
    }
} 

function getLine(points, color){
    var pointList = [];
    for (var i = 0; i < points.length; i++) {
        pointList.push(new L.LatLng(points[i]['lat'],points[i]['lon']))
    }
    var line = new L.Polyline(pointList,
    {
        color: color,
        weight: 3,
        opacity: 5,
        smoothFactor: 2
    });
    return line;
}


function getColor(d) {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;

}


function mapVisuals(mapid, data) {     
    var mymap = L.map(mapid).setView([44.35184883333333, -79.6284255], 10);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiaGFza3BwcCIsImEiOiJjanAzOHFscDQwNWRvM2twZXlxMTNocmRpIn0.-fR_k4Aw9WSYPqlX6NHfHA'
    }).addTo(mymap);

    // const colors = [];
    // for (var i = 0; i < data.length; i += 1) {
    //     colors.push('#'+();
    // }

    var indexColor = 0;
    Object.keys(data).forEach(function(key) {

        var d = data[key];
        var points = [];
        for(var i = 0; i < d.length; i++) {
            points.push({'lat': d[i][2], 'lon': d[i][1]});
        }
        var line = getLine(points, getColor(indexColor++));
        line.addTo(mymap);
        mymap.fitBounds(line.getBounds());
      
    });


    // var latlang = [
    //     [[17.385044, 78.486671], [16.506174, 80.648015], [17.686816, 83.218482]],
    //     [[13.082680, 80.270718], [12.971599, 77.594563],[15.828126, 78.037279]]
    //  ];
     
    //  // Creating poly line options
    //  var multiPolyLineOptions = {color:'red'};
     
    //  // Creating multi poly-lines
    //  var multipolyline = L.multiPolyline(latlang , multiPolyLineOptions);
     
    //  // Adding multi poly-line to map
    //  multipolyline.addTo(mymap);
    // console.log(points, line);
    // var j;
    // var temppoints=[];
    // //draw lines
    // for(j=0;j<static.length-1;j++){
    //     temppoints[0]=static[j];
    //     temppoints[1]=static[j+1];
    //     var temppoly=colorPoints(temppoints,getColor(temppoints[0]['capacity']));
    //     temppoly.addTo(mymap);
    // }
    // //set labels
    // for(j=0;j<static.length;j++)
    // {
    //     var marker = L.marker([static[j]['latitude'],static[j]['longitude']]).addTo(mymap);
    //     //marker.bindTooltip(static[j]['stop_code'],{permanent:true,direction:'right'})
    //     marker.bindPopup("<b>Bus Stop: "+static[j]['stop_code']+"</b><br>Here is "+static[j]['stop_name']).openPopup();
    // }

    // var legend = L.control({position: 'bottomright'});
    // legend.onAdd = function (map) {
    //     var div = L.DomUtil.create('div', 'info legend'),
    //         grades = [10, 20, 30, 40, 50, 60, 70, 80],
    //         labels = ['a', 'd', 'c', 'b'];
    //     // loop through our density intervals and generate a label with a colored square for each interval
    //     for (var i = 0; i < grades.length; i++) {
    //         div.innerHTML +=
    //             '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
    //             grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    //     }

    //     return div;
    // };
}

function compareRoutes(data) {
    var mymap = L.map(mapid).setView([44.35184883333333, -79.6284255], 10);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiaGFza3BwcCIsImEiOiJjanAzOHFscDQwNWRvM2twZXlxMTNocmRpIn0.-fR_k4Aw9WSYPqlX6NHfHA'
    }).addTo(mymap);
}

function processAPI(path, func) {
    fetch(`./api_v1/${path}`)
    .then(
        function(response) {
            if (response.status !== 200) {
                console.log(
                    `Some problem with ${path}, ${response.status}`
                );
                return;
            }
            response.json().then(func);
        }
    )
    .catch(function(err) {
        console.log('Fetch Error :-S', err);
    });
}


window.onload = function() {
    processAPI(
        'get_avg_per_stop_location',
        function(data) {
            mapVisuals('mapid1', data);
        }
    );

    processAPI(
        'get_avg_pass',
        function(data) {
            var chartData = [['Route', 'Average number of passenger']];
            chartData.push(...data.results);
            
            var options = {
                title: 'Average number of passengers',
                hAxis: {title: 'Route'},
                vAxis: {title: 'Average number of passenger'},
                legend: 'none'
            };
            createScatterPlot(chartData, options, 'chart_div');
        }
    );

    processAPI(
        'get_avg_route_stop',
        function(data) {
            var chartData = [['Route', 'N', 'Avg Pass', 'Stop']];
            chartData.push(...data.results);

            var options = {
                title: 'Average number of passengers per route per stop',
                hAxis: {title: 'Route'},
                vAxis: {title: 'Average number'},
                legend: 'none'
            };
            createBubbleChart(chartData, options, 'chart_stops_routes_avg');
        }
    );

    processAPI(
        'get_compare_routes',
        function(data) {
            var chartData = [['Route', 'Avg Pass', 'Avg Speed']];
            chartData.push(...data.results);

            var options = {
                title: 'Average number of passengers and average speed per route',
                hAxis: {title: 'Route'},
                vAxis: {title: 'Average number'},
                seriesType: 'bars',
                legend: 'none'
            };
            createComboChart(chartData, options, 'chart_compare_routes');
        }
    );

    processAPI(
        'get_routes_num',
        function(data) {
            let routesbag = document.getElementById("routesnumbar");
            routesbag.innerHTML = `
            <div class="card-header">
                <h4>Routes in Barrie</h4>
            </div>
            <div class="card-body">
                ${data.num_of_routes}
            </div>`;
        }
    );
    processAPI(
        'get_bus_num',
        function(data) {
            let busbag = document.getElementById("busnumbar");
            busbag.innerHTML = `
            <div class="card-header">
                <h4>Buses in Barrie</h4>
            </div>
            <div class="card-body">
                ${data.num_of_vehicles}
            </div>`;
        }
    );
    processAPI(
        'get_track_days',
        function(data) {
            let daystackbag = document.getElementById("daystrackbar");
            daystackbag.innerHTML = `
            <div class="card-header">
                <h4>Days of tracking</h4>
            </div>
            <div class="card-body">
                ${data.days}
            </div>`;
        }
    );
}
