import discord as discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
import asyncio
import db_sqlite as to
import json

description = '''A bot that helps you with CTFs'''
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#Fonction qui log les print dans un fichier
def log(text):
    with open("ctf_log.txt", "a") as f:
        f.write("[" + str(datetime.now()) + "] > " + text + "\n")

#Create a ctf
@bot.command(name="createctf", description="Create a CTF")
async def create(ctx, name):
    to.add_ctf(name)
    to.create_tchallenge(name + ".db")
    to.create_tuser(name + ".db")
    to.create_thistory(name + ".db")
    await ctx.send("CTF created")

#Set active ctf
@bot.command(name="setactive", description="Set active CTF")
async def setactive(ctx, name):
    to.set_active_ctf(name)
    await ctx.send("CTF set active")

#Add challenge to active ctf
@bot.command(name="addchallenge", description="Add a challenge to the database")
async def add_challenge(ctx, nameid: str, points: int, flag: str):
    if ctx.author.bot:
        return
    #if ctx.author.id != 1234567890:
    #    await ctx.send("Tu ne peux pas ajouter de challenges.")
    #    return

    ctf = to.get_active_ctf()[0]
    to.add_challenge(ctf + ".db", nameid, points, flag)

    await ctx.send("Challenge ajouté !")

#Show all challenges
@bot.command(name="showchallenges", description="Show all challenges")
async def show_challenges(ctx):
    ctf = to.get_active_ctf()[0]
    challenges = to.get_all_challenges(ctf + ".db")
    msg = ""
    for challenge in challenges:
        msg += "NameID: " + challenge[1] + " | Name: " + challenge[2] + " | Points: " + str(challenge[3]) + " | Flag: " + str(challenge[5]) + " | History ASS: " + challenge[6] + " || "
    await ctx.send(msg)

#Show all history
@bot.command(name="showhistory", description="Show all history")
async def show_history(ctx):
    ctf = to.get_active_ctf()[0]
    history = to.get_all_history(ctf + ".db")
    msg = ""
    for h in history:
        msg += "ID : " + h[0] + "Content : " + h[1] + " || "
    
    await ctx.send(msg)

#Add name to challenge
@bot.command(name="addname", description="Add a name to a challenge")
async def add_name(ctx, nameid: str, *, arg):
    if ctx.author.bot:
        return
    #if ctx.author.id != 1234567890:
    #    await ctx.send("Tu ne peux pas ajouter de challenges.")
    #    return

    ctf = to.get_active_ctf()[0]
    to.update_name(ctf + ".db", nameid, arg)

    await ctx.send("Nom ajouté !")

#Add description to challenge
@bot.command(name="adddescription", description="Add a description to a challenge")
async def add_description(ctx, nameid: str, *, arg):
    if ctx.author.bot:
        return
    #if ctx.author.id != 1234567890:
    #    await ctx.send("Tu ne peux pas ajouter de challenges.")
    #    return

    ctf = to.get_active_ctf()[0]
    to.update_description(ctf + ".db", nameid, arg)

    await ctx.send("Description ajoutée !")

#Add points to challenge
@bot.command(name="addpoints", description="Add points to a challenge")
async def add_points(ctx, nameid: str, points: int):
    if ctx.author.bot:
        return
    #if ctx.author.id != 1234567890:
    #    await ctx.send("Tu ne peux pas ajouter de challenges.")
    #    return

    ctf = to.get_active_ctf()[0]
    to.update_points(ctf + ".db", nameid, points)

    await ctx.send("Points ajoutés !")

#Add flag to challenge
@bot.command(name="addflag", description="Add a flag to a challenge")
async def add_flag(ctx, nameid: str, flag: str):
    if ctx.author.bot:
        return
    #if ctx.author.id != 1234567890:
    #    await ctx.send("Tu ne peux pas ajouter de challenges.")
    #    return

    ctf = to.get_active_ctf()[0]
    to.update_flag(ctf + ".db", nameid, flag)

    await ctx.send("Flag ajouté !")

#Add history to challenge
@bot.command(name="addhistory", description="Add a history to a challenge")
async def add_history(ctx, nameid: str, dh: str):
    if ctx.author.bot:
        return
    #if ctx.author.id != 1234567890:
    #    await ctx.send("Tu ne peux pas ajouter de challenges.")
    #    return

    ctf = to.get_active_ctf()[0]
    to.update_history(ctf + ".db", nameid, dh)

    await ctx.send("Historique ajouté !")

#Add history to history
@bot.command(name="addhth", description="Add a history to a history")
async def add_history_to_history(ctx, *, arg):
    if ctx.author.bot:
        return
    #if ctx.author.id != 1234567890:
    #    await ctx.send("Tu ne peux pas ajouter de challenges.")
    #    return

    ctf = to.get_active_ctf()[0]
    to.add_history(ctf + ".db", arg)

    await ctx.send("Histoire ajouté !")

#Start CTF and send message to all users
@bot.command(name="startctf", description="Start CTF")
async def startctf(ctx):
    if ctx.author.bot:
        return
    #if ctx.author.id != 1234567890:
    #    await ctx.send("Tu ne peux pas ajouter de challenges.")
    #    return

    ctf = to.get_active_ctf()[0]
    for i in to.get_all_players(ctf + ".db"):
        user = bot.get_user(int(i[0]))
        embed = discord.Embed(title="Le CTF a commencé !", description="Le Début", color=0x0000ff)
        embed.add_field(name="Histoire", value=to.get_history(ctf + ".db", "1")[0], inline=False)
        await user.send(embed=embed)

    await ctx.send("CTF started !")

