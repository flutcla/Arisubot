import re
import requests
from time import sleep
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, List
from myutils.get_data_from_json import get_data_from_json


def api(token: str):
    # throws urllib.error.HTTPError
    request_head = "https://pink-check.school/api/v1/"
    request = request_head + token
#    with urllib.request.urlopen(request) as res:
#        body = res.read()
    body = requests.get(request)
    body.raise_for_status()
    data = json.loads(body.text)
    sleep(1)
    return data


# 現在開催中のイベント情報を抽出する
def get_event():
    time = datetime.now()
    for _ in range(24):
        try:
            event_data = api("events/?time={}".format(time.strftime('%Y-%m-%dT%H:%M:%S')))
            break
        except requests.exceptions.HTTPError:
            time -= timedelta(hours=1)
            continue
    else:
        raise RuntimeError("There is no nearly held event or API error.")
    return event_data


# メッセージとサーバIDからプロダクションIDを抽出する
def get_pro_id(message: str, server_id: str = "0"):
    msg = message.split()
    if len(msg) == 1:
        server_pro_dict = get_data_from_json(Path.cwd()/"imcgapi"/"server_pro_dict.json")
        if server_id in server_pro_dict.keys():
            return server_pro_dict[server_id]
        else:
            raise KeyError("The server({0}) haven't been registered.".format(server_id))
    elif len(msg) == 2:
        pro_id_list = get_data_from_json(Path.cwd()/"imcgapi"/"pro_id_list.json")
        for key, value in pro_id_list.items():
            if re.search(key, msg[1], re.I):
                return value
        else:
            return msg[1]
    else:
        raise SyntaxError("The command is wrong.")


# プロダクションIDからプロメンと正式名称を抽出する
def get_pro_member(pro_id: str, pro_name: str = "None") -> Tuple[str, List[str]]:
    token = "producers?productionId={0}".format(pro_id)
    data = api(token)
    member = list()
    if len(data) != 0:
        pro_name = list(data.values())[0]["productionName"]
        member += [str(p['mobageId']) for p in data.values()]
    additional_pro_member = get_data_from_json(Path.cwd()/"imcgapi"/"additional_pro_member.json")
    if pro_id in additional_pro_member.keys():
        member += additional_pro_member[pro_id]["member"]["ID"]
    return pro_name, member
