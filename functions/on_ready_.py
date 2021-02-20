import discord


def main(client: discord.client):
    @client.event
    async def on_ready():
        print('Connected as {0}. Version: {1}'.format(client.user, discord.__version__))

