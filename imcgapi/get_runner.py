from imcgapi.imcgapi import *
from requests.exceptions import HTTPError


# イベント種別ID
# ツアー(旧方式): 1、アイプロ: 2、ドリフェス: 3、アイバラ: 4、ぷちコレ: 5、フェス: 6アイチャレ: 7
# アイロワ: 8、TBS: 9、フェスS: 10、アニバアイプロ: 11、ツアーカーニバル: 12、TBSオールスターSP: 13
# 復刻アイプロ: 14、復刻アイチャレ: 15、ミュージックJAM: 16、復刻ツアー: 17
# 追加報酬ID
# プロダクション: 2、ミニチーム: 3、なし: 0


# イベント走者情報を調べる
def get_runner(message: str, server_id: str, server_name: str) -> str:
    try:
        pro_id = get_pro_id(message, server_id)
    except KeyError:
        return "プロダクションIDとサーバーの紐付けがされていません。bot管理者に問い合わせてください。"
    pro_name, member = get_pro_member(pro_id)

    if not pro_name:
        try:
            pro_name = message.split()[1]
        except IndexError:
            pro_name = server_name

    event_data = list(get_event().values())[0]
    event_detail = list(event_data["details"].values())[0]

    event = {
        "name": event_data["name"],
        "detailId": event_detail["eventDetailId"],
    }

    time_now = datetime.now()
    time_search = time_now - timedelta(minutes=time_now.minute, seconds=time_now.second,
                                       microseconds=time_now.microsecond)
    for _ in range(24):
        get_ranking_token = "eventdetails/{0}/rankings?rankingTypeId={1}&time={2}&targetId={3}".format(
            event["detailId"], 1, time_search.strftime("%Y-%m-%dT%H:00:00"), ",".join(member)
        )
        try:
            ranking = api(get_ranking_token)
            break
        except HTTPError:
            time_search -= timedelta(hours=1)
            continue
    else:
        ranking = dict()

    if not ranking:
        return "{0} では、現在のイベント {1} を走っている人は確認できませんでした。".format(pro_name, event["name"])

    running_members = list(ranking.values())[0]
    reply = "{0} の順位情報を連絡します。\n{1} では {2} 時点で\n".format(
        event["name"], pro_name, time_search.strftime('%Y-%m-%d %H:00')
    )
    for member in running_members:
        reply += "{0} さんが {1} 位({2}pts)\n".format(member["name"], member["rank"], member["point"])
    reply += "です。プロデューサーさん、頑張ってください。"
    return reply
