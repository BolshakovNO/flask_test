'use strict';

function addChart(data) {
    $.plot($("#piechart"), data,
    {
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
}

function sendTask(url) {

}
