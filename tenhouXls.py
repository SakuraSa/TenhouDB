#!/usr/bin/env python
#coding=utf-8

import os
import xlwt
import tenhouDB

xlsDir = r"static/xls/"
host = r"http://tenhou.net/0/?log="

dxnb = [u"东", u"南", u"西", u"北"]
numb = [u"零", u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"]
numx = [u"", u"十", u"百", u"千", u"万", ]

def chnum(num):
    num = abs(int(num))
    if num == 0:
        return numb[num]
    s = u""
    upper = False
    for lvl in range(10, -1, -1):
        x = num / (10 ** lvl)
        if x:
            upper = True
            num -= x * (10 ** lvl)
            s += numb[x] + numx[lvl]
        elif upper:
            upper = False
            s += numb[x]
    return s

def gameIndexDes(indexTuple):
    changfeng = dxnb[indexTuple[0] / 4]
    changshu  = chnum(indexTuple[0] % 4 + 1)
    changju   = indexTuple[1]
    return u"%s%s局%s本场" % (changfeng, changshu, changju)

def createXLS(obj):
    if len(obj["name"]) != 4:
        raise Exception("Not 4 Player Game, skipped.")
      
    wbName = obj["ref"] + ".xls"
    if not os.path.exists(xlsDir):
        os.makedirs(xlsDir)
    if os.path.exists(os.path.join(xlsDir, wbName)):
        return os.path.join(xlsDir, wbName)

    wb = xlwt.Workbook()

    al = xlwt.Alignment()
    al.horz = xlwt.Alignment.HORZ_CENTER
    al.vert = xlwt.Alignment.VERT_CENTER

    font_header = xlwt.Font()
    font_header.name = u"黑体"
    font_header.bold = True
    border_header = xlwt.Borders()
    border_header.left = 1
    border_header.right = 1
    border_header.top = 1
    border_header.bottom = 1
    style_header = xlwt.XFStyle()
    style_header.font = font_header
    style_header.borders = border_header
    style_header.alignment = al

    font_value = xlwt.Font()
    font_value.name = u"宋体"
    font_value.bold = False
    border_value = xlwt.Borders()
    border_value.left = 1
    border_value.right = 1
    border_value.top = 1
    border_value.bottom = 1
    style_value = xlwt.XFStyle()
    style_value.font = font_value
    style_value.borders = border_value
    style_value.alignment = al

    #玩家信息
    ws_player = wb.add_sheet(u"玩家信息")

    ws_player.col(0).width = 0x0f00

    titles = [u"ID", u"性别", u"起家", u"段数", u"R值", u"得分", u"得点", u"顺位"]
    for i in range(len(titles)):
        ws_player.write(0, i, titles[i], style_header)
    orders = [(obj["sc"][i * 2], 4 - i, i) for i in range(4)]
    orders.sort(reverse = True)
    orders = [i[2] for i in orders]
    orders = [orders.index(i) for i in range(4)]
    for i in range(4):
        ws_player.write(i + 1, 0, obj["name"][i], style_value)
        ws_player.write(i + 1, 1, u"基佬" if obj["sx"][i] == "M" else u"妹子", style_value)
        ws_player.write(i + 1, 2, dxnb[i], style_value)
        ws_player.write(i + 1, 3, obj["dan"][i], style_value)
        ws_player.write(i + 1, 4, int(obj["rate"][i]), style_value)
        ws_player.write(i + 1, 5, obj["sc"][i * 2], style_value)
        ws_player.write(i + 1, 6, obj["sc"][i * 2 + 1], style_value)
        ws_player.write(i + 1, 7, u"第%s名" % chnum(orders[i] + 1), style_value)
    ws_player.write(5, 0, u"连接", style_header)
    ws_player.write_merge(5, 5, 1, 7, 
        xlwt.Formula('HYPERLINK("%s%s&tw=2";"%s")' % (host, obj["ref"], obj["ref"])), 
        style_value)

    #对局分数信息
    ws_score = wb.add_sheet(u"对局分数信息")

    lastCol = 2 + len(obj["log"])
    ws_score.col(0).width = 0x0a00
    ws_score.col(1).width = 0x0f00
    for i in range(2, lastCol + 1):
        ws_score.col(i).width = 0x1500

    ws_score.write_merge(0, 0, 0, 1, u"序号", style_header)
    ws_score.write_merge(1, 1, 0, 1, u"场次", style_header)
    ws_score.write_merge(2, 5, 0, 0, u"起家", style_header)
    for i in range(4):
        ws_score.write(2 + i, 1, obj["name"][i], style_header)
    ws_score.write_merge(6, 9, 0, 0, u"分数变动", style_header)
    for i in range(4):
        ws_score.write(6 + i, 1, obj["name"][i], style_header)
    ws_score.write_merge(10, 13, 0, 0, u"起手分数", style_header)
    for i in range(4):
        ws_score.write(10 + i, 1, obj["name"][i], style_header)
    ws_score.write_merge(14, 17, 0, 0, u"当前排位", style_header)
    for i in range(4):
        ws_score.write(14 + i, 1, u"第%s位" % numb[i + 1], style_header)
    ws_score.write_merge(18, 28, 0, 0, u"役", style_header)
    ws_score.write(18, 1, u"符与飜", style_header)
    for i in range(10):
        ws_score.write(19 + i, 1, u"第%2d种役" % (i + 1), style_header)

    for i in range(len(obj["log"])):
        ws_score.write(0, 2 + i, i + 1, style_value)
        ws_score.write(1, 2 + i, gameIndexDes(obj["log"][i][0]), style_value)
        while not obj["log"][-1]:
            obj["log"].pop()
        rRow = obj["log"][i][-1]
        for j in range(4):
            ws_score.write(2 + j, 2 + i, dxnb[(j + obj["log"][i][0][0]) % 4], style_value)
            if len(rRow) > 2:
                ws_score.write(6 + j, 2 + i, rRow[1][j], style_value)
            else:
                ws_score.write(6 + j, 2 + i, 0, style_value)
            ws_score.write(10 + j, 2 + i, obj["log"][i][1][j], style_value)
        orders    = [(obj["log"][i][1][j] + (rRow[1][j] if len(rRow) > 2 else 0), 4 - j, j) for j in range(4)]
        orders.sort(reverse = True)
        for j in range(4):
            ws_score.write(14 + j, 2 + i, obj["name"][orders[j][2]], style_value)
        if len(rRow) > 2:
            ws_score.write(18, 2 + i, rRow[2][3], style_value)
            for j in range(len(rRow[2]) - 4):
                ws_score.write(19 + j, 2 + i, rRow[2][4 + j], style_value)
            for j in range(len(rRow[2]) - 4, 10):
                ws_score.write(19 + j, 2 + i, u"", style_value)
        else:
            ws_score.write(18, 2 + i, rRow[0], style_value)
            for j in range(10):
                ws_score.write(19 + j, 2 + i, u"", style_value)

    ws_score.write_merge(0, 9, lastCol, lastCol, u"对局结果", style_value)
    for i in range(4):
        ws_score.write(10 + i, lastCol, obj["sc"][i * 2], style_value)
        orders = [(obj["sc"][j * 2], 4 - j, j) for j in range(4)]
        orders.sort(reverse = True)
        ws_score.write(14 + i, lastCol, obj["name"][orders[i][2]], style_value)
    ws_score.write_merge(18, 28, lastCol, lastCol, u"", style_value)

    wb.save(os.path.join(xlsDir, wbName))

    return os.path.join(xlsDir, wbName)

if __name__ == "__main__":
    fn = "urls.txt"
    with open(fn, "r") as f:
        lines = f.read()

    for success, obj in tenhouDB.addLogs(lines):
        if success:
            #try:
                createXLS(obj)
            #    print obj["ref"], "ok!"
            #except Exception, e:
            #    print obj["ref"], "Error:", e
        else:
            print obj