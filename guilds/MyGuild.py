from pathlib import Path
import discord
from imcgapi.get_runner import get_runner
from functions import among_us
from myutils.get_data_from_json import get_data_from_json


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

        # Among Us 関連機能
        elif message_s[0] == "/au":
            await among_us.main(self.client, message)

    async def on_member_join_(self, member: discord.Member):
        pass

    async def on_raw_reaction_add_(self, client: discord.client, payload: discord.RawReactionActionEvent):
        data = get_data_from_json(Path.cwd()/"guilds"/"guild_db.json")
        for guild_data in data.values():
            guild = client.get_guild(payload.guild_id)

            # Among Us!用
            if "au" in guild_data.keys():
                role_id = guild_data["au"]["role_id"]
                role = guild.get_role(role_id)
                # アナウンスメッセージ
                announce_message_id = guild_data["au"]["announce_message_id"]
                if payload.message_id == announce_message_id and payload.emoji.name == "👍":
                    await payload.member.add_roles(role)
                # ミュートボタン
                mute_button_message_id = guild_data["au"]["mute_button_message_id"]
                if payload.message_id == mute_button_message_id and payload.emoji.name == ":mute:":
                    await among_us.mute(role)

    async def on_raw_reaction_remove_(self, client: discord.client, payload: discord.RawReactionActionEvent):
        data = get_data_from_json(Path.cwd() / "guilds" / "guild_db.json")
        for guild_data in data.values():
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            # Among Us!用
            if "au" in guild_data.keys():
                role_id = guild_data["au"]["role_id"]
                role = guild.get_role(role_id)
                # アナウンスメッセージ
                announce_message_id = guild_data["au"]["announce_message_id"]
                if payload.message_id == announce_message_id and payload.emoji.name == "👍":
                    await member.remove_roles(role)
                # ミュートボタン
                mute_button_message_id = guild_data["au"]["mute_button_message_id"]
                if payload.message_id == mute_button_message_id and payload.emoji.name == ":mute:":
                    await among_us.mute(role, unmute=True)


def default(client):
    return MyGuild(0, client)
