function createPlot(data) {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ['Age', 'Weight'],
            [ 8,      12],
            [ 4,      5.5],
            [ 11,     14],
            [ 4,      5],
            [ 3,      3.5],
            [ 6.5,    7]
        ]);

        var options = {
            title: 'Age vs. Weight comparison',
            hAxis: {title: 'Age', minValue: 0, maxValue: 15},
            vAxis: {title: 'Weight', minValue: 0, maxValue: 15},
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
                console.log(data);
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

window.onload = function() {
    fetchInitialBars();
}
