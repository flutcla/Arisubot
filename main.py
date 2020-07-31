from pathlib import Path
import discord

import myutils

from functions import *
from guilds import make_guild_dict


token: str = myutils.get_data_from_json(Path.cwd()/"token.json")["token"]["test"]
client = discord.Client()

guild_dict = make_guild_dict(client)

on_ready_.main(client)
on_message_.main(client, guild_dict)
on_member_join_.main(client, guild_dict)

client.run(token)

