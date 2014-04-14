function drawTable(data){
    var table = $("#hotIDs");
    for(var i = 0; i<data.length; i++){
        var tr = $("<tr></tr>");
        tr.append($("<td></td>").html("" + (i + 1)));
        tr.append($("<td></td>").append($("<a></a>").html(data[i].name).attr("href", "../playerLogs?name="+data[i].name)));
        tr.append($("<td></td>").html("" + data[i].count));
        tr.append($("<td></td>")
                  .append($("<a></a>")
                  .text("统计")
                  .attr("href", "../statistics?name=" + data[i].name)));
        table.append(tr);
    }

}

$(document).ready(
    function(){
        var limit = getQueryStringByName("limit");
        if(!limit) limit = 10;
        $.get("../API?method=hotIDs&limit=" + limit, function(data,status){
            if(status!='success'){
                $("p#info").text("网络出错，请刷新").css("color", "red");
            }else{
                $("p#info").text("");
                jsonObj = JSON.parse(data);
                drawTable(jsonObj);
            }
        });
    }
);