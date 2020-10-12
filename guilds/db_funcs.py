from pathlib import Path
from myutils import get_data_from_json, write_data_to_json


def get_guild_data(guild_id: int, guild_name: str):
    guild_id = str(guild_id)
    path = Path.cwd()/"guilds"/"guild_db.json"
    data = get_data_from_json(path)
    if guild_id in data.keys():
        return data[guild_id]
    else:
        data[guild_id] = {"id": guild_id, "name": guild_name}
        write_data_to_json(path, data)
        return data[guild_id]


def write_guild_data(guild_data: dict):
    path = Path.cwd()/"guilds"/"guild_db.json"
    data = get_data_from_json(path)
    data[guild_data["id"]] = guild_data
    write_data_to_json(path, data)
