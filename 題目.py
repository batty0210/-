import discord
import random
import time
import json
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

Going = {}
Perfer = {}
with open('會計111.json', 'r') as f:
    data = json.load(f)
    B64 = data
with open('會計112.json', 'r') as f:
    data = json.load(f)
    B65 = data
with open('會計113.json', 'r') as f:
    data = json.load(f)
    B66 = data
B63 = {}
@bot.event
async def on_ready():
    synced = await bot.tree.sync()
@bot.event
async def on_message(ctx):
    user = ctx.author.id
    if user not in Going:
        return
    題目=eval(Going[user]["Q"])
    ran=Going[user]["Asking"] #題目的index編號
    idk = list(題目)[ran] #正在問的題目的名字
    ABCD=["A","B","C","D"]
    if (ctx.author.bot):
        return
    try:
        a = Perfer[str(user)]["選項打亂"]
    except:
        Perfer[str(user)] = {}
        Perfer[str(user)]["選項打亂"] = False
    try:
        Num = ABCD.index(ctx.content)
        if ctx.content.startswith("A") or ctx.content.startswith("B") or ctx.content.startswith("C") or ctx.content.startswith("D"):
            if Perfer[str(user)]["選項打亂"] == True:
                ans = ABCD[Going[user]["FML"].index(題目[idk][題目[idk]["Correct"]])]
                if Going[user]["FML"][Num] == 題目[idk][題目[idk]["Correct"]]:
                    await ctx.channel.send("好棒 你對了")
                    Going[user]["Number"] += 1
                    Going[user]["Asked"].append(ran)
                    Going[user]["Correct"] += 1
                else:
                    await ctx.channel.send(f"錯了 正確答案是{ans}")
                    Going[user]["Number"] += 1
                    Going[user]["Asked"].append(ran)
            elif Perfer[str(user)]["選項打亂"] == False:
                ans = ABCD[Going[user]["NFML"].index(題目[idk][題目[idk]["Correct"]])]
                if Going[user]["NFML"][Num] == 題目[idk][題目[idk]["Correct"]]:
                    await ctx.channel.send("好棒 你對了")
                    Going[user]["Number"] += 1
                    Going[user]["Asked"].append(ran)
                    Going[user]["Correct"] += 1
                else:
                    await ctx.channel.send(f"錯了 正確答案是{ans}")
                    Going[user]["Number"] += 1
                    Going[user]["Asked"].append(ran)
            if len(Going[user]["Asked"]) >= len(題目):
                Correct = Going[user]["Correct"]
                Correct = 100 / len(題目) * Correct
                
                await ctx.channel.send(f"結束 總分為 {int(Correct)} 分")
                del Going[user]
                return
            await ask(ctx)
    except:
        if ctx.content.startswith("X") or ctx.content.startswith("O"):
            ans = 題目[list(題目)[ran]]["Correct"]
            ig = ["X", "O"]
            if 題目[list(題目)[ran]]["Correct"] not in ig:
                return
            if 題目[list(題目)[ran]]["Correct"] == ctx.content:
                await ctx.channel.send("好棒 你對了")
                Going[user]["Number"] += 1
                Going[user]["Asked"].append(ran)
                Going[user]["Correct"] += 1
            else:
                await ctx.channel.send(f"錯了 正確答案是{ans}")
                Going[user]["Number"] += 1
                Going[user]["Asked"].append(ran)
            if len(Going[user]["Asked"]) >= len(題目):
                Correct = Going[user]["Correct"]
                Correct = 100 / len(題目) * Correct
                
                await ctx.channel.send(f"結束 總分為 {int(Correct)} 分")
                del Going[user]
                return
            await ask(ctx)

@bot.tree.command(name="停止刷題") 
async def stop(interaction:discord.Interaction):
    user = interaction.user.id
    if user not in Going:
        await interaction.response.send_message("你尚未開始刷題！", ephemeral=False)
    else:
        del Going[user]
        await interaction.response.send_message("已結束此次刷題", ephemeral=False)
