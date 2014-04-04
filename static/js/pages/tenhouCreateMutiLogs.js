$(document).ready(function(){
    var refLst = [];

    $("textarea#refs").change(function(){
        var patt = /\d{10}gm-\w{4}-\d{4,5}-\w{8}/g;
        var m;
        $("div#res").empty();
        refLst = [];
        while((m = patt.exec($("textarea#refs").val()))){
            refLst.push(m[0]);
        }
        $("p#st").text("记录:" + refLst.length);
    });

    var pushRef = function(ref){
        var obj = $("<a></a>").text(ref + " loading...");
        $("div#res").append(obj);
        $("div#res").append($("<br>"));
        $.get("../API?method=createLog&ref=" + ref,function(data, status){
            obj.text(ref + " " + data);
            if(data == "ok"){
                obj.attr("href", "../tenhouCreateLog?ref=" + ref);
            }
            if(refLst.length > 0){
                pushRef(refLst.pop());
            }
        })
    };

    $("button#submit").click(function(){
        $("div#res").empty();
        if(refLst.length > 0){
            pushRef(refLst.pop());
        }
    });
});