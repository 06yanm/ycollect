from flask import Flask, render_template, request, jsonify
import json,time
import os, webbrowser, threading,sys
import requests
from colorama import init, Fore
import logging

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def chunk_list(lst, chunk_size):
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

if getattr(sys, 'frozen', False):
    datapath = os.path.dirname(sys.executable)
else:
    datapath = os.path.dirname(__file__)

datajson = os.path.join(datapath, "data.json")
portfile = os.path.join(datapath, "port.txt")
with open(portfile, "r", encoding="utf-8") as file:
    porth = int(file.read())

@app.route('/', methods=["GET"])
def index():
    data = ""
    with open(datajson, "r", encoding="utf-8") as file:
        data = file.read()
    content = json.loads(data)
    for item in content["body"]:
        if item["type"] == 0:
            item["content"] = chunk_list(item["content"], 3)
        else:
            item["content"] = chunk_list(item["content"], 2)
    return render_template("index.html", datas=content, port=porth)

@app.route("/addWebsite", methods=["POST"])
def addWebsite():
    name = request.form.get("name")
    url = request.form.get("url")
    describe = request.form.get("describe")
    notice = request.form.get("notice")
    is_vpn = request.form.get("is-vpn")
    category = request.form.get("category")
    if not all([name, url, describe,  is_vpn, category]):
        return render_template("goto.html", say="参数不全", title="操作失败")
    with open(datajson, "r", encoding="utf-8") as file:
        d = json.loads(file.read())
    webid = int(time.time())
    for cate in d["body"]:
        if cate["id"] == int(category):
            cate["content"].append({
                    "id": webid,
                    "pass": 0,
                    "username": "",
                    "password": "",
                    "is_vpn": int(is_vpn),
                    "facvion": f"{url}favicon.ico",
                    "name": name,
                    "descripition": describe,
                    "notice": notice,
                    "url": url
            })
    try:
        with open(f"./static/icons/{webid}.ico", "w") as file:
            file.write(requests.get(f"{url}favicon.ico").content)
    except Exception as e:
        print(e)

    with open(datajson, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)
    
    return render_template("goto.html", say="添加成功", title="操作成功")

@app.route("/addCategory", methods=["POST"])
def addCategory():
    name = request.form.get("categoryname")
    categoryType = request.form.get("categorytype")
    if not all([name, categoryType]):
        return render_template("goto.html", say="参数不全", title="操作失败")
    with open(datajson, "r", encoding="utf-8") as file:
        d = json.loads(file.read())
    d["body"].append({
        "id": int(time.time()) ,
        "tag": name,
        "type": int(categoryType),
        "content": []
    })

    with open(datajson, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

    return render_template("goto.html", say="添加成功", title="操作成功")

@app.route("/deleteCategory", methods=["POST"])
def deleteCategory():
    id = request.form.get("categoryid")
    if not id:
        return render_template("goto.html", say="删除失败", title="操作失败")
    with open(datajson, "r", encoding="utf-8") as file:
        d = json.loads(file.read())
    new = {
        "logo": d["logo"],
        "name": d["name"],
        "body": []
    }
    for item in d["body"]:
        if item["id"] != int(id):
            new["body"].append(item)
    with open(datajson, 'w', encoding='utf-8') as f:
        json.dump(new, f, ensure_ascii=False, indent=4)
    return render_template("goto.html", say="删除成功", title="操作成功")

@app.route("/deleteWebsite", methods=["POST"])
def deleteWebsite():
    cate_id = request.form.get("cate-id")
    web_id = request.form.get("web-id")
    if not all([cate_id, web_id]):
        return render_template("goto.html", say="参数不全", title="操作失败")
    cate_id = cate_id.replace("v", "")
    with open(datajson, "r", encoding="utf-8") as file:
        d = json.loads(file.read())
    new = {
        "logo": d["logo"],
        "name": d["name"],
        "body": []
    }
    i = 0
    for data in d["body"]:
        new["body"].append({
            "id": data["id"],
            "tag": data["tag"],
            "type": data["type"],
            "content": []
        })
        for c in data["content"]:
            if c["id"] != int(web_id):
                new["body"][i]["content"].append(c)
        i += 1

    with open(datajson, 'w', encoding='utf-8') as f:
        json.dump(new, f, ensure_ascii=False, indent=4)

    return render_template("goto.html", say="删除成功", title="操作成功")

@app.route("/editWebsite", methods=["POST"])
def edit_website():
    web_id = request.form.get("e-web-id")
    category_id = request.form.get("e-category-id")
    web_name = request.form.get("e-web-name")
    web_describe = request.form.get("e-web-describe")
    web_url = request.form.get("e-web-url")
    is_vpn = request.form.get("e-is-vpn")
    notice = request.form.get("e-web-notice")
    y_category_id = request.form.get("e-y-category-id")
    facvion_url = request.form.get("icons-url")
    if not all([web_describe, web_id, web_name, web_url, category_id, is_vpn, y_category_id]):
        return render_template("goto.html", say="参数不全", title="操作失败")
    
    with open(datajson, "r", encoding="utf-8") as file:
        d = json.loads(file.read())

    for category in d["body"]:
        if category["id"] == int(y_category_id):
            for item in category["content"]:
                if item["id"] == int(web_id):
                   category["content"] = [one for one in category["content"] if one["id"] != int(web_id)]
    for category in d["body"]:
        if category["id"] == int(category_id):
            category["content"].append({
                    "id": int(web_id),
                    "pass": 0,
                    "username": "",
                    "password": "",
                    "is_vpn": int(is_vpn),
                    "facvion": f"./static/icons/{web_id}.ico",
                    "name": web_name,
                    "descripition": web_describe,
                    "notice": notice,
                    "url": web_url
            })
    try:
        with open(f"./static/icons/{web_id}.ico", "w") as file:
            file.write(requests.get(facvion_url).content)
    except Exception as e:
        print(e)

    with open(datajson, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)
    return render_template("goto.html", say="修改成功", title="操作成功")
    # return f"{web_id} + {category_id} + {web_name} + {web_describe} + {web_url} + {is_vpn} + {notice}"


@app.route("/getWebInfo", methods=["GET"])
def get_web_info():
    category = request.args.get("category")
    webid = request.args.get("website")
    if not all([category, webid]):
        return jsonify({"code": 400, "data": {}})
    category = category.replace("v", "")
    with open(datajson, "r", encoding="utf-8") as file:
        data = file.read()
    info = {}
    datas = json.loads(data)
    for cate in datas["body"]:
        if cate["id"] == int(category):
            for item in cate["content"]:
                if item["id"] == int(webid):
                    info = item
                    info["categoryid"] = cate["id"]
    if not info:
        return jsonify({"code": 400, "data": {}})
    else:
        return jsonify({"code": 200, "data": info})
    

def open_browser():
    webbrowser.open_new(f'http://127.0.0.1:{porth}/')
                
if __name__ == "__main__":
    threading.Timer(0.5, open_browser).start()
    print(f"收藏夹服务运行中...")
    print(f"请访问：\n")
    print(Fore.GREEN + f"http://127.0.0.1:{porth}\n" + Fore.WHITE)
    print(f"（Ctrl + 单击 以快速打开）\n\n如需关闭服务，直接关闭本终端窗口即可\n\n")
    app.run(port=porth)
    