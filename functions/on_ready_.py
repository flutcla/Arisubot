import discord


def main(client: discord.client):
    @client.event
    async def on_ready():
        print('Connected as {0}'.format(client.user))

