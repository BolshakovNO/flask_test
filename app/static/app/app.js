
'use strict';

function addChart(data) {
    var container = $('#parent-chart-container'),
        new_chart = $('<div class="chart-container col-md-4 col-md-offset-3">');
    container.append(new_chart);

    $.plot(new_chart, [JSON.parse(data)], {
        series: {
            bars: {
                show: true,
                barWidth: 0.6,
                align: "center"
            }
        },
        xaxis: {
            mode: "categories",
            tickLength: 0
        }
    });
    new_chart.css('opacity', 1);
}

function onEnterKeyPress() {
    if (window.event.charCode == 13) {
        sendTask();
    }
}

function sendTask() {
    socket.emit('task', {url: $('#text').val()});
}

var socket = io.connect(window.location.href + 'parse');
socket.on('parse complete', addChart);

socket.on('message', function () {
    debugger;
});
