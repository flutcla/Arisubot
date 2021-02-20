from collections import defaultdict
from guilds.MyGuild import default
from guilds.Test import test
from guilds.Techmas import techmas
from guilds.LookForward import lookforward
from guilds.Tanmatsu import tanmatsu


def make_guild_dict(client):
    guild_list = list()
    guild_dict = defaultdict(lambda: default(client))

    guild_list.append(test(client))
    guild_list.append(techmas(client))
    guild_list.append(lookforward(client))
    guild_list.append(tanmatsu(client))

    for guild in guild_list:
        guild_dict[guild.id_] = guild

    return guild_dict
