import discord
from imcgapi.get_runner import get_runner


class MyGuild:
    def __init__(self, id_: int, client: discord.Client) -> None:
        self.id_ = id_
        self.client = client

    async def on_message_(self, message: discord.Message):
        message_s = message.content.split()
        if len(message_s) == 0:
            return
        elif message_s[0] == "/arisu":
            await message.channel.send("私の使用方法については、こちら( https://hackmd.io/AZJWZiG-QxaQVn7x1eTxDA?view )をご覧ください。")
        elif message_s[0] == "/neko":
            await message.channel.send("正常に稼働してます、に、にゃ......")
        elif message_s[0] == "/runner":
            reply = get_runner(message.content, str(message.guild.id), message.guild.name)
            await message.channel.send(reply)

    async def on_member_join_(self, member: discord.Member):
        pass

    async def on_raw_reaction_add_(self, client: discord.client, payload: discord.RawReactionActionEvent):
        pass

    async def on_raw_reaction_remove_(self, client: discord.client, payload: discord.RawReactionActionEvent):
        pass


def default(client):
    return MyGuild(0, client)