######################################
## Play commands #####################
######################################
#Join a ctf
@bot.command(name="join", description="Add a user to the database")
async def add_user(ctx):

    log("Le joueur " + str(ctx.author) + " vient de rejoindre le CTF.")

    if ctx.author.bot:
        return

    autid = ctx.author.id

    ctf = to.get_active_ctf()[0]
    to.add_user(ctf + ".db", autid)

    embed = discord.Embed(title="CTF - OKA", description="Bienvenue !", color=0x00ff00)
    embed.add_field(name="Bienvenue dans ce CTF !", value="Vous avez rejoint avec votre compte Discord : " + str(ctx.author), inline=False)
    await ctx.send(embed=embed)

#Check flag
@bot.command(name="submit", description="Check a flag")
async def check_flag(ctx, flag: str):
    if ctx.author.bot:
        return

    log("Tentative de Flag de " + str(ctx.author) + " : " + flag)

    ctf = to.get_active_ctf()[0]

    autid = ctx.author.id
    if to.check_player(ctf + ".db", autid) is False:
        embed = discord.Embed(title="CTF - OKA", description="ERREUR !", color=0xff0000)
        embed.add_field(name="Il y a eu un soucis...", value="Vous devez rejoindre le CTF en premier avec la commande '!join'", inline=False)
        await ctx.send(embed=embed)
        return

    aws = to.check_flag(ctf + ".db", flag)

    if aws is True:
        chal = to.get_challengesdone(ctf + ".db", autid)[0]
        try :
            chal = chal.split(",")
        except:
            print("No challenges done")
        for i in chal:
            if i == to.get_nameid(ctf + ".db", flag)[0]:
                embed = discord.Embed(title="CTF - OKA", description="Hey !", color=0xff0000)
                embed.add_field(name="Il y a eu un soucis...", value="Vous avez déjà rentré ce Flag !", inline=False)
                await ctx.send(embed=embed)
                return

        to.update_challengesdone(ctf + ".db", autid, to.get_challengesdone(ctf + ".db", autid)[0] + to.get_nameid(ctf + ".db", flag)[0] + ",")
        pts_old = to.get_score(ctf + ".db", autid)[0]
        pts_new = pts_old + to.get_points(ctf + ".db", flag)[0]
        to.update_score(ctf + ".db", autid, pts_new)


        embed = discord.Embed(title="Félicitations !", description="Votre Flag est correcte", color=0x00ff00)
        embed.add_field(name="Histoire", value=to.get_history(ctf + ".db", to.get_history_id(ctf + ".db", flag)[0])[0], inline=False)
        await ctx.send(embed=embed)

        log("Flag correct de " + str(ctx.author) + " : " + flag)
    else:
        embed = discord.Embed(title="CTF - OKA", description="Hey !", color=0xff0000)
        embed.add_field(name="Il y a eu un soucis...", value="Le Flag que vous venez d'entrer n'est pas correct !", inline=False)
        await ctx.send(embed=embed)

#Show classemment
pt = 0
@bot.command(name="classement", description="Show the classemment")
async def show_classement(ctx):
    pt = 0
    if ctx.author.bot:
        return

    ctf = to.get_active_ctf()[0]
    embed = discord.Embed(title="Classement", description="Classement du CTF", color=0xe05000)
    for i in to.get_classement(ctf + ".db"):
        pt = pt + 1
        embed.add_field(name=str(pt) + " - " + str(bot.get_user(int(i[0]))), value="Points : " + str(i[1]), inline=False)
    await ctx.send(embed=embed)

@bot.command(name="credits", description="Show the credits")
async def show_credits(ctx):
    if ctx.author.bot:
        return

    embed = discord.Embed(title="Crédits", description="Crédits de OKA - CTF", color=0xe05000)
    embed.add_field(name="Créateurs du CTF", value="Saber | XBORZ#2588 -- Thomas | ThomasM#4405", inline=False)
    embed.add_field(name="Créateur de OKA - Bot Discord", value="Rhenar | Hope#5432", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="endctf", description="End CTF")
async def endctf(ctx):
    ctf = to.get_active_ctf()[0]

    for i in to.get_all_players(ctf + ".db"):
        user = bot.get_user(int(i[0]))
        embed = discord.Embed(title="Le CTF est finis !", description="La FIN !", color=0x0000ff)
        embed.add_field(name="Merci a vous d'avoir participé !", value="Il est temps de voir le classement final.", inline=False)
        await user.send(embed=embed)

        pt = 0
        embed = discord.Embed(title="Classement", description="Classement du CTF", color=0x00ff00)
        for i in to.get_classement(ctf + ".db"):
            pt = pt + 1
            embed.add_field(name=str(pt) + " - " + str(bot.get_user(int(i[0]))), value="Points : " + str(i[1]), inline=False)
        await user.send(embed=embed)

        embed = discord.Embed(title="Crédits", description="Crédits de OKA - CTF", color=0xff0000)
        embed.add_field(name="Créateurs du CTF", value="Saber | XBORZ#2588 -- Thomas | ThomasM#4405", inline=False)
        embed.add_field(name="Créateur de OKA - Bot Discord", value="Rhenar | Hope#5432", inline=False)
        await user.send(embed=embed)

    await ctx.send("CTF ended !")

@bot.command("initall", description="Init all")
async def initall(ctx):
    if ctx.author.bot:
        return
    #if ctx.author.id != 1234567890:
    #    await ctx.send("Tu ne peux pas ajouter de challenges.")
    #    return
    #to.drop_ctf()
    to.create_ctf()
    await ctx.send("Init all done")

with open('config.json') as config_file:
    config = json.load(config_file)

bot.run(config[0]['token'])