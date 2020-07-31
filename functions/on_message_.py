from collections import defaultdict
import discord


def main(client: discord.Client, guild_dict: defaultdict):
    @client.event
    async def on_message(message: discord.message):
        if message.author.bot:
            return
        await guild_dict[message.guild.id].on_message_(message)
