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

function fill_stats(data, t) {
    let avgs = document.getElementById("stats_avgs");
    avgs.innerHTML = `
    <div class="detail-value">${data.AvgStop} minutes</div>
    <div class="detail-name">Average waiting time on stops today</div>`;

    let maxs = document.getElementById("stats_maxs");
    maxs.innerHTML = `
    <div class="detail-value">${data.MaxStop} minutes</div>
    <div class="detail-name">Max waiting time on stops today</div>`;

    let mins = document.getElementById("stats_mins");
    mins.innerHTML = `
    <div class="detail-value">${data.MinStop} minutes</div>
    <div class="detail-name">Min waiting time on stops today</div>`;

    let avgd = document.getElementById("stats_avgd");
    avgd.innerHTML = `
    <div class="detail-value">${data.AvgDelay} minutes</div>
    <div class="detail-name">Average delay today</div>`;

    let maxd = document.getElementById("stats_maxd");
    maxd.innerHTML = `
    <div class="detail-value">${data.MaxDelay} minutes</div>
    <div class="detail-name">Max delay today</div>`;

    let mind = document.getElementById("stats_mind");
    mind.innerHTML = `
    <div class="detail-value">${data.MinDelay} minutes</div>
    <div class="detail-name">Min delay today</div>`;

    if (t == 0) {
        document.getElementById("day_stat_btn").classList.add('active');
        document.getElementById("week_stat_btn").classList.remove('active');
    }
    else if (t == 1) {
        document.getElementById("week_stat_btn").classList.add('active');
        document.getElementById("day_stat_btn").classList.remove('active');
    }
}

function getStats(t) {
    processAPI(
        `get_stats/${t}`,
        function(data) {
            fill_stats(data, t);
        }
    );
}

function mapVisuals(mapid, data, routeName) {
    var mymap = L.map(mapid).setView([44.35184883333333, -79.6284255], 10);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiaGFza3BwcCIsImEiOiJjanAzOHFscDQwNWRvM2twZXlxMTNocmRpIn0.-fR_k4Aw9WSYPqlX6NHfHA'
    }).addTo(mymap);

    var d = data[routeName];
    for(var i = 0; i < d.length; i++) {
        var numberIcon = L.divIcon({
            className: "number-icon",
            iconSize: [25, 41],
            iconAnchor: [10, 44],
            popupAnchor: [3, -40],
            html: d[i][3],        
        });
        var marker = new L.marker([d[i][2], d[i][1]], { icon: numberIcon });
        marker.addTo(mymap);
    }
}

function onClickRoute(routeName) {
    processAPI(
        'get_avg_per_stop_location',
        function(data) {
            mapVisuals('mapid1', data, routeName);
        }
    );
}

function buildMap() {
    processAPI(
        'get_avg_per_stop_location',
        function(data) {
            let resultHtml = ``;
            let routes = Object.keys(data);

            resultHtml += `<a href="#" onclick="onClickRoute('${routes[0]}');" class="btn active">${routes[0]}</a>`;
            routes.slice(1).forEach(function (route) {
                resultHtml += `<a href="#" onclick="onClickRoute('${route}');" class="btn">${route}</a>`;
            });

            let mind = document.getElementById("routeListBtn");
            mind.innerHTML = resultHtml;

            mapVisuals('mapid1', data, routes[1]);
        }
    );
}

window.onload = function() {
    getStats(1);

    //buildMap();

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
    processAPI(
        'get_records_num',
        function(data) {
            let daystackbag = document.getElementById("locrecnum");
            daystackbag.innerHTML = data.num_of_records;
        }
    );
}
