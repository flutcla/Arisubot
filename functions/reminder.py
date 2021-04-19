from pathlib import Path
from datetime import datetime, timedelta
import discord
from myutils import get_data_from_json, write_data_to_json, id_gen
from copy import deepcopy
from collections import OrderedDict


PATH = Path.cwd()/"functions"/"data"/"reminder_data.json"


async def help_reminder(message: discord.message):
    await message.reply(
        'リマインダー機能の使い方は以下の通りです。\n' +
        '追加: /reminder add %m月%d日%H時%M分 内容\n' +
        '一覧: /reminder list\n' +
        '削除: /reminder delete ID\n' +
        'IDはリマインダー一覧で確認ができます。'
    )


async def add_reminder(message: discord.message):
    m = message.content.split()
    try:
        date = m[2]
        word = ' '.join(m[3:])
    except IndexError:
        return await message.reply('メッセージのフォーマットが間違っています。「/reminder add %m月%d日%H時%M分 内容」のように書いてください。')
    try:
        remind_time = datetime.strptime(date, '%m月%d日%H時%M分')
        remind_time = remind_time.replace(year=datetime.now().year)
    except Exception:
        return await message.reply('日付のフォーマットが間違っています。「%m月%d日%H時%M分」のように書いてください。')

    if datetime.now() - remind_time > timedelta(seconds=0):
        remind_time += timedelta(days=365)

    remind_time_str = remind_time.strftime('%Y年%m月%d日%H時%M分')

    reminder_data = get_data_from_json(PATH)
    _ID = id_gen()
    reminder_data[_ID] = {'ID': _ID, 'remind_time': remind_time_str, 'word': word, 'channel_id': message.channel.id}
    write_data_to_json(PATH, reminder_data)
    await message.reply(f'{remind_time_str} にリマインダーを登録しました。')


async def check_reminder(client: discord.client):
    time_now = datetime.now()
    reminder_data = get_data_from_json(PATH)
    reminder_data_copy = deepcopy(reminder_data)
    for data in reminder_data_copy.values():
        if timedelta(minutes=0) < time_now - datetime.strptime(data['remind_time'], '%Y年%m月%d日%H時%M分') < timedelta(minutes=5):
            channel = client.get_channel(data['channel_id'])
            word = '[リマインダー]' + data['word']
            await channel.send(word)
            reminder_data.pop(str(data['ID']))
        elif time_now - datetime.strptime(data['remind_time'], '%Y年%m月%d日%H時%M分') >= timedelta(minutes=5):
            print(f'{data["remind_time"]}に設定されていたリマインダー「{data["word"]}」を時間経過により削除しました。')
            reminder_data.pop(str(data['ID']))

    write_data_to_json(PATH, reminder_data)


async def list_reminder(message: discord.message):
    def key(x):
        return datetime.strptime(x['remind_time'], '%Y年%m月%d日%H時%M分')

    reminder_data = get_data_from_json(PATH)
    sorted_reminder_data = sorted(reminder_data.values(), key=key)
    word = ""
    for data in sorted_reminder_data:
        if data["channel_id"] == message.channel.id:
            word += f'\nID:{data["ID"]} {data["remind_time"]} {data["word"]}'
    if word == "":
        word = '現在このチャンネルで設定されているリマインダーはありません。'
    else:
        word = '現在このチャンネルで設定されているリマインダー一覧です。' + word
    await message.reply(word)


async def delete_reminder(message: discord.message):
    m = message.content.split()
    try:
        _ID = m[2]
    except TypeError:
        return await message.reply('IDは数字で入力してください。')
    reminder_data = get_data_from_json(PATH)
    if _ID in reminder_data:
        data = reminder_data.pop(_ID)
        write_data_to_json(PATH, reminder_data)
        return await message.reply(f'{data["remind_time"]}に設定されていたリマインダー「{data["word"]}」を削除しました。')
    else:
        return await message.reply('指定したIDが見つかりませんでした。')


async def main(message: discord.message):
    message_s = message.content.split()
    if message_s[1] == 'help':
        await help_reminder(message)
    elif message_s[1] == 'add':
        await add_reminder(message)
    elif message_s[1] == 'list':
        await list_reminder(message)
    elif message_s[1] == 'delete':
        await delete_reminder(message)
