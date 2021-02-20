from collections import defaultdict
import discord


def main(client: discord.Client, guild_dict: defaultdict):
    @client.event
    async def on_member_join(member: discord.Member):
        await guild_dict[member.guild.id].on_member_join_(client, member)

