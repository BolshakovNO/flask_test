'use strict';

function addChart(data) {
    var container = $('#parent-chart-container'),
        new_chart = $('<div class="chart-container col-md-4 col-md-offset-3">');
    container.append(new_chart);

    $.plot(new_chart, data, {
        series: {
            pie: {
                show: true
            }
        },
        grid: {
            hoverable: true,
            clickable: true
        },
        legend: {
            show: false
        },
        colors: ["#FA5833", "#2FABE9", "#FABB3D", "#78CD51"]
    });
    new_chart.css('opacity', 1);
}

function onEnterKeyPress (e) {
    debugger;
    if (e.charCode == 13) {
        sendTask();
    }
}
function sendTask(url) {
    alert('ok')
}

//var socket = io.connect("http://localhost:5000/tail");
//socket.emit("subscribe");
//socket.on("tail-message", function(data) {
//  $(".log-output").append(data);
//});
