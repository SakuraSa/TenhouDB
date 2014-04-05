var jsonObj;

var perStr = function(num){
    if(!num) return "0%";
    return Math.floor(num*10000) / 100 + "%";
};
var flStr = function(num){
    if(!num) return "0";
    return "" + Math.floor(num*100) / 100;
};
var inStr = function(num){
    if(!num) return "0";
    return "" + Math.floor(num);
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

    $('#sttree').tree({data:data, animate:true});
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
            $("p#info").text("Loading...");
            $.get(APIurl, function(data,status){
                if(status=='success'){
                    if(data.substring(0,5) == "error"){
                        $("p#info").text(data);
                    }else{
                        $("p#info").text("");
                        jsonObj = JSON.parse(data);
                        fillChart(jsonObj);
                    }
                }else{
                    $("p#info").text(data);
                }
            });
        }
    }
);