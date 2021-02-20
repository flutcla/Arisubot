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

    # 橘ありすの端末での定数（ID）
    ID_USER_ROLE = 812752880087990333
    # ID_REVOCATION_ROLE = 742256629470330992
    # ID_GLC_ROLE = 736905506815344691
    ID_ENTRANCE_CHANNEL = 527464796799631383
    ID_RULE_CHANNEL = 527464796799631383
    ID_INTRO_CHANNEL = 527464796799631383
    # ID_GLC_RULE_CHANNEL = 736919335964114964

    async def on_member_join_(self, member: discord.Member):
        await super().on_member_join_(member)
        channel = self.client.get_channel(self.ID_ENTRANCE_CHANNEL)
        await channel.send(member.mention
                           + "橘ありすDiscordサーバー[橘ありすの端末]へようこそお越しくださいました。\n"
                           + "当サーバーのご利用にあたって、まずは <#{}> チャンネルの規約をご覧ください。\n".format(self.ID_RULE_CHANNEL)
                           + "その後、<#{}> チャンネルに自己紹介の記入をよろしくお願いいたします。\n".format(self.ID_INTRO_CHANNEL)
                           + "（スパム等の荒らし対策のため、自己紹介で確認が取れた方のみURLを含む発言などが可能となります。）")


def test(client):
    return Test(ID_TEST, client)
