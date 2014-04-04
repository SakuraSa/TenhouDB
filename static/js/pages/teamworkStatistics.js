$(document).ready(function(){
    var refLst = [];
    var logs = [];

    $("textarea#refs").change(function(){
        var patt = /\d{10}gm-\w{4}-\d{4,5}-\w{8}/g;
        var m;
        $("div#res").empty();
        refLst = [];
        logs = [];
        while((m = patt.exec($("textarea#refs").val()))){
            refLst.push(m[0]);
        }
        $("p#st").text("记录:" + refLst.length);
    });

    var pushRef = function(ref){
        var obj = $("<a></a>").text(ref + " loading...");
        $("div#res").append(obj);
        $("div#res").append($("<br>"));
        $.get("../API?method=getLogJson&ref=" + ref,function(data, status){
            var patt = /^error/;
            if(patt.test(data)){
                obj.text(ref + " " + data);
            }else{
                obj.text(ref + " " + status);
                obj.attr("href", "../tenhouCreateLog?ref=" + ref);
                logs.push(JSON.parse(data));
            }
            if(refLst.length > 0){
                pushRef(refLst.pop());
            }else{
                statistic();
            }
        })
    };

    var statistic = function(){
        var playerSC = {};
        for(var i=0;i<logs.length;i++){
            if(logs[i].name.length != 4)
                continue;
            for(var j=0;j<4;j++){
                var name = logs[i].name[j];
                var dj = (j + 2) % 4;
                var scSum = logs[i].sc[j * 2] + logs[i].sc[dj * 2];
                if(!playerSC[name])
                    playerSC[name] = 0;
                playerSC[name] += ptFunc(scSum);
            }
        }
        var obj = $("<a></a>").text("Ranking:");
        $("div#res").append(obj);
        $("div#res").append($("<br>"));
        var order = [];
        for(var name in playerSC){
            order.push([name, playerSC[name]])
        }
        order.sort(function(a, b){
            return b[1] - a[1];
        });
        for(var i = 0;i < order.length;i++){
            var obj = $("<a></a>").text((i + 1).toString() + ". " + order[i][0] + ": " + order[i][1]);
            $("div#res").append(obj);
            $("div#res").append($("<br>"));
        }
    }

    var ptFunc = function(sc){
        if(sc>=50000){
            return 25 * ( 2 + (sc - 50000) / 50000 * (sc - 50000) / 50000 + Math.tan((sc - 50000) / 200000 / Math.PI) );
        }else{
            sc = 100000 - sc;
            return 100 - 25 * ( 2 + (sc - 50000) / 50000 * (sc - 50000) / 50000 + Math.tan((sc - 50000) / 200000 / Math.PI) );
        }
    }

    $("button#submit").click(function(){
        $("div#res").empty();
        if(refLst.length > 0){
            pushRef(refLst.pop());
        }
    });
});