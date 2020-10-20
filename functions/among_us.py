from pathlib import Path
import discord
from asyncio import TimeoutError
from guilds.db_funcs import get_guild_data, write_guild_data


async def main(client: discord.client, message: discord.message):
    message_s = message.content.split()
    key = message_s[1]
    guild = message.guild
    data = get_guild_data(guild.id, guild.name)
    if "au" not in data.keys():
        data["au"] = dict()
    if key == "register":  # サーバーを登録
        await register(client, message)
    elif "registered" not in data["au"].keys() or not data["au"]["registered"]:
        await message.channel.send("Among Us!関連機能を利用するためには、まず最初に'/au register'コマンドで登録してください。")

    if message.channel.id != int(data["au"]["command_channel_id"]):
        return

    if key == "announce":
        await announce(client, message)
    elif key == "button":
        await generate_mute_button(client, message)
    elif key == "mute":
        await command_mute(message)
    elif key == "unmute":
        await command_mute(message, unmute=True)
    elif key == "map":
        await send_map(message)



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
        "作成できたら、1分以内にロールのIDを教えて下さい。")
    while True:
        try:
            reply = await client.wait_for("message", timeout=60)
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
        "また、部屋名の通知もそのチャンネルで行うことができます。\n"
        "こちらも1分以内でお願いします。")
    while True:
        try:
            reply = await client.wait_for("message", timeout=60)
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
        "最後に、一括ミュート等のコマンドを使うテキストチャンネルのIDを教えてください。\n"
        "わざわざ言わずともわかるかもしれませんが、1分以内にお願いします。")
    while True:
        try:
            reply = await client.wait_for("message", timeout=60)
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

    data["au"]["registered"] = True
    write_guild_data(data)
    await message.channel.send("ありがとうございます、正常に登録されました。")
    await announce(client, message)


async def announce(client: discord.client, message: discord.message):
    guild = message.guild
    data = get_guild_data(guild.id, guild.name)
    announce_channel = guild.get_channel(data["au"]["announce_channel_id"])
    announce_message = await announce_channel.send(
        "--------------------------------------------------\n"
        "これは、Among Us!専用ロール付与用のメッセージです。\n"
        "このメッセージに'👍'でリアクションすると、参加者専用ロールが付与されます。\n"
        "このロールが付与されている場合、一斉ミュート等の対象になります。\n"
        "また、リアクションを外すとロールが外されます。")
    await announce_message.add_reaction("👍")
    announce_message_id = announce_message.id
    data["au"]["announce_message_id"] = announce_message_id
    write_guild_data(data)


async def generate_mute_button(client: discord.client, message: discord.message):
    guild = message.guild
    data = get_guild_data(guild.id, guild.name)
    announce_channel = guild.get_channel(data["au"]["announce_channel_id"])
    mute_button_message = await announce_channel.send(
        "--------------------------------------------------\n"
        "これは、Among Us!参加者一括ミュート機能用のメッセージです。\n"
        "このメッセージに'🔇'でリアクションすると、専用ロール所持者が一括ミュートされます。\n"
        "また、リアクションを外すとミュートが外れます。")
    await mute_button_message.add_reaction("🔇")
    mute_button_message_id = mute_button_message.id
    data["au"]["mute_button_message_id"] = mute_button_message_id
    write_guild_data(data)


async def command_mute(message: discord.message, unmute: bool = False):
    data = get_guild_data(message.guild.id, message.guild.name)
    role = message.guild.get_role(int(data["au"]["role_id"]))
    if role is None:
        await message.channel.send()
    await mute(role, unmute)


async def mute(role: discord.role, unmute: bool = False):
    members = role.members
    for member in members:
        if member.voice is None or member.voice.channel is None:
            continue
        else:
            if unmute:
                await member.edit(mute=False)
            else:
                await member.edit(mute=True)


async def send_map(message: discord.message):
    m = message.split()
    file_path = [Path.cwd()/"functions"/"data"/"Skeld_guid.jpg",
                 Path.cwd()/"functions"/"data"/"Mira_guid.jpg",
                 Path.cwd()/"functions"/"data"/"Polus_guid.jpg"]

    if len(m) == 2:
        await message.channel.send(file=discord.File(file_path[0]))
        await message.channel.send(file=discord.File(file_path[1]))
        await message.channel.send(file=discord.File(file_path[2]))
    elif m[2] in ["0", "1", "2"]:
        await message.channel.send(file=discord.File(file_path[int(m[2])]))
