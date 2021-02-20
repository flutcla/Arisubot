import discord
from guilds.MyGuild import MyGuild

ID_TEST = 527464796799631375


class Test(MyGuild):

    async def on_raw_reaction_add_(self, client: discord.client, payload: discord.RawReactionActionEvent):
        await super().on_raw_reaction_add_(client, payload)
        if payload.message_id == 738789309548593195 and payload.emoji.name == "👍":
            guild = client.get_guild(payload.guild_id)
            role = guild.get_role(738788021628960812)
            await payload.member.add_roles(role)

    async def on_raw_reaction_remove_(self, client: discord.client, payload: discord.RawReactionActionEvent):
        await super().on_raw_reaction_remove_(client, payload)
        if payload.message_id == 738789309548593195 and payload.emoji.name == "👍":
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(738788021628960812)
            await member.remove_roles(role)


def test(client):
    return Test(ID_TEST, client)
