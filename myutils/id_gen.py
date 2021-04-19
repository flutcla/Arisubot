from pathlib import Path
from myutils.get_data_from_json import *

PATH = Path.cwd()/'myutils'/'id_now.json'


def id_gen():
    data = get_data_from_json(PATH)
    id_now = data['ID']
    data['ID'] += 7
    write_data_to_json(PATH, data)

    return id_now
