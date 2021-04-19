from typing import Dict
import json
from pathlib import Path
from time import sleep


LOCKED = False


def get_data_from_json(path: Path) -> Dict:
    global LOCKED
    while LOCKED:
        sleep(1)
    LOCKED = True
    if '.json' == path.suffix:
        raise ValueError('ファイルの拡張子がJSONではありません。')
    with path.open(encoding="utf-8_sig") as file:
        data = json.load(file)
    LOCKED = False
    return data


def write_data_to_json(path: Path, data: Dict):
    global LOCKED
    while LOCKED:
        sleep(1)
    LOCKED = True
    if '.json' == path.suffix:
        raise ValueError('ファイルの拡張子がJSONではありません。')
    with path.open(encoding="utf-8_sig", mode="w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    LOCKED = False
