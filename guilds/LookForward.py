import discord
from guilds.MyGuild import MyGuild

ID_LOOKFORWARD = 737266798314913803


class Lookforward(MyGuild):

    async def on_raw_reaction_add_(self, client: discord.client, payload: discord.RawReactionActionEvent):
        await super().on_raw_reaction_add_(client, payload)
        if payload.message_id == 738781425716690964 and payload.emoji.name == "👍":
            guild = client.get_guild(payload.guild_id)
            role = guild.get_role(738780960815841371)
            await payload.member.add_roles(role)

    async def on_raw_reaction_remove_(self, client: discord.client, payload: discord.RawReactionActionEvent):
        await super().on_raw_reaction_remove_(client, payload)
        if payload.message_id == 738781425716690964 and payload.emoji.name == "👍":
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(738780960815841371)
            await member.remove_roles(role)


def lookforward(client):
    return Lookforward(ID_LOOKFORWARD, client)
