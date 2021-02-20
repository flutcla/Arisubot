"""
橘ありすの端末
ID: 373751424171114498
"""

import discord
from guilds import MyGuild

ID_TANMATSU = 373751424171114498


class Tanmatsu(MyGuild):
    # 橘ありすの端末での定数（ID）
    ID_USER_ROLE = 513596307236192277
    ID_REVOCATION_ROLE = 742256629470330992
    ID_GLC_ROLE = 736905506815344691
    ID_ENTRANCE_CHANNEL = 741932065339211816
    ID_RULE_CHANNEL = 447382367217254420
    ID_INTRO_CHANNEL = 398954346852646915
    ID_GLC_RULE_CHANNEL = 736919335964114964

    async def on_member_join_(self, client: discord.Client, member: discord.Member):
        channel = client.get_channel(self.ID_ENTRANCE_CHANNEL)
        await channel.send(member.mention
                           + "橘ありすDiscordサーバー[橘ありすの端末へようこそお越しくださいました。\n"
                           + "当サーバーのご利用にあたって、まずは <#{}> チャンネルの規約をご覧ください。\n".format(self.ID_RULE_CHANNEL)
                           + "その後、<#{}> チャンネルに自己紹介の記入をよろしくお願いいたします。\n".format(self.ID_INTRO_CHANNEL)
                           + "（スパム等の荒らし対策のため、自己紹介で確認が取れた方のみURLを含む発言などが可能となります。）")

    async def on_message_(self, client: discord.Client, message: discord.Message):
        channel = client.get_channel(self.ID_INTRO_CHANNEL)
        if message.author.bot:
            return

        if message.channel.id == self.ID_INTRO_CHANNEL:
            if "名前" in message.content and "担当" in message.content:
                channel = client.get_channel(self.ID_ENTRANCE_CHANNEL)
                await channel.send(message.author.mention
                                   + "さんのユーザー申請を承認、あなたに一般ユーザーの権限を付与しました。\n"
                                   + "あらためまして、ようこそ[橘ありすの端末]へ。\n"
                                   + "あなたの来訪を、心より歓迎します。")
                role = channel.guild.get_role(self.ID_USER_ROLE)
                await message.author.add_roles(role)

    async def on_raw_reaction_add_(self, client: discord.client, payload: discord.RawReactionActionEvent):
        channel = client.get_channel(payload.channel_id)
        if channel.id == self.ID_GLC_RULE_CHANNEL:
            guild = client.get_guild(payload.guild_id)
            member = channel.guild.get_member(payload.user_id)
            for r in member.roles:
                if r.id == self.ID_REVOCATION_ROLE:
                    print("invalid apply")
                    return
            role = channel.guild.get_role(self.ID_GLC_ROLE)
            await member.add_roles(role)


def tanmatsu(client):
    return Tanmatsu(ID_TANMATSU, client)
