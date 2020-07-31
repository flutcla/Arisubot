from collections import defaultdict
import discord


def main(client: discord.Client, guild_dict: defaultdict):
    @client.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        await guild_dict[payload.guild_id].on_raw_reaction_add_(client, payload)

    @client.event
    async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
        await guild_dict[payload.guild_id].on_raw_reaction_remove_(client, payload)
