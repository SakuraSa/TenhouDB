var playerName = getQueryStringByName("name");
var lobby = getQueryStringByName("lobby");
var limit = getQueryStringByName("limit");
var before = getQueryStringByName("before");
var after = getQueryStringByName("after");
var morethan = getQueryStringByName("morethan");
var jsonObj;

var perStr = function(num){
    if(!num) return "0%";
    return Math.floor(num*1000000) / 10000 + "%";
};
var flStr = function(num){
    if(!num) return "0";
    return "" + Math.floor(num*10000) / 10000;
};
var inStr = function(num){
    if(!num) return "0";
    return "" + Math.floor(num);
};
var radar_number = function(num, maxV, minV, length){
    if(num < minV) num = minV;
    if(num > maxV) num = maxV;
    return (num - minV) * length / (maxV -minV);
};


var fillRadar = function(js){
    var container = document.getElementById("radar_container");
    var radar_length = 10;
    var dt = { label : decodeURI(playerName),
               data  : [[0, radar_number(js.winGame.avg, 0.30, 0.15, radar_length)], 
                        [1, radar_number(1 - js.winGame_fulu.per, 0.70, 0.35, radar_length)], 
                        [2, radar_number(js.winGame_score.avg, 7500, 5000, radar_length)], 
                        [3, radar_number(1 - js.chong.avg, 0.90, 0.80, radar_length)], 
                        [4, radar_number(js.richi_inner_dora.avg, 0.8, 0.3, radar_length)], 
                        [5, radar_number(20 - js.winGame_round.avg, 10.0, 7.0, radar_length)]] };
    var ticks =  [
        [0, "和了"],
        [1, "和门"],
        [2, "和点"],
        [3, "防御"],
        [4, "里宝"],
        [5, "和巡"]
    ];
    var graph = Flotr.draw(container, [ dt ], {
        radar : { show : true}, 
        grid  : { circular : true, minorHorizontalLines : true}, 
        yaxis : { min : 0, max : radar_length, minorTickFreq : 2}, 
        xaxis : { ticks : ticks},
        mouse : { 
            track : true,
            lineColor: 'purple',
            position: 'sw',
            trackFormatter: function(e) {
                var i = Math.floor(e.x);
                if(i == 0){
                    return "胜率: " + perStr(js.winGame.avg);
                }else if(i == 1){
                    return "门清率: " + perStr(1 - js.fulu.avg);
                }else if(i == 2){
                    return "胜场平均得点: " + inStr(js.winGame_score.avg);
                }else if(i == 3){
                    return "铳率: " + perStr(js.chong.avg);
                }else if(i == 4){
                    return "平均里dora数: " + flStr(js.dora_inner.avg);
                }else if(i == 5){
                    return "平均和巡: " + flStr(js.winGame_round.avg);
                }
                return "unknow";
            }
    }
    });

};

