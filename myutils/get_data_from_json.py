from typing import Dict
import json
from pathlib import Path


def get_data_from_json(path: Path) -> Dict:
    if 'json' not in path.name:
        raise ValueError('ファイルの拡張子がJSONではありません。')
    with path.open(encoding="utf-8_sig") as file:
        data = json.load(file)
    return data


def write_data_to_json(path: Path, data: Dict):
    if 'json' not in path.name:
        raise ValueError('ファイルの拡張子がJSONではありません。')
    with path.open(encoding="utf-8_sig", mode="w") as file:
        json.dump(data, file, indent=4)
