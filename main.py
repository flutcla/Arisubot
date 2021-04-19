from pathlib import Path
import discord
from discord.ext import tasks

import myutils

from functions import *
from guilds import make_guild_dict


token: str = myutils.get_data_from_json(Path.cwd()/"token.json")["token"]["test"]
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

guild_dict = make_guild_dict(client)

on_ready_.main(client)
on_message_.main(client, guild_dict)
on_member_join_.main(client, guild_dict)
on_raw_reaction_add_.main(client, guild_dict)


@tasks.loop(seconds=60)
async def loop():
    await client.wait_until_ready()
    await loop_task.main(client)

loop.start()

client.run(token)

