import discord as discord
from discord.ext import commands
from datetime import datetime
import db_sqlite as to
import json

description = '''A bot that helps you with CTFs'''
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

admin_users = [173731309120651264, 615766504318959616, 561148984488361984]

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#Fonction qui log les print dans un fichier
def log(text):
    with open("/root/oka/ctf_log.txt", "a", encoding="UTF-8") as f:
        f.write("[" + str(datetime.now()) + "] > " + text + "\n")

def a_log(text):
    with open("/root/oka/admin_ctf_log.txt", "a", encoding="UTF-8") as f:
        f.write("[" + str(datetime.now()) + "] > " + text + "\n")

#Create a ctf
@bot.command(name="createctf", description="Create a CTF")
async def create(ctx, name):
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return
    to.add_ctf(name)
    to.create_tchallenge(name + ".db")
    to.create_tuser(name + ".db")
    to.create_thistory(name + ".db")
    await ctx.send("CTF created")

    a_log("CTF created by " + str(ctx.author) + " : " + name)

#Set active ctf
@bot.command(name="setactive", description="Set active CTF")
async def setactive(ctx, name):
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return
    try:
        to.set_active_ctf(name)
    except:
        await ctx.send("Vous vous êtes trompé dans la commande ou le nom du CTF n'est pas valide.")
        return
    await ctx.send("CTF set active")

    a_log("CTF set active by " + str(ctx.author) + " : " + name)

#Add challenge to active ctf
@bot.command(name="addchallenge", description="Add a challenge to the database")
async def add_challenge(ctx, nameid: str, points: int, flag: str):
    if ctx.author.bot:
        return

    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    try:
        to.add_challenge(ctf + ".db", nameid, points, flag)
    except:
        await ctx.send("Vous vous êtes trompé dans la commande ou le CTF n'est pas actif")
        return

    await ctx.send("Challenge ajouté !")

    a_log("Challenge added by " + str(ctx.author) + " : " + nameid + " " + str(points) + " " + flag)

#Show all challenges
@bot.command(name="showchallenges", description="Show all challenges")
async def show_challenges(ctx):
    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return
    challenges = to.get_all_challenges(ctf + ".db")
    msg = ""
    for challenge in challenges:
        msg += "NameID: " + challenge[1] + " | Points: " + str(challenge[3]) + " | Flag: " + str(challenge[5]) + " | History ASS: " + str(challenge[6]) + " |-| "
    await ctx.send(msg)

    a_log("Challenges shown by " + str(ctx.author))

#Show all history
@bot.command(name="showhistory", description="Show all history")
async def show_history(ctx):
    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return
    history = to.get_all_history(ctf + ".db")
    msg = ""
    for h in history:
        msg += "ID : " + str(h[0]) + " / Content : " + h[1] + " |-| "
    
    await ctx.send(msg)

    a_log("History shown by " + str(ctx.author))

#Add name to challenge
@bot.command(name="addname", description="Add a name to a challenge")
async def add_name(ctx, nameid: str, *, arg):
    if ctx.author.bot:
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    try:
        to.update_name(ctf + ".db", nameid, arg)
    except:
        await ctx.send("Le nom du challenge est incorrect ou le CTF n'est pas actif")
        return    

    await ctx.send("Nom ajouté !")

    a_log("Name added by " + str(ctx.author) + " : " + nameid + " " + arg)

#Add description to challenge
@bot.command(name="adddescription", description="Add a description to a challenge")
async def add_description(ctx, nameid: str, *, arg):
    if ctx.author.bot:
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    try:
        to.update_description(ctf + ".db", nameid, arg)
    except:
        await ctx.send("Le nom du challenge est incorrect ou le CTF n'est pas actif")
        return

    await ctx.send("Description ajoutée !")

    a_log("Description added by " + str(ctx.author) + " : " + nameid + " " + arg)

#Add points to challenge
@bot.command(name="addpoints", description="Add points to a challenge")
async def add_points(ctx, nameid: str, points: int):
    if ctx.author.bot:
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    try:
        to.update_points(ctf + ".db", nameid, points)
    except:
        await ctx.send("Le nom du challenge est incorrect ou le CTF n'est pas actif")
        return

    await ctx.send("Points ajoutés !")

    a_log("Points added by " + str(ctx.author) + " : " + nameid + " " + str(points))

