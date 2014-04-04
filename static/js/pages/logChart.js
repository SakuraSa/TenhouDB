var jsonObj;

var drawChart = function(jsonChart){
    var container, graph, ticks, datas, scMax, scMin;
    var tickSize = 5000;
    container = document.getElementById("container");
    ticks = [[0, "开场"]];
    for(var i=0;i<jsonChart.logs.length;i++){
        ticks.push([i+1, jsonChart.logs[i].name]);
    }
    datas = [];
    scMax = jsonChart.logs[0].startScore[0];scMin = scMax;
    for(var i=0;i<jsonChart.playerSum;i++){
        var dataRow = {"lines":{"show": true}, 
                       "points":{"show": true},
                       "label":jsonChart.players[i].name};
        var scoreRow = [[0, jsonChart.logs[0].startScore[i]]];
        for(var j=0;j<jsonChart.logs.length;j++){
            scoreRow.push([j+1, jsonChart.logs[j].endScore[i]]);
            scMax = Math.max(scMax, jsonChart.logs[j].endScore[i]);
            scMin = Math.min(scMin, jsonChart.logs[j].endScore[i]);
        }
        dataRow.data = scoreRow;
        datas.push(dataRow);
    }
    scMin = Math.floor(scMin / tickSize) * tickSize;
    scMax = Math.ceil(scMax / tickSize) * tickSize;
    graph = Flotr.draw(container,
        datas,
        {
            xaxis: {
                ticks: ticks,
            },
            yaxis: {
                max: scMax,
                min: scMin,
            },
            grid: {
                backgroundColor: {
                    colors: [[0, '#fff'], [1, '#eee']],
                    start: 'top',
                    end: 'bottom'
                }
            },
            legend : {
                position : 'nw'
            },
            title: '比赛分数变动表',
            subtitle: jsonChart.date + " <a id='watch' target='_blank' href='http://tenhou.net/0/?log=" + jsonChart.ref + "'>" + jsonChart.ref + "</a>",
            mouse: {
                track: true,
                lineColor: 'purple',
                position: 'sw',
                trackFormatter: function(e) {
                    var i = Math.floor(e.x);
                    if(i>0){
                        $('div#chart').accordion('select', ticks[i][1]);
                    }
                    return ticks[i][1] + ": " + Math.floor(e.y);
                }
            }
        });
};

var fillChart = function(jsonChart){
    var e = $('div#chart');
    $('#playerInfo').tree({data:playerDes(jsonChart), animate:true});
    for(var i=0;i<jsonChart.logs.length;i++){
        e.accordion('add',{
            title: jsonChart.logs[i].name,
            content: gameDes(jsonChart, i),
            selected: false,
            iconCls: 'icon-tip'
        });
    }
};

var sexDes = function(sex){
    if(sex=='M') return '男';
    else return '女';
}

var indexDes = function(index){
    return ['东', '南', '西', '北'][index];
}

var playerDes = function(jsonChart){
    var lst = [];
    var pls = [];
    for(var i=0;i<jsonChart.players.length;i++){
        pls.push(jsonChart.players[i]);
    }
    pls.sort(function(a, b){
        return b.score + b.index - a.score - a.index;
    });
    for(var i=0;i<pls.length;i++){
        var pl = pls[i];
        lst.push({
            text: pl.name,
            state: 'closed',
            children: [
                {text: "得分: " + pl.score},
                {text: "得点: " + pl.point},
                {text: "顺位: " + pl.rank},
                {text: "段位: " + pl.dan},
                {text: "Ｒ值: " + Math.floor(pl.rate)},
                {text: "起家: " + indexDes(pl.index)},
                {text: "性别: " + sexDes(pl.sex)}
            ]
        });
    }
    return lst;
};

var gameDes = function(jsonChart, index){
    var con = $("<div></div>");
    var log = jsonChart.logs[index];
    for(var i=0;i<log.changeScore.length;i++){
        if(!log.isDraw){
            var subtitle = "";
            var winner = jsonChart.players[log.winnerIndex[i]].name;
            subtitle += winner + " " + log.changeScoreDes[i];
            if(log.isZimo){
                subtitle += " 自摸";
                con.append($("<h3 id='subtitle_win'></h3>").text(subtitle));
            }else{
                con.append($("<h3 id='subtitle_win'></h3>").text(subtitle));
                var loser = jsonChart.players[log.loserIndex[i]].name;
                subtitle = loser + " 放铳" ;
                con.append($("<h4 id='subtitle_lose'></h3>").text(subtitle));
            }
            for(var j=0;j<log.yakus[i].length;j++){
                con.append($("<p id='yaku'></p>").text(log.yakus[i][j]));
            }
            con.append($("<div id='lastline'></div>"));
        }else{
            var header = $("<h3 id='subtitle_draw'></h3>").text(log.result);
            con.append(header);
        }
    }
    return con.html();
};



$(document).ready(
    function(){
        $.get("../API?method=logChart&ref=" + refCode, function(data,status){
            if(status!='success'){
                $("#container").text("获取数据失败，请刷新本页面");
            }else{
                $("#container").text("");
                jsonObj = JSON.parse(data);
                drawChart(jsonObj);
                fillChart(jsonObj);
            }
        });
    }
);