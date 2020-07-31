from collections import defaultdict
import discord

from guilds import MyGuild


def main(client: discord.Client, guild_dict: defaultdict):
    @client.event
    async def on_member_join(member: discord.Member):
        for guild in guild_dict:
            guild.on_member_join_(member)