@bot.tree.command(name="刷題") 
async def start(ctx,題目:str):
    user = ctx.user.id
    if user in Going:
        await ctx.channel.send("你已經在刷題了！")
        return
    Going[user] = {}
    Going[user]["Q"] = 題目
    if 題目 == "B63":
        test = {}
        yesorno = 0
        choose = 0
        for i in range(20):
            ran = random.randint(0,len(yesorno)-1)
            while list(yesorno)[ran] in list(test):
                ran = random.randint(0,len(yesorno)-1)
            現在是哪一題 = list(yesorno)[ran]
            test[現在是哪一題] = {"Correct": yesorno[現在是哪一題]["Correct"]}
        for i in range(40):
            ran = random.randint(0,len(choose)-1)
            while list(choose)[ran] in list(test):
                ran = random.randint(0,len(choose)-1)
            現在是哪一題 = list(choose)[ran]
            test[現在是哪一題] = {"A": choose[現在是哪一題]["A"], "B": choose[現在是哪一題]["B"], "C": choose[現在是哪一題]["C"], "D": choose[現在是哪一題]["D"], "Correct": choose[現在是哪一題]["Correct"]}
        global B63
        B63 = test
    Going[user]["Asked"] = []
    Going[user]["Asking"] = ""
    Going[user]["Number"] = 1
    Going[user]["Correct"] = 0
    await ask(ctx)
@start.autocomplete("題目")
async def startchoice(ctx,choice:str):
    d = [] 
    for c in ["會計111","會計112","會計113"]:
        if choice.lower() in c.lower():
            b=c
            match c:
                case "會計111":
                    b = "B64"
                case "會計112":
                    b = "B65"
                case "會計113":
                    b = "B66"
            d.append(app_commands.Choice(name=c, value=b))
    return d

@bot.tree.command(name="選項打亂") 
async def randomrize(ctx,開關:str):
    user = ctx.user.id
    try:
        a = Perfer[str(user)]["選項打亂"]
    except:
        Perfer[str(user)] = {}
        Perfer[str(user)]["選項打亂"] = False
        print("動了")
    if (開關 == "開"):
        Perfer[str(user)]["選項打亂"] = True
    elif (開關 == "關"):
        Perfer[str(user)]["選項打亂"] = False
    await ctx.response.send_message(f"成功將選項打亂設定為: {開關}", ephemeral=False)
    with open("perfer.json", "w") as outfile:
        json.dump(Perfer, outfile)
@randomrize.autocomplete("開關")
async def randomchoice(ctx,choice:str):
    d = [] 
    for c in ["開","關"]:
        if choice.lower() in c.lower():
            d.append(app_commands.Choice(name=c, value=c))
    return d

async def ask(ctx):
    try:
        user = ctx.author.id
    except:
        user = ctx.user.id
    題目=eval(Going[user]["Q"])
    ran = random.randint(0,len(題目)-1)
    while ran in Going[user]["Asked"]:
        ran = random.randint(0,len(題目)-1)
    Going[user]["Asking"] = ran
    idk = list(題目)[ran]
    SuperLongShit = str(Going[user]["Number"]) + ". " + str(list(題目)[int(Going[user]["Asking"])])
    try:
        a = Perfer[str(user)]["選項打亂"]
    except:
        Perfer[str(user)] = {}
        Perfer[str(user)]["選項打亂"] = False
    try:
        messup = [題目[idk]["A"], 題目[idk]["B"], 題目[idk]["C"], 題目[idk]["D"]]
        notmessup = [題目[idk]["A"], 題目[idk]["B"], 題目[idk]["C"], 題目[idk]["D"]]
        random.shuffle(messup)
        Going[user]["FML"] = messup
        Going[user]["NFML"] = notmessup
        if (Perfer[str(user)]["選項打亂"] == True):
            SuperLongShit += "\n(A)" + messup[0]
            SuperLongShit += "\n(B)" + messup[1]
            SuperLongShit += "\n(C)" + messup[2]
            SuperLongShit += "\n(D)" + messup[3]
        else:
            SuperLongShit += "\n(A)" + notmessup[0]
            SuperLongShit += "\n(B)" + notmessup[1]
            SuperLongShit += "\n(C)" + notmessup[2]
            SuperLongShit += "\n(D)" + notmessup[3]  
    except KeyError:
        pass
    try:
        await ctx.response.send_message(SuperLongShit, ephemeral=False)
    except:
        await ctx.channel.send(SuperLongShit)
bot.run('token here')