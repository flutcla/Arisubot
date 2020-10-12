from pathlib import Path
import discord
from asyncio import TimeoutError
from guilds.db_funcs import get_guild_data, write_guild_data


async def main(client: discord.client, message: discord.message):
    message_s = message.content.split()
    key = message_s[1]
    if key == "register":  # サーバーを登録
        await register(client, message)
    elif key == "mute":
        await mute(client, message)


async def register(client: discord.client, message: discord.message):
    role_id: int = 0
    announce_channel_id: int = 0
    command_channel_id: int = 0

    guild = message.guild
    data = get_guild_data(guild.id, guild.name)
    if "au" not in data.keys():
        data["au"] = dict()

    await message.channel.send(
        "Among Us!関連機能のセットアップを開始します。\n"
        "まず初めに、専用のロールを作成してください。\n"
        "作成できたら、30秒以内にロールのIDを教えて下さい。")
    while True:
        try:
            reply = await client.wait_for("message", timeout="30")
            role_id = int(reply.content)
            role = guild.get_role(role_id)
            if role is None:
                await message.channel.send("ロールIDが間違っているかもしれません、確認してもう一度入力してください。")
                continue
            break
        except TimeoutError:
            await message.channel.send("お忙しいようですので、中断しました。")
            return
        except TypeError:
            await message.channel.send("ロールIDは数値で入力してください。")
            continue
    data["au"]["role_id"] = role_id

    await message.channel.send(
        "続いて、Among Us!の紹介と権限付与用のメッセージを送るテキストチャンネルのIDを教えてください。\n"
        "また、部屋名の通知もそのチャンネルで行うことができます。")
    while True:
        try:
            reply = await client.wait_for("message", timeout="30")
            announce_channel_id = int(reply.content)
            announce_channel = guild.get_channel(announce_channel_id)
            if announce_channel is None:
                await message.channel.send("チャンネルIDが間違っているかもしれません、確認してもう一度入力してください。")
                continue
            break
        except TimeoutError:
            await message.channel.send("お忙しいようですので、中断しました。")
            return
        except TypeError:
            await message.channel.send("チャンネルIDは数値で入力してください。")
            continue
    data["au"]["announce_channel_id"] = announce_channel_id

    await message.channel.send(
        "最後に、一括ミュート等のコマンドを使うテキストチャンネルのIDを教えてください。")
    while True:
        try:
            reply = await client.wait_for("message", timeout="30")
            command_channel_id = int(reply.content)
            command_channel = guild.get_channel(command_channel_id)
            if command_channel is None:
                await message.channel.send("チャンネルIDが間違っているかもしれません、確認してもう一度入力してください。")
                continue
            break
        except TimeoutError:
            await message.channel.send("お忙しいようですので、中断しました。")
            return
        except TypeError:
            await message.channel.send("チャンネルIDは数値で入力してください。")
            continue
    data["au"]["command_channel_id"] = command_channel_id

    write_guild_data(data)
    await message.channel.send("ありがとうございます、正常に登録されました。")


async def mute(client: discord.client, message: discord.message):
    guild = message.guild
    data = get_guild_data(guild.id, guild.name)
    if message.channel.id != int(data["au"]["command_channel_id"]):
        return
    role = client.get_role(int(data["au"]["role_id"]))
    if role is None:
        await message.channel.send()
    members = role.members
    for member in members:
        if member.voice.channel is None:
            continue
        else:
            member.voice.self_mute = True
