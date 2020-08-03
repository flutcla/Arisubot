from random import choices
import discord

fortune = {"大吉": 30, "中吉": 20, "吉": 20, "凶": 20, "大凶": 7,
           "特殊吉": 3}

special = {"スタ吉": 10, "エナ吉": 10, "鍵クロ吉": 1, "ガシャ吉": 10}

comment = {"大吉": }

def omikuji(message: discord.message):

