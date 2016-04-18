
'use strict';

function addChart(result) {
    var data = result.data,
        url = result.url;

    var container = $('#parent-chart-container'),
        url_text = $('<span class="url-text col-md-4 col-md-offset-3">'),
        new_chart = $('<div class="chart-container col-md-4 col-md-offset-3">');

    url_text.text(url);
    container.append(url_text);
    container.append(new_chart);

    $.plot(new_chart, [data], {
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
    var url = $('#text').val();
    if (!!url.trim()) {
        //socket.emit('task', {url: url});
        $.ajax('/run_task', {
            method: 'POST',
            data: {url: url}
        }).done(function (resp) {
            if (resp.error) {
                setErrorText(resp.error);
            }
            else if (resp.task_id) {
                socket.emit('monitor', resp.task_id)
            }
            else if (resp.result) {
                addChart(resp.result);
            }
        });
        setErrorText('');
    } else {
        setErrorText('No URL passed')
    }
}

function setErrorText(text) {
    $('#error-container').text(text);
}

var socket = io.connect(window.location.href);

socket.on('parse_complete', addChart);

socket.on('error', function (error) {
    setErrorText(error)
});
