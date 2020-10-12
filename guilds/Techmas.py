import discord
from guilds.MyGuild import MyGuild

ID_TECHMAS = 499428622331805697


class Techmas(MyGuild):
    def __init__(self, id_: int, client: discord.Client) -> None:
        super().__init__(id_, client)

    async def on_message_(self, message: discord.Message):
        await super().on_message_(message)


def techmas(client):
    return Techmas(ID_TECHMAS, client)
