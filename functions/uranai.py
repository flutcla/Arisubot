import random

fortune = {"大吉": 30, "中吉": 20, "吉": 20, "凶": 20, "大凶": 7,
           "特殊吉": 3}

special = {"スタ吉": 10, "エナ吉": 10, "鍵クロ吉": 1, "ガシャ吉": 10}

item = {"スタミナドリンク", "エナジードリンク", "鍵付きクローゼット",
        "LPドリンク", "APドリンク", "BPドリンク", "TPキャンディー",
        "CPブレッド", "EPドリンク", "SPゼリー", "エナドリチャージ10"}

comment = {"大吉": []}


def omikuji(name: str):
    result = random.choices(fortune.keys(), weights=fortune.values())
    if result == "大吉":
        comment = f"{name}さんの運勢は、{result}です。"
