function createScatterPlot(inputData, options, place) {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable(inputData);
        var chart = new google.visualization.ScatterChart(document.getElementById(place));
        chart.draw(data, options);
    }
}

function mapVisuals() {
    var mymap = L.map('mapid').setView([79.6903, 44.3894], 8);

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
                    'Some problem with ${path}, ${response.status}'
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
    mapVisuals();

    processAPI(
        'get_avg_pass',
        function(data) {
            var chartData = [['Route', 'Average number']];
            chartData.push(...data.results);
            
            var options = {
                title: 'Average number of passengers per route',
                hAxis: {title: 'Route'},
                vAxis: {title: 'Average number'},
                legend: 'none'
            };
            createScatterPlot(chartData, options, 'chart_div');
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
