var jsonObj;
var tops = parseInt(getQueryStringByName("top"));
var morethan = parseInt(getQueryStringByName("morethan"));
var limit = parseInt(getQueryStringByName("limit"));
if(isNaN(tops)) tops = 20;
if(isNaN(morethan)) morethan = 30;
if(isNaN(limit)) limit = 100;

var tags = [
    ["total.avg", "平均顺位", true],
    ["winGame.avg", "平均和了率", false],
    ["winGame_score.avg", "平均和了点", false],
    ["chong.avg", "平均铳率", true],
    ["winGame_round.avg", "平均和了巡", true],
    ["fulu.avg", "平均副露率", true],
    ["fulu_winGame.per", "平均副露和了率", false],
    ["fulu_score.avg", "平均副露得点", false],
    ["richi.avg", "平均立直率", false],
    ["richi_winGame.per", "平均立直和了率", false],
    ["richi_score.avg", "平均立直得点", false],
    ["richi_inner_dora.avg", "平均立直和了里dora数", false],
    ["richi_yifa.per", "平均立直一发率", false]
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
    var row = ['unknow', false];
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

    showList(dtLst);
};

var showList = function(dtLst){
    var con = $("div#bill_list");
    con.empty();
    var table = $("<table id='bill_list'></table>");
    table.append($("<tr></tr>").append("<td>排名</td>").append("<td>ID</td>").append("<td>数值</td>"));
    for(var i = 0; i < dtLst.length; i++){
        var name = dtLst[i][1];
        var value = dtLst[i][0];
        var nametd = $("<td></td>").append($("<a>" + name + "</a>").attr('href', '../statistics?name=' + name));
        table.append($("<tr></tr>").append("<td>" + (i + 1) + "</td>").append(nametd).append("<td>" + value + "</td>"));
    }
    con.append(table);
};

$(document).ready(function(){
    var apiUrl = "../API?method=billboard&morethan=" + morethan + "&limit=" + limit;
    $.get(apiUrl, function(data, status){
        if(status!='success'){

        }else{
            jsonObj = JSON.parse(data);
            loadTag();
            showChart(tags[0][0]);
        }
    });
});