#Add flag to challenge
@bot.command(name="addflag", description="Add a flag to a challenge")
async def add_flag(ctx, nameid: str, flag: str):
    if ctx.author.bot:
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    try:
        to.update_flag(ctf + ".db", nameid, flag)
    except:
        await ctx.send("Le nom du challenge est incorrect ou le CTF n'est pas actif")
        return

    await ctx.send("Flag ajouté !")

    a_log("Flag added by " + str(ctx.author) + " : " + nameid + " " + flag)

#Add history to challenge
@bot.command(name="addhistory", description="Add a history to a challenge")
async def add_history(ctx, nameid: str, dh: str):
    if ctx.author.bot:
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    try:
        to.update_history(ctf + ".db", nameid, dh)
    except:
        await ctx.send("Le nom du challenge est incorrect ou le CTF n'est pas actif")
        return

    await ctx.send("Histoire lié au challenge !")

    a_log("History linked by " + str(ctx.author) + " : " + nameid + " " + dh)

#Add history to history
@bot.command(name="addhth", description="Add a history to a history")
async def add_history_to_history(ctx, *, arg):
    if ctx.author.bot:
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    try:
        to.add_history(ctf + ".db", arg)
    except:
        await ctx.send("Attention ! Vous avez peut-être oublié de mettre le CTF en actif !")
        return

    await ctx.send("Histoire ajouté !")

    a_log("History added by " + str(ctx.author) + " : " + arg)

#Start CTF and send message to all users
@bot.command(name="startctf", description="Start CTF")
async def startctf(ctx):
    if ctx.author.bot:
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    for i in to.get_all_players(ctf + ".db"):
        user = bot.get_user(int(i[0]))
        embed = discord.Embed(title="Le CTF a commencé !", description="Le Début", color=0x0000ff)
        embed.add_field(name="Histoire", value=to.get_history(ctf + ".db", "1")[0], inline=False)
        await user.send(embed=embed)

    await ctx.send("CTF started !")

    a_log("CTF started by " + str(ctx.author))

    

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

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    try:
        to.add_user(ctf + ".db", autid)
    except:
        await ctx.send("Tu es déjà inscrit au CTF ou il y a un soucis !")
        return

    embed = discord.Embed(title="CTF - OKA", description="Bienvenue !", color=0x00ff00)
    embed.add_field(name="Bienvenue dans ce CTF !", value="Vous avez rejoint avec votre compte Discord : " + str(ctx.author), inline=False)
    await ctx.send(embed=embed)

    a_log("User " + str(ctx.author) + " joined the CTF.")

#Check flag
@bot.command(name="submit", description="Check a flag")
async def check_flag(ctx, flag: str):
    if ctx.author.bot:
        return

    log("Tentative de Flag de " + str(ctx.author) + " : " + flag)

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
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

    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
    embed = discord.Embed(title="Classement", description="Classement du CTF", color=0xe05000)
    for i in to.get_classement(ctf + ".db"):
        pt = pt + 1
        embed.add_field(name=str(pt) + " - " + str(bot.get_user(int(i[0]))), value="Points : " + str(i[1]), inline=False)
    await ctx.send(embed=embed)

    a_log("Classement shown by " + str(ctx.author))

@bot.command(name="credits", description="Show the credits")
async def show_credits(ctx):
    if ctx.author.bot:
        return

    embed = discord.Embed(title="Crédits", description="Crédits de OKA - CTF", color=0xe05000)
    embed.add_field(name="Créateurs du CTF", value="Saber | XBORZ#2588 -- Thomas | ThomasM#4405", inline=False)
    embed.add_field(name="Créateur de OKA - Bot Discord", value="Rhenar | Hope#5432", inline=False)
    await ctx.send(embed=embed)

    a_log("Credits shown by " + str(ctx.author))

@bot.command(name="endctf", description="End CTF")
async def endctf(ctx):
    try:
        ctf = to.get_active_ctf()[0]
    except:
        await ctx.send("Aucun CTF n'est actif.")
        return
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

    a_log("CTF ended by " + str(ctx.author))

@bot.command("initall", description="Init all")
async def initall(ctx):
    if ctx.author.bot:
        return
    if ctx.author.id not in admin_users:
        await ctx.send("Insufficient permissions")
        a_log("Insufficient permissions for " + str(ctx.author))
        return
    #to.drop_ctf()
    to.create_ctf()
    await ctx.send("Init all done")

    a_log("Init all done by " + str(ctx.author))

with open('/root/oka/config.json', encoding="UTF-8") as config_file:
    config = json.load(config_file)

bot.run(config[0]['token'])