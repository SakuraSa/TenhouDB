var jsonObj;
var tops = parseInt(getQueryStringByName("top"));
if(isNaN(tops)) tops = 20;

var tags = [
    ["total.avg", "平均顺位", true],
    ["winGame.avg", "平均和了率", false],
    ["winGame_score.avg", "平均和了点", false],
    ["chong.avg", "平均铳率", true],
    ["richi.avg", "平均立直率", false],
    ["winGame_round.avg", "平均和了巡", true]
];

var loadTag = function(){
    var con = $("div#bill_tags");
    con.empty();
    for(var i = 0; i < tags.length; i++){
        var row = tags[i];
        var link = $("<a></a>").text(row[1]);
        link.attr("href", "javascript: showChart('" + row[0] + "');");
        link.attr("id", "tags");
        con.append(link);    
    }

};

var showChart = function(name){
    var
    bars = {
        data: [],
        bars: {
            show: true,
            barWidth: 0.2,
            lineWidth: 0,
            fillColor: {
                colors: ['#11f', '#ddf'],
                start: 'top',
                end: 'bottom'
            },
            fillOpacity: 0.8
        }
    }, markers = {
        data: [],
        markers: {
            show: true,
            position: 'ct'
        }
    }, lines = {
        data: [],
        lines: {
            show: true,
            fillColor: ['#00A8F0', '#fff'],
            fill: true,
        }
    }, avgLine = {
        data: [],
        lines: {
            show: true,
            color: '#aff',
            fillOpacity: 1
        }
    },
    point,
    graph,
    ticks = [],
    i,
    avg = 0,
    container = document.getElementById("bill_chart");

    var dtLst;
    var row;
    for(i = 0; i < tags.length; i++)
        if(tags[i][0] == name){
            row = tags[i];
            break;
        }
    if(row[2]) {
        dtLst = jsonObj[name].concat().reverse();
    }else{
        dtLst = jsonObj[name];
    }

    for (i = 0; i < dtLst.length; i++)
        avg += dtLst[i][0];
    avg = avg / dtLst.length;

    for (i = 0; i < dtLst.length && i < tops; i++) {
        point = [i, dtLst[i][0]];
        bars.data.push(point);
        markers.data.push(point);
        lines.data.push(point);
        avgLine.data.push([i, avg]);
        ticks.push([i, dtLst[i][1]]);
    }

    graph = Flotr.draw(
    container,
    [lines, avgLine, bars, markers], {
        xaxis: {
            ticks: ticks
        },
        grid: {
            verticalLines: false,
            backgroundColor: ['#fff', '#ccc']
        },
        title: row[1]
    }
    );
};

$(document).ready(function(){
    $.get("../API?method=billboard", function(data, status){
        if(status!='success'){

        }else{
            jsonObj = JSON.parse(data);
            loadTag();
            showChart(tags[0][0]);
        }
    });
});