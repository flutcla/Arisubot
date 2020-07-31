"""
橘ありすの端末
ID: 373751424171114498
"""

import discord

from guilds import myGuild


async def on_member_join_(client: discord.Client, member: discord.Member):
    channel_id = 150731150731
    channel = client.get_channel(channel_id)
    await channel.send(f"{member.mention}さん、私の端末へようこそ。\n"
                       "あなたの来訪を心より歓迎します。\n"
                       "私は当ワールドのマスター、アリスです。\n"
                       "どうぞよろしくお願いいたします。\n"
                       "さて、今回あなたに課されたミッションはただひとつ。\n"
                       "このチャンネルで「規約読んだよありすちゃん」とつぶやくことです。")

# async def on_message_(client: discord.Client, message: discord.Message):
#     await