var fillChart = function(js){
    var data = [];

    data.push(
        {text: "统计局数: " + js.games}
    );

    data.push(
        {text: "顺位", children: [
            {text: "综合", children: [
                {text: "平均: " + flStr(js.total.avg)},
                {text: "一位: " + perStr(js.total.groupPercent[1])},
                {text: "二位: " + perStr(js.total.groupPercent[2])},
                {text: "三位: " + perStr(js.total.groupPercent[3])},
                {text: "四位: " + perStr(js.total.groupPercent[4])},
            ]},
            {text: "东起", children: [
                {text: "平均: " + flStr(js.east.avg)},
                {text: "一位: " + perStr(js.east.groupPercent[1])},
                {text: "二位: " + perStr(js.east.groupPercent[2])},
                {text: "三位: " + perStr(js.east.groupPercent[3])},
                {text: "四位: " + perStr(js.east.groupPercent[4])},
            ]},
            {text: "南起", children: [
                {text: "平均: " + flStr(js.south.avg)},
                {text: "一位: " + perStr(js.south.groupPercent[1])},
                {text: "二位: " + perStr(js.south.groupPercent[2])},
                {text: "三位: " + perStr(js.south.groupPercent[3])},
                {text: "四位: " + perStr(js.south.groupPercent[4])},
            ]},
            {text: "西起", children: [
                {text: "平均: " + flStr(js.west.avg)},
                {text: "一位: " + perStr(js.west.groupPercent[1])},
                {text: "二位: " + perStr(js.west.groupPercent[2])},
                {text: "三位: " + perStr(js.west.groupPercent[3])},
                {text: "四位: " + perStr(js.west.groupPercent[4])},
            ]},
            {text: "北起", children: [
                {text: "平均: " + flStr(js.north.avg)},
                {text: "一位: " + perStr(js.north.groupPercent[1])},
                {text: "二位: " + perStr(js.north.groupPercent[2])},
                {text: "三位: " + perStr(js.north.groupPercent[3])},
                {text: "四位: " + perStr(js.north.groupPercent[4])},
            ]},
        ]}
    );

    data.push(        
        {text: "场终得分", children: [
            {text: "平均: " + inStr(js.endScore.avg)},
            {text: "最大: " + inStr(js.endScore.max)},
            {text: "最小: " + inStr(js.endScore.min)},
        ]}
    );

    data.push(
        {text: "负分出局", children: [
            {text: "自己", children: [
                {text: "频率: " + perStr(js.minusScore.avg)},
                {text: "次数: " + inStr(js.minusScore.sum)},
            ]},
            {text: "它人", children: [
                {text: "频率: " + perStr(js.minusOther.avg)},
                {text: "次数: " + inStr(js.minusOther.sum)},
                {text: "人数: " + inStr(js.minusOther.plr)},
            ]},
        ]}
    );

    data.push(
        {text: "dora", children: [
            {text: "综合", children: [
                {text: "平均: " + flStr(js.dora.avg)},
                {text: "最大: " + inStr(js.dora.max)},
            ]},
            {text: "里dora", children: [
                {text: "平均: " + flStr(js.dora_inner.avg)},
                {text: "最大: " + inStr(js.dora_inner.max)},
            ]},
        ]}
    );

    data.push(
        {text: "胜场", children: [
            {text: "频率: " + perStr(js.winGame.avg)},
            {text: "得分", children: [
                {text: "平均: " + flStr(js.winGame_score.avg)},
                {text: "最大: " + inStr(js.winGame_score.max)},
            ]},
            {text: "自亲", children: [
                {text: "频率: " + perStr(js.winGame_host.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.winGame_host.avg)},
                    {text: "最大: " + inStr(js.winGame_host.max)},
                ]},
            ]},
            {text: "自摸", children: [
                {text: "频率: " + perStr(js.winGame_zimo.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.winGame_zimo.avg)},
                    {text: "最大: " + inStr(js.winGame_zimo.max)},
                ]},
            ]},
            {text: "荣和", children: [
                {text: "频率: " + perStr(js.winGame_rong.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.winGame_rong.avg)},
                    {text: "最大: " + inStr(js.winGame_rong.max)},
                ]},
            ]},
            {text: "副露", children: [
                {text: "频率: " + perStr(js.winGame_fulu.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.winGame_fulu.avg)},
                    {text: "最大: " + inStr(js.winGame_fulu.max)},
                ]},
            ]},
            {text: "立直", children: [
                {text: "频率: " + perStr(js.winGame_richi.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.winGame_richi.avg)},
                    {text: "最大: " + inStr(js.winGame_richi.max)},
                ]},
            ]},
            {text: "默听", children: [
                {text: "频率: " + perStr(js.winGame_dama.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.winGame_dama.avg)},
                    {text: "最大: " + inStr(js.winGame_dama.max)},
                ]},
            ]},
            {text: "巡目", children: [
                {text: "平均: " + flStr(js.winGame_round.avg)},
                {text: "最小: " + inStr(js.winGame_round.min)},
            ]},
        ]}
    );

    data.push(
        {text: "副露", children: [
            {text: "频率: " + perStr(js.fulu.avg)},
            {text: "胜率: " + perStr(js.fulu_winGame.per)},
            {text: "得分", children: [
                {text: "平均: " + flStr(js.fulu_score.avg)},
                {text: "最大: " + inStr(js.fulu_score.max)},
            ]},
            {text: "自摸", children: [
                {text: "频率: " + perStr(js.fulu_zimo.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.fulu_zimo.avg)},
                    {text: "最大: " + inStr(js.fulu_zimo.max)},
                ]},
            ]},
            {text: "荣和", children: [
                {text: "频率: " + perStr(js.fulu_rong.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.fulu_rong.avg)},
                    {text: "最大: " + inStr(js.fulu_rong.max)},
                ]},
            ]},
            {text: "放铳", children: [
                {text: "频率: " + perStr(js.fulu_chong.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.fulu_chong.avg)},
                    {text: "最大: " + inStr(js.fulu_chong.min)},
                ]},
            ]},
        ]}
    );

    data.push(
        {text: "放铳", children: [
            {text: "频率: " + perStr(js.chong.avg)},
            {text: "得分", children: [
                {text: "平均: " + flStr(js.chong_score.avg)},
                {text: "最大: " + inStr(js.chong_score.min)},
            ]},
            {text: "自亲", children: [
                {text: "频率: " + perStr(js.chong_host.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.chong_host.avg)},
                    {text: "最大: " + inStr(js.chong_host.min)},
                ]},
            ]},
            {text: "副露", children: [
                {text: "频率: " + perStr(js.chong_fulu.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.chong_fulu.avg)},
                    {text: "最大: " + inStr(js.chong_fulu.min)},
                ]},
            ]},
            {text: "立直", children: [
                {text: "频率: " + perStr(js.chong_richi.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.chong_richi.avg)},
                    {text: "最大: " + inStr(js.chong_richi.min)},
                ]},
            ]},
        ]}
    );

    data.push(
        {text: "被自摸", children: [
            {text: "频率: " + perStr(js.otherZimo.avg)},
            {text: "得分", children: [
                {text: "平均: " + flStr(js.otherZimo_score.avg)},
                {text: "最大: " + inStr(js.otherZimo_score.min)},
            ]},
            {text: "自亲", children: [
                {text: "频率: " + perStr(js.dehost.avg)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.dehost_score.avg)},
                    {text: "最大: " + inStr(js.dehost_score.min)},
                ]},
            ]},
        ]}
    );

    data.push(
        {text: "立直", children: [
            {text: "频率: " + perStr(js.richi.avg)},
            {text: "胜率: " + perStr(js.richi_winGame.per)},
            {text: "得分", children: [
                {text: "平均: " + flStr(js.richi_score.avg)},
                {text: "最大: " + inStr(js.richi_score.max)},
                {text: "最小: " + inStr(js.richi_score.min)},
            ]},
            {text: "一发", children: [
                {text: "频率: " + perStr(js.richi_yifa.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.richi_yifa.avg)},
                    {text: "最大: " + inStr(js.richi_yifa.max)},
                ]},
            ]},
            {text: "自摸", children: [
                {text: "频率: " + perStr(js.richi_zimo.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.richi_zimo.avg)},
                    {text: "最大: " + inStr(js.richi_zimo.max)},
                ]},
            ]},
            {text: "荣和", children: [
                {text: "频率: " + perStr(js.richi_rong.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.richi_rong.avg)},
                    {text: "最大: " + inStr(js.richi_rong.max)},
                ]},
            ]},
            {text: "放铳", children: [
                {text: "频率: " + perStr(js.richi_chong.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.richi_chong.avg)},
                    {text: "最大: " + inStr(js.richi_chong.min)},
                ]},
            ]},
            {text: "被自摸", children: [
                {text: "频率: " + perStr(js.richi_otherZimo.per)},
                {text: "得分", children: [
                    {text: "平均: " + flStr(js.richi_otherZimo.avg)},
                    {text: "最大: " + inStr(js.richi_otherZimo.min)},
                ]},
            ]},
            {text: "流局", children: [
                {text: "频率: " + perStr(js.richi_draw.per)},
            ]},
        ]}
    );

    if(js.yakus){
        var yakus = js.yakus.sort(function(a, b){return b[0] - a[0];});
        var ch = [];
        for(i=0;i<yakus.length;i++){
            var pair = yakus[i];
            ch.push(
                {text: pair[1], children: [
                    {text: "频率: " + perStr(pair[0] / js.winGame.len)},
                    {text: "总计: " + inStr(pair[0])},
                ]}
            );
        }
        data.push({text: "役", children: ch});
    }

    $('#sttree').tree({data:data, animate:true});
    $('#sttree').tree('collapseAll');
};

$(document).ready(
    function(){
        if(playerName){
            var APIurl = "../API?method=statistics";
            if(playerName) APIurl += "&name=" + playerName;
            if(lobby) APIurl += "&lobby=" + lobby;
            if(limit) APIurl += "&limit=" + limit;
            if(before) APIurl += "&before=" + before;
            if(after) APIurl += "&after=" + after;
            if(morethan) APIurl += "&morethan=" + morethan;
            $("p#info").text("Loading...");
            $.get(APIurl, function(data,status){
                if(status=='success'){
                    if(data.substring(0,5) == "error"){
                        $("p#info").text(data);
                    }else{
                        $("p#info").text("");
                        jsonObj = JSON.parse(data);
                        fillRadar(jsonObj);
                        fillChart(jsonObj);
                    }
                }else{
                    $("p#info").text(data);
                }
            });
        }
    }
);