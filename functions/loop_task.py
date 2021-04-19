import discord
from functions import reminder


async def main(client: discord.client):
    await reminder.check_reminder(client)
