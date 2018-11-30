function createPlot(data) {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ['Route', 'Delay'],
            [ '8A',      12],
            [ '8B',      5.5],
            [ '100C',     14],
            [ '100D',      5],
            [ '3A',      3.5],
            [ '3B',    7]
        ]);

        var options = {
            title: 'Average delay per route',
            hAxis: {title: 'Route', minValue: 0, maxValue: 15},
            vAxis: {title: 'Delay', minValue: 0, maxValue: 15},
            legend: 'none'
        };

        var chart = new google.visualization.ScatterChart(document.getElementById('chart_div'));

        chart.draw(data, options);
    }
}

function getRoutes() {
    fetch('./api_v1/get_routes')
    .then(
        function(response) {
            if (response.status !== 200) {
                console.log(
                    'Looks like there was a problem. Status Code: ' + response.status);
                return;
            }

            response.json().then(function(data) {
                console.log(data);
                // but it's the simplset way
                // need to figure how to change existing plot every time
                createPlot(data);
            });
        }
    )
    .catch(function(err) {
        console.log('Fetch Error :-S', err);
    });
}


function fetchInitialBars() {
    fetch('./api_v1/get_all_routes')
    .then(
        function(response) {
            if (response.status !== 200) {
                console.log(
                    'Looks like there was a problem. Status Code: ' + response.status);
                return;
            }

            response.json().then(function(data) {
                var busbag = document.getElementById("busbag");
                busbag.innerHTML = 
                `<div class="card-header">
                    <h4>Routes that we track</h4>
                </div>
                <div class="card-body">`
                    + data.routes + 
                `</div>`;
            });
        }
    )
    .catch(function(err) {
        console.log('Fetch Error :-S', err);
    });
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
    getRoutes();
    fetchInitialBars();
    mapVisuals();

    processAPI(
        'get_routes_num',
        function(data) {
            let routesbag = document.getElementById("routesnumbar");
            routesbag.innerHTML = `
            <div class="card-header">
                <h4>Routes in Barrie</h4>
            </div>
            <div class="card-body">
                ${data.NumOfRoute}
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
                ${data.NumOfVehicle}
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
