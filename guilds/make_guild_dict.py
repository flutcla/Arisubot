from collections import defaultdict
from guilds.MyGuild import default
from guilds.Techmas import techmas


def make_guild_dict(client):
    guild_list = list()
    guild_dict = defaultdict(lambda: default(client))

    guild_list.append(techmas(client))

    for guild in guild_list:
        guild_dict[guild.id_] = guild

    return guild_dict
