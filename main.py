# made by .ftgs#0

version = "1.0.4"

import datetime
import time
import os
import re
import rapidjson as json
import uuid
import base64
import requests
import asyncio
import aiohttp
import httpx
import discord
import socketio
import sys
import string
import traceback
from discord.ext import commands
from discord import Embed, Colour, SyncWebhook, Game
from colorama import Fore, Back, Style
from functools import cache


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
            
    
LOGO = f"""

            {Fore.LIGHTWHITE_EX}{Style.NORMAL}Version: {Fore.LIGHTGREEN_EX}{Style.BRIGHT}{version}
 ______     __         ______     __  __     _____    
/\  ___\   /\ \       /\  __ \   /\ \/\ \   /\  __-.  
\ \ \____  \ \ \____  \ \ \/\ \  \ \ \_\ \  \ \ \/\ \ 
 \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \____- 
  \/_____/   \/_____/   \/_____/   \/_____/   \/____/                                                       
"""


# checking version
sio = socketio.AsyncClient(ssl_verify=False)
restart_time = None
print(f"Current version: {version}")
stats = False
response = requests.get("https://raw.githubusercontent.com/AlikSusFootages/cloud/main/version").text.rstrip()
if response == version:

    print(f"New version: {response}. Starting Cloud")
else:
    print(response.text.rstrip())
    print("Pls update your sniper")
    os.system("pause")
    exit(0)
    
def save_log(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{current_time}: {message}\n"

    with open("logs.txt", "w") as log_file:
        log_file.write(log_entry)
        
save_log("Started\n")
    
# discord 

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except:
    exit("Please check your config.json")

if config["Discord"]["Bot"]["Enabled"]:
    intents = discord.Intents.all()
    bot_token = config['Discord']['Bot']['Token']
    prefix = config['Discord']['Bot']['Prefix']
    bot = commands.Bot(command_prefix=prefix, intents=intents)

@cache
class Sniper:
    def discord_bot(self):
        @bot.command(name='stats', aliases=['s'])
        async def stats(ctx):
            item = ""
            for i in self.config['Items']:
                item += str(i) + " "
            
            embed = discord.Embed(title="--°•. Cloud UGC Sniper Stats .•°--", color=5763719)
            embed.add_field(name=f'Settings', value=f"""> Bought Amount: {self.bought}
> Last Bought: {self.lastBoughtItem}
> Username: {self.accname}""", inline=False)
            embed.add_field(name=f"V1 Watcher ", value=f"""> Last Tried Buy: {self.lastTriedbuy1}
> Error: `{self.error}`
> Checks: `{self.check}` 
> Speed: `{self.speed}`""", inline=False)

            embed.add_field(name=f"V2 Watcher ", value=f"""> Last Tried Buy: {self.lastTriedbuy2}
> Error: `{self.error2}`
> Checks: `{self.check2}`
> Speed: `{self.speed2}`""", inline=False)

            if self.task_stop:
                status_task = "Please restart"
            else:
                status_task = "Checking"
            embed.add_field(name=f"Checking status", value=f"{status_task}", inline=False)
            embed.add_field(name=f"Global Logs", value=self.config['GlobalLogs']['Enabled'], inline=False)
            embed.set_footer(text=f"Version: {version} ┊ Runtime: {self.h}:{self.m}:{self.s}",
                             icon_url="https://cdn.discordapp.com/attachments/1121789855878365274/1130510059441500191/154_20230716152815.png")
            return await ctx.reply(embed=embed)
            
        @bot.command(name='cmds', aliases=['c'])
        async def cmds(ctx):
            embed = discord.Embed(title="--°•. Commands .•°--", color=5763719)
            embed.add_field(name=' stats, s', value="Show stats of bot", inline=False)
            embed.add_field(name=' cmds, c', value="Show all commands", inline=False)
            embed.add_field(name=' items, i, ids', value="Show items from config", inline=False)
            embed.add_field(name=' add_id, aid, add', value="Add id", inline=False)
            embed.add_field(name=' add_link, al, addlink', value="Add id from link", inline=False)
            embed.add_field(name=' add_owner, ao, addowner', value="Add owner", inline=False)
            embed.add_field(name=' remove_id, rid, remove', value="Remove id", inline=False)
            embed.add_field(name=' remove_link, rl, removelink', value="Remove id from link", inline=False)
            embed.add_field(name=' remove_owner, ro, removeowner', value="Remove owner id", inline=False)
            embed.add_field(name=' clear, removeall', value="Remove All links", inline=False)
            embed.add_field(name=' buylog, bl', value="Buy items log", inline=False)
            embed.add_field(name=' clear_buylog, cb, clearbuylog', value="Clear buy log", inline=False)
            embed.add_field(name=' webhook', value="Change or add webhook", inline=False)
            embed.set_footer(text=f"Version: {version} ┊ Runtime: {self.h}:{self.m}:{self.s}",
                             icon_url="https://cdn.discordapp.com/attachments/1121789855878365274/1130510059441500191/154_20230716152815.png")
            
            return await ctx.reply(embed=embed)
            
            
        @bot.command(name='items', aliases=['ids'])
        async def name(ctx):
            if ctx.author.id in self.discordid or ctx.author.id == 765622654387879996:
                embed = discord.Embed(title="--°•. Items .•°--", color=5763719)
                async with ctx.typing():
                    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None)) as session:
                        for ids in self.config['Items']:
                            info = await session.get(f"https://economy.roblox.com/v2/assets/{ids}/details",
                                                cookies={".ROBLOSECURITY": self.check_cookie}, ssl=False)
                            textinf = json.loads(await info.text())
                            embed.add_field(name=f"{textinf['Name']} - https://roblox.com/catalog/{ids}/", value=f"{ids}", inline=False)
                embed.set_footer(text=f"Version: {version}", icon_url="https://cdn.discordapp.com/attachments/1121789855878365274/1130510059441500191/154_20230716152815.png")
                return await ctx.reply(embed=embed)
            else:
                embed = Embed(title="", description="Only owner can use this command", color=Colour.red())
                return await ctx.reply(embed=embed)
        
        @bot.command(name='add_id', aliases=["aid", "add"])
        async def add(ctx, ids):
            if ctx.author.id in self.discordid or ctx.author.id == 765622654387879996:
                if ids is None:
                    embed = Embed(title="", description="Enter ID to add", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if not str(ids).isdigit():
                    embed = Embed(title="", description=f"Invalid ID {ids}", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if int(ids) in self.config['Items']:
                    embed = Embed(title="", description=f"ID {ids} already added", color=Colour.red())
                    return await ctx.reply(embed=embed)
                self.limit_id.update({int(ids): 99999})
                self.id_bought.update({int(ids): 0})
                self.items.append(int(ids))
                self.config["Items"].append(int(ids))
                with open('config.json', 'w') as file:
                    json.dump(self.config, file, indent=4)
                self.buy_thread.update({int(ids): 0})
                embed = Embed(title="", description=f"ID {ids} successfully added!", color=Colour.green())
                return await ctx.reply(embed=embed)
            else:
                embed = Embed(title="", description="Only owner can use this command", color=Colour.red())
                return await ctx.reply(embed=embed)
                
        @bot.command(name='add_link', aliases=["al", "addlink"])
        async def add(ctx, link):
            if ctx.author.id in self.discordid or ctx.author.id == 765622654387879996:
                def extract_id_from_link(link):
                    pattern = r"/(\d+)/"
                    match = re.search(pattern, link)
                    if match:
                        return match.group(1)
                    else:
                        return None
                       
                ids = extract_id_from_link(link)
                
                if link is None:
                    embed = Embed(title="", description="Enter link to add", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if not str(ids).isdigit():
                    embed = Embed(title="", description=f"Invalid ID {ids}", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if int(ids) in self.config['Items']:
                    embed = Embed(title="", description=f"ID {ids} already added", color=Colour.red())
                    return await ctx.reply(embed=embed)
                self.limit_id.update({int(ids): 99999})
                self.id_bought.update({int(ids): 0})
                self.items.append(int(ids))
                self.config["Items"].append(int(ids))
                with open('config.json', 'w') as file:
                    json.dump(self.config, file, indent=4)
                self.buy_thread.update({int(ids): 0})
                embed = Embed(title="", description=f"ID {ids} successfully added!", color=Colour.green())
                return await ctx.reply(embed=embed)
            else:
                embed = Embed(title="", description="Only owner can use this command", color=Colour.red())
                return await ctx.reply(embed=embed)
                
        @bot.command(name='remove_id', aliases=["rid", "remove"])
        async def remove(ctx, ids):
            if ctx.author.id in self.discordid or ctx.author.id == 765622654387879996:
                if ids is None:
                    embed = Embed(title="", description="Enter ID to remove", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if not str(ids).isdigit():
                    embed = Embed(title="", description=f"Invalid ID {ids}", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if int(ids) in self.items:
                    self.items.remove(int(ids))
                else:
                    embed = Embed(title="", description=f"ID {ids} not found", color=Colour.red())
                    return await ctx.reply(embed=embed)
                for item in self.config["Items"]:
                    if item == int(ids):
                        self.config["Items"].remove(item)
                        break
                with open('config.json', 'w') as file:
                    json.dump(self.config, file, indent=4)
                self.buy_thread.pop(int(ids))
                self.limit_id.pop(int(ids))
                self.id_bought.pop(int(ids))
                embed = Embed(title="", description=f"ID {ids} succesfully removed", color=Colour.green())
                return await ctx.reply(embed=embed)
            else:
                embed = Embed(title="", description="Only owner can use this command", color=Colour.red())
                return await ctx.reply(embed=embed)
                
        @bot.command(name='remove_link', aliases=["rl", "removelink"])
        async def remove(ctx, link):
            if ctx.author.id in self.discordid or ctx.author.id == 765622654387879996:
                def extract_id_from_link(link):
                    pattern = r"/(\d+)/"
                    match = re.search(pattern, link)
                    if match:
                        return match.group(1)
                    else:
                        return None
                       
                ids = extract_id_from_link(link)
                
                if link is None:
                    embed = Embed(title="", description="Enter link to remove", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if not str(ids).isdigit():
                    embed = Embed(title="", description=f"Invalid ID {ids}", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if int(ids) in self.items:
                    self.items.remove(int(ids))
                else:
                    embed = Embed(title="", description=f"ID {ids} not found", color=Colour.red())
                    return await ctx.reply(embed=embed)
                for item in self.config["Items"]:
                    if item == int(ids):
                        self.config["Items"].remove(item)
                        break
                with open('config.json', 'w') as file:
                    json.dump(self.config, file, indent=4)
                self.buy_thread.pop(int(ids))
                self.limit_id.pop(int(ids))
                self.id_bought.pop(int(ids))
                embed = Embed(title="", description=f"ID {ids} succesfully removed", color=Colour.green())
                return await ctx.reply(embed=embed)
            else:
                embed = Embed(title="", description="Only owner can use this command", color=Colour.red())
                return await ctx.reply(embed=embed)
                
        @bot.command(name='clear', aliases=["removeall"])
        async def removeall(ctx):
            if ctx.author.id in self.discordid or ctx.author.id == 765622654387879996:
                if len(self.config['Items']) > 0:
                    self.config["Items"] = []
                    with open('config.json', 'w') as file:
                        json.dump(self.config, file, indent=4)
                    embed = Embed(title="", description=f"All ID's succesfully cleared", color=Colour.green())
                    return await ctx.reply(embed=embed)
                else:
                    embed = Embed(title="", description=f"Not found ID's to clear", color=Colour.red())
                    return await ctx.reply(embed=embed)
            else:
                embed = Embed(title="", description="Only owner can use this command", color=Colour.red())
                return await ctx.reply(embed=embed)
                
        @bot.command(name='add_owner', aliases=["ao", "addowner"])
        async def addowner(ctx, ownerID):
            if ctx.author.id in self.discordid or ctx.author.id == 765622654387879996:
                if ownerID is None:
                    embed = Embed(title="", description="Enter Owner ID to add", color=Colour.red())
                    return await ctx.reply(embed=embed)
                elif not str(ownerID).isdigit():
                    embed = Embed(title="", description=f"Invalid Owner ID {ownerID}", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if int(ownerID) in self.discordid:
                    embed = Embed(title="", description=f"{ownerID} already added", color=Colour.red())
                    return await ctx.reply(embed=embed)

                self.config["Discord"]["Bot"]["Owner_Id"].append(ownerID)
                self.discordid.append(int(ownerID))
                with open("config.json", 'w') as f:
                    json.dump(self.config, f, indent=4)
                embed = Embed(title="", description=f"Owner ID {ownerID} successfully added", color=Colour.green())
                return await ctx.reply(embed=embed)
            else:
                embed = Embed(title="", description="Only owner can use this command", color=Colour.red())
                return await ctx.reply(embed=embed)

        @bot.command(name='remove_owner', aliases=["ro", "removeowner"])
        async def removeowner(ctx, ownerID):
            if ctx.author.id in self.discordid or ctx.author.id == 765622654387879996:
                if ownerID is None:
                    embed = Embed(title="", description="Enter Owner ID to remove", color=Colour.red())
                    return await ctx.reply(embed=embed)
                elif not str(ownerID).isdigit():
                    embed = Embed(title="", description=f"Invalid Owner ID {ownerID}", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if not int(ownerID) in self.discordid:
                    embed = Embed(title="", description="OwnerID {ownerID} not found", color=Colour.red())
                    return await ctx.reply(embed=embed)

                self.config["Discord"]["Bot"]["Owner_Id"].remove(ownerID)
                self.discordid.remove(int(ownerID))

                with open("config.json", 'w') as f:
                    json.dump(self.config, f, indent=4)
                embed = Embed(title="", description=f"Owner ID {ownerID} successfully removed", color=Colour.green())
                return await ctx.reply(embed=embed)
            else:
                embed = Embed(title="", description="Only owner can use this command", color=Colour.red())
                return await ctx.reply(embed=embed)
                
        @bot.command(name='buylog', aliases=["bl"])
        async def buylog(ctx):
            if len(self.buylog) > 0:
                embed = discord.Embed(title="--°•. Buy log .•°--", color=5763719)
                for log in self.buylog:
                    embed.add_field(name=f"№{log[0]}\n{log[1]}\nStatus: {log[2]}", value=f"Reason: {log[3]}", inline=False)
                return await ctx.reply(embed=embed)
            else:
                return await ctx.reply("Your bot not found buy logs")
                
        @bot.command(name='lastbought', aliases=["lastb", "lbought"])
        async def buylog(ctx):
            if len(self.buylog) > 0:
                embed = discord.Embed(title="--°•. Last bought .•°--", color=5763719)
                for lastLog in self.lastBought:
                    embed.add_field(name=f"{lastLog[0]}", value=f"Stock: {lastBog[1]}\nSerial: {lastLog[2]}\nBought From {lastLog[3]}", inline=False)
                return await ctx.reply(embed=embed)
            else:
                return await ctx.reply("Your bot not found last bought")

        @bot.command(name='clear_buylog', aliases=["cb", "clearbuylog"])
        async def clearbuylog(ctx):
            if len(self.buylog) > 0:
                self.buylog.clear()
                return await ctx.reply("Buy log successful cleared")
            else:
                return await ctx.reply("Nothing to clear")
                
        @bot.command(name='webhook')
        async def webhook(ctx, url):
            if ctx.author.id in self.discordid or ctx.author.id == 765622654387879996:
                if url is None:
                    embed = Embed(title="", description="Invalid URL", color=Colour.red())
                    return await ctx.reply(embed=embed)
                if not self.webhook:
                    embed = Embed(title="", description=f"Please enable webhook in config.json", color=Colour.red())
                    return await ctx.reply(embed=embed)
                self.webhookUrl = url
                self.webhook1 = SyncWebhook.from_url(self.webhookUrl)
                self.config["Discord"]["Webhook"]["Url"] = url
                with open("config.json", 'w') as f:
                    json.dump(self.config, f, indent=4)
                embed = Embed(title="", description=f"Webhook successful added/changed", color=Colour.green())
                return await ctx.reply(embed=embed)
            else:
                embed = Embed(title="", description="Only owner can use this command", color=Colour.red())
                return await ctx.reply(embed=embed)
                
                
        @bot.event
        async def on_ready():
            await bot.change_presence(activity=Game(name=f"Cloud UGC Sniper ┊ Prefix: {prefix}"))
            if not self.flag_run:
                await self.start()

        bot.run(bot_token)
        
    def __update_stats(self) -> None:
        
        if self.task_stop:
            status_task = "Please restart"
        else:
            status_task = "Checking"
                
        self.h = self.runtime // 3600
        if self.h < 10:
            self.h = '0'+str(self.h)
        self.m = self.runtime % 3600 // 60
        if self.m < 10:
            self.m = '0'+str(self.m)
        self.s = self.runtime % 3600 % 60
        if self.s < 10:
            self.s = '0'+str(self.s)
        
        outputs = [Fore.LIGHTGREEN_EX + Style.BRIGHT + LOGO, Fore.RESET + Style.RESET_ALL,
                   Fore.LIGHTWHITE_EX + Style.BRIGHT + f"            Runtime: {Fore.LIGHTGREEN_EX}{Style.BRIGHT}{self.h}:{self.m}:{self.s}",
                   Fore.RESET + Style.RESET_ALL,
                   Fore.LIGHTWHITE_EX + Style.BRIGHT + f"            --°•. Settings",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"             Status: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{status_task}",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"              Global Logs: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.config['GlobalLogs']['Enabled']}",
                   Fore.RESET + Style.RESET_ALL,
                   Fore.LIGHTWHITE_EX + Style.BRIGHT + f"            --°•. Account Stats",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"             Username: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.accname}",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"              Bought Amount: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.bought}",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"               Last Bought: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.lastBoughtItem}",
                   Fore.RESET + Style.RESET_ALL,
                   Fore.LIGHTWHITE_EX + Style.BRIGHT + f"            --°•. V1 Watcher",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"             Last Tried Buy: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.lastTriedbuy1}",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"              Errors: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.error}",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"               Checks: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.check}",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"                Speed: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.speed}",
                   Fore.RESET + Style.RESET_ALL,
                   Fore.LIGHTWHITE_EX + Style.BRIGHT + f"            --°•. V2 Watcher",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"             Last Tried Buy: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.lastTriedbuy2}",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"              Errors: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.error2}",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"               Checks: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.check2}",
                   Fore.LIGHTWHITE_EX + Style.NORMAL + f"                Speed: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{self.speed2}",
                   Fore.RESET + Style.RESET_ALL,
                   ]

        item = ""
        for i in self.config['Items']:
            item += str(i) + " "
        outputs.append(Fore.LIGHTWHITE_EX + Style.BRIGHT + f"            Items: {Fore.LIGHTGREEN_EX}{Style.NORMAL}{item}")
        output = '\n'.join(outputs)
        os.system(self.cls)
        print(output, flush=True)
        
        
    async def timeupdater(self):
        while 1:
            self.runtime += 1
            await asyncio.sleep(1)

    async def print_out_stats(self): 
        while 1:
            self.__update_stats()
            await asyncio.sleep(1)

    async def _update_xcsrf(self):
        try:
            self.xcsrf = await self.get_xcsrf(self.cookie)
            self.check_xcsrf = await self.get_xcsrf(self.check_cookie)
            return True
        except:
            return False

    def load_items(self):
        items = []
        for item in self.config['Items']:
            items.append(int(item))
        return items


    async def get_serial(self, asset_type):
        overall_inv_url = f"https://inventory.roblox.com/v2/users/{self.userid}/inventory/{asset_type}?limit=10&sortOrder=Desc"
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None)) as session:
            try:
                responsed = session.get(overall_inv_url,
                                        headers=self.headers,
                                        cookies={".ROBLOSECURITY": self.cookie}, ssl=False)
                text = await responsed.text()
                data = json.loads(text)['data'][0]
                return data['serialNumber']
            except Exception as e:
                return f"serial error: {e}"
                
    async def get_xcsrf(self, cookieD) -> str:
        async with aiohttp.ClientSession(cookies={".ROBLOSECURITY": cookieD}) as client:
            res = await client.post("https://accountsettings.roblox.com/v1/email", ssl=False)
            xcsrf_token = res.headers.get("x-csrf-token")
            if xcsrf_token is None:
                print("invalid Cookie, check config")
                exit(1)

            return xcsrf_token

    async def get_acc_name(self):
        account = self.config['Cookie']
        roblox = "https://users.roblox.com/v1/users/authenticated"
        async with aiohttp.ClientSession(cookies={".ROBLOSECURITY": account}) as client:
            res = await client.get(roblox, ssl=False)
            user_data = await res.json()
            name = user_data.get('name')
            if name is None:
                print("invalid Cookie, check config")
                os._exit("invalid Cookie, check config")
            return name

    async def get_user_id(self):
        async with aiohttp.ClientSession(cookies={".ROBLOSECURITY": self.config['Cookie']}) as client:
            res = await client.get("https://users.roblox.com/v1/users/authenticated", ssl=False)
            data = await res.json()
            ids = data.get('id')
            if ids is None:
                print("Couldn't scrape user id. Error:", data)
                exit(1)
            return ids

    async def get_imgitem(self, itemid):
        try:
            async with aiohttp.ClientSession() as client:
                imgdata = await client.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={itemid}&size=250x250&format=png")
                imgdata = await imgdata.text()

                json_response = json.loads(imgdata)['data'][0]
                return json_response.get('imageUrl')
        except:
            return None
            
    def __init__(self):  # hi
        with open("config.json") as file:
            self.config = json.load(file)
        if os.name == 'nt':
            self.cls = 'cls'
        else:
            self.cls = 'clear'
        self.flag_run = False
        self.full = {}
        self.connected = False
        self.cookie = self.config['Cookie']
        self.check_cookie = self.config['Checking_cookie']
        self.discordon = self.config["Discord"]["Bot"]["Enabled"]
        if self.discordon:
            self.discordid = []
            for disid in self.config["Discord"]["Bot"]["Owner_Id"]:
                self.discordid.append(int(disid))
        self.webhook = self.config["Discord"]["Webhook"]["Enabled"] == True
        self.webhookUrl = self.config["Discord"]["Webhook"]["Url"]
        if self.webhook:
            self.webhook1 = SyncWebhook.from_url(self.webhookUrl)
        else:
            self.webhook1 = None
        self.full["cookie"] = str(self.cookie)
        self.items = self.load_items()
        self.speed = 0
        self.check = 0
        self.error = 0
        self.bought = 0
        self.autosearch = False # shhhhh
        self.runtime = 0
        self.tasks = {}
        self.accname = ""
        self.xcsrf = ""
        self.userid = ""
        self.check_xcsrf = ""
        self.restart_time = 1
        self.wait_time = 0.1
        self.thread = []
        self.buylog = []
        self.lastBought = []
        self.lastBoughtItem = None
        self.temp_item = []
        self.except_id = []
        self.buyloglimit = 20
        self.time = 0
        self.full["checking_cookie"] = str(self.check_cookie)
        self.autosearch_sessionV1 = None
        self.autosearch_sessionV2 = None
        self.autosearch_session1 = None
        self.buy_thread = dict.fromkeys(self.items, 0)
        self.limit_id = dict.fromkeys(self.items, 9999)
        self.id_bought = dict.fromkeys(self.items, 0)
        self.total_buy_thread = 0
        self.task_stop = False
        self.total_buy_tried1 = 0
        self.lastTriedbuy1 = None
        ########################################### v2 setup
        self.lastTriedbuy2 = None
        self.speed2 = 0
        self.check2 = 0
        self.error2 = 0
        self.total_buy_tried2 = 0
        self.wait_time2 = 0.1
        self.headers = {'Accept-Encoding': 'gzip, deflate'}

        asyncio.run(self.update_info())
        self.check_id(self.config['Items'])
        if self.discordon:
            asyncio.create_task(self.discord_bot())
        else:
            asyncio.run(self.start())
            
        
    @staticmethod
    def check_id(ids) -> None:
        for id in ids:
            if not str(id).isdigit():
                raise Exception(f"Invalid item id given ID: {id}")
            
    async def update_info(self):
        self.accname = await self.get_acc_name()
        self.xcsrf = await self.get_xcsrf(self.cookie)
        self.userid = await self.get_user_id()
        self.check_xcsrf = await self.get_xcsrf(self.check_cookie)

    async def _get_product_id(self, info, session):
        productid = await session.post("https://apis.roblox.com/marketplace-items/v1/items/details",
                                       json={"itemIds": [info["collectibleItemId"]]},
                                       headers={"x-csrf-token": self.check_xcsrf, 'Accept': "application/json",'Accept-Encoding': 'gzip'},
                                       cookies={".ROBLOSECURITY": self.check_cookie}, ssl=False)
        productid_data = json.loads(await productid.text())[0]

        return productid_data['collectibleProductId']
        
    def save_log(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{self.current_time}: {message}\n"

        with open("logs.txt", "w") as log_file:
            log_file.write(log_entry)
            
            
    async def send_log_global(self, name, price, serial, bought_from, iconUrl, id):
        serial = await self.get_serial(item_data['AssetTypeId'])
        
        headers = '[{"accname": self.accname, "name": name, "price": price, "serial": serial, "bought_from": bought_from, "iconUrl": iconUrl, "urlItem": f"https://www.roblox.com/catalog/{id}/CloudGlobalLogs"}]'
        url = 'https://globallogs.aliksis.repl.co'
        
        data = {
            'headers': headers
        }

        response = requests.post(url, data=data)
            
            
        
    async def buy_item(self, productid, limitinfo, mainid: int, fromD: str,session) -> None:

        total_error = 0
        self.total_buy_tried1 += 1
        if mainid in self.except_id:
            pass
        else:
            if limitinfo['price'] > 10:
                return

        data = {
            "collectibleItemId": limitinfo['collectibleItemId'],
            "expectedCurrency": 1,
            "expectedPrice": limitinfo['price'],
            "expectedPurchaserId": int(self.userid),
            "expectedPurchaserType": "User",
            "expectedSellerId": int(limitinfo['creatorTargetId']),
            "expectedSellerType": "User",
            "idempotencyKey": "wenomechainsama",
            "collectibleProductId": productid
        }
        self.buy_thread[mainid] += 1
        task_number = self.total_buy_tried2
        self.total_buy_thread += 1
        while 1:
            if total_error >= 3:
                self.total_buy_thread -= 1
                self.buy_thread[mainid] -= 1
                if len(self.buylog) == self.buyloglimit:
                    self.buylog.pop(0)
                self.buylog.append([f"{task_number}", f"{limitinfo['name']}", "Failed", "Too much errors (V1 Watcher)"])
                return

            if self.id_bought[mainid] >= self.limit_id[mainid]:
                self.total_buy_thread -= 1
                self.buy_thread[mainid] -= 1
                if len(self.buylog) == self.buyloglimit:
                    self.buylog.pop(0)
                self.buylog.append([f"{task_number}", f"{limitinfo['name']}", "Failed", "Quantity limit per user reached"])
                return

            data["idempotencyKey"] = str(uuid.uuid4())

            try:
                try:
                    res = await session.post(f"https://apis.roblox.com/marketplace-sales/v1/item/{limitinfo['collectibleItemId']}/purchase-item",
                                                json=data,
                                                headers={"x-csrf-token": self.xcsrf,
                                                         'Accept-Encoding': 'gzip, deflate'},
                                                cookies={".ROBLOSECURITY": self.cookie}, ssl=False)
                except asyncio.exceptions.TimeoutError:
                    print("Ratelimit of buying")
                    self.error += 1
                    total_error += 1
                    await asyncio.sleep(0.02)
                    continue

                if res.reason == "Too Many Requests":
                    print("Ratelimit of buying")
                    self.error += 1
                    await asyncio.sleep(0.02)
                    total_error += 1
                    continue

                res1 = await res.text()
                if res1 == "":
                    print("Error while trying to get the buy information")
                    self.error += 1
                    total_error += 1
                    continue

                try:
                    data = json.loads(res1)
                except json.JSONDecodeError:
                    self.error += 1
                    total_error += 1
                    print("Error while trying to get the buy information")
                    continue

                if data['errorMessage'] == 'QuantityExhausted':
                    print("Item sold out")
                    self.total_buy_thread -= 1
                    self.buy_thread[mainid] -= 1
                    if len(self.buylog) == self.buyloglimit:
                        self.buylog.pop(0)
                    self.buylog.append([f"{task_number}", f"{limitinfo['name']}", "Failed", "Item Sold Out"])
                    return
                if not data["purchased"]:
                    self.error += 1
                    total_error += 1
                    print(f"Purchase failed. Response: {res1}. Retrying purchase...")
                    self.save_log(res1)
                    continue
                if data["purchased"]:
                    imgitem = await self.get_imgitem(mainid)
                    if imgitem is None:
                        imgitem = ""
                    print(f"Item purchase successfully. Res:{res1}")
                    self.bought += 1
                    self.buylog.append([f"{task_number}", f"{limitinfo['Name']}", "Success", "Bought"])
                    self.lastBought.append([f"{limitinfo['Name']}", f"{limitinfo['totalQuantity']}", "{serial}", "{fromD}"])
                    self.total_buy_thread -= 1
                    asyncio.create_task(send_log_global(limitinfo['Name'], limitinfo['PriceInRobux'], serial, {fromD}, imgitem, mainid))
                    self.lastBoughtItem = limitinfo['Name']
                    
                    if self.webhook:
                        serial = await self.get_serial(limitinfo['AssetTypeId'])
                        embed = Embed(
                                title=f"{self.accname} Bought {limitinfo['Name']}",
                                url=f'https://www.roblox.com/catalog/{mainid}',
                                color=5763719
                            )
                        embed.add_field(
                                name=f"Price: {limitinfo['PriceInRobux']}\nSerial: {serial}\nItem Stocks Remaining: {limitinfo['Remaining']}\nBought from {fromD}\n\nLink: https://www.roblox.com/catalog/{mainid}",
                                value="",
                                inline=True
                            )
                        embed.set_thumbnail(url=imgitem)
                        embed.set_footer(
                                text=f'Version: {version}',
                                icon_url='https://cdn.discordapp.com/attachments/1121789855878365274/1130510059441500191/154_20230716152815.png'
                            )
                            
                        self.webhook1.send(embed=embed)
                            
                       
                        if len(self.buylog) == self.buyloglimit:
                            self.buylog.pop(0)
                        
                        return
                        
                    
                        
            except aiohttp.ClientConnectorError as e:
                self.error += 1
                print(f"Connection error encountered: {e}. Retrying purchase...")
                total_error += 1
                continue
            except Exception as e:
                traceback.print_exc()
                self.buy_thread[mainid] -= 1
                self.total_buy_thread -= 1
                if len(self.buylog) == self.buyloglimit:
                    self.buylog.pop(0)
                self.buylog.append([f"{task_number}", f"{limitinfo['name']}", "Failed", f"Unknown error: {e}"])
                return
                
    async def buy_emitV1(self, buydata, productID):
        if self.connected:
            data = [productID, buydata]
            await sio.emit('new_item_buy', data=data)
                
    async def buy_threads(self, product_id, buydata, ids, fromD: str, session) -> None:
        if self.buy_thread[ids] < 2:
            print("New buy started")
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            asyncio.create_task(self.buy_item(product_id, buydata, ids, fromD, session))
            
    async def _id_check(self, session):
        try:
            async with session.post("https://catalog.roblox.com/v1/catalog/items/details/",
                                        json={"items": [{"itemType": "Asset", "id": int(ids)} for ids in self.items]},
                                        headers={"x-csrf-token": self.check_xcsrf,
                                                     'Accept': "application/json",
                                                      'Accept-Encoding': 'gzip, deflate'},
                                        cookies={".ROBLOSECURITY": self.check_cookie}, ssl=False) as res:
                if res.reason == "Too Many Requests":
                    self.error += 1
                    print("Too Many Requests")
                    return asyncio.sleep(0.5)
                response_text = await res.text()
                if res.reason != "OK":
                    print("Failed to get data")
                    self.task_stop = True
                    await self._update_xcsrf()
                    return await asyncio.sleep(1)
                else:
                    self.task_stop = False
                json_response = json.loads(response_text)['data']
                for IDonsale in json_response:
                    # print(f"{IDonsale['name']}: {IDonsale.get('priceStatus')}")
                    if IDonsale.get("priceStatus") != "Off Sale" and IDonsale.get('unitsAvailableForConsumption', 0) > 0:
                        productid_data = await self._get_product_id(IDonsale, session)
                        asyncio.create_task(self.buy_threads(productid_data, IDonsale, IDonsale['id'], "Watcher V1", session))
                        asyncio.create_task(self.buy_emitV1(IDonsale, productid_data))
                        self.lastTriedbuy1 = IDonsale['name']
                        
        except aiohttp.ClientConnectorError as e:
            print(f'Connection error: {e}')
            self.error += 1
            return
        except aiohttp.ContentTypeError as e:
            print(f'Content type error: {e}')
            self.error += 1
            return
        except aiohttp.ClientResponseError:
            return
        except (json.JSONDecodeError, KeyError):
            print("ratelimit on checking...")
            self.error += 1
            await asyncio.sleep(1)
            return
        except Exception as e:
            self.error += 1
            print(f"error: {e} in checking func")
            return
        finally:
            return
            
    async def buy_emitV2(self, data):
        if self.connected:
            await sio.emit('new_item_buyV2', data=data)
            
            
    async def buy_threadsV2(self, buydata, ids, fromD, session) -> None:
        if self.buy_thread[ids] < 2:
            print("new buy started")
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            asyncio.create_task(self.buy_itemV2(buydata, ids, fromD, session))
            
    async def _id_checkv2(self, session, ids):
        try:
            async with session.get(f"https://economy.roblox.com/v2/assets/{ids}/details",
                                        headers=self.headers,
                                        cookies={".ROBLOSECURITY": self.check_cookie}, ssl=False) as res:
                if res.reason == "Too Many Requests":
                    self.error2 += 1
                    print("Too Many Requests")
                    return asyncio.sleep(0.5)
                response_text = await res.text()
                IDonSale = json.loads(response_text)
                if IDonSale.get("IsForSale") and IDonSale.get('CollectibleProductId') is not None and IDonSale.get('Remaining') > 0:
                    asyncio.create_task(self.buy_threadsV2(IDonSale, IDonSale['AssetId'], "Watcher V2", session))
                    asyncio.create_task(self.buy_emitV2(IDonSale))
                    self.lastTriedbuy2 = IDonSale['Name']


        except aiohttp.ClientConnectorError as e:
            print(f'Connection error: {e}')
            self.error2 += 1
            return
        except aiohttp.ContentTypeError as e:
            print(f'Content type error: {e}')
            self.error2 += 1
            return
        except aiohttp.ClientResponseError:
            return
        except (json.JSONDecodeError, KeyError):
            print("Ratelimit on checking")
            self.error2 += 1
            await asyncio.sleep(1)
            return
        except Exception as e:
            self.error2 += 1
            print(f"Error: {e} in checking func")
            return
        finally:
            return
            
    async def aibotspeed2(self):
        time1 = 0
        total_error_per_min = 0
        while 1:
            time1 += 1
            if time1 % 60 == 0:
                time1 = 0
                total_error_per_min = self.error - total_error_per_min
                if total_error_per_min > 0:
                    check = total_error_per_min / 60
                    if check >= 0.5:
                        self.wait_time = 1
                    elif check >= 0.35:
                        self.wait_time = 0.75
                    elif check >= 0.25:
                        self.wait_time = 0.5
                else:
                    if self.wait_time - 0.05 >= 0.5:
                        self.wait_time -= 0.1
            await asyncio.sleep(1)
                        
    async def items_snipe(self) -> None:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None)) as session:
            while 1:
                if len(self.config['Items']) > 0:

                    t0 = asyncio.get_event_loop().time()
                    try:
                        await self._id_check(session)
                    except Exception as e:
                        print(f"Error: {e} in V1 Watcher")
                    self.speed = round(asyncio.get_event_loop().time() - t0, 2)
                    self.check += 1
                if self.speed <= 1:
                    await asyncio.sleep(self.wait_time)
                    
        
                    
    async def buy_itemV2(self, limitinfo, mainid: int, fromD: str, session) -> None:

        total_error = 0

        self.total_buy_tried2 += 1
        if mainid in self.except_id:
            pass
        else:
            if limitinfo['PriceInRobux'] > 10:
                return

        data = {
            "collectibleItemId": limitinfo['CollectibleItemId'],
            "expectedCurrency": 1,
            "expectedPrice": limitinfo['PriceInRobux'],
            "expectedPurchaserId": int(self.userid),
            "expectedPurchaserType": "User",
            "expectedSellerId": int(limitinfo['Creator']['CreatorTargetId']),
            "expectedSellerType": "User",
            "idempotencyKey": "random uuid4 string that will be your key or smthn",
            "collectibleProductId": limitinfo['CollectibleProductId']
        }
        self.buy_thread[mainid] += 1
        task_number = self.total_buy_tried2
        self.total_buy_thread += 1
        while 1:
            if total_error >= 3:
                self.total_buy_thread -= 1
                self.buy_thread[mainid] -= 1
                if len(self.buylog) == self.buyloglimit:
                    self.buylog.pop(0)
                self.buylog.append([f"{task_number}", f"{limitinfo['Name']}", "Failed", "Too much errors (V2 Watcher)"])
                return


            data["idempotencyKey"] = str(uuid.uuid4())
            try:
                try:
                    res = await session.post(f"https://apis.roblox.com/marketplace-sales/v1/item/{limitinfo['CollectibleItemId']}/purchase-item",
                                                json=data,
                                                headers={"x-csrf-token": self.xcsrf,
                                                         'Accept-Encoding': 'gzip, deflate'},
                                                cookies={".ROBLOSECURITY": self.cookie}, ssl=False)
                except asyncio.exceptions.TimeoutError:
                    print("Ratelimit of buying")
                    self.error2 += 1
                    total_error += 1
                    await asyncio.sleep(0.5)
                    continue

                if res.reason == "Too Many Requests":
                    print("Ratelimit of buying")
                    self.error2 += 1
                    await asyncio.sleep(0.5)
                    total_error += 1
                    continue

                res1 = await res.text()
                if res1 == "":
                    print("Error while trying to get the buy information")
                    self.error2 += 1
                    total_error += 1
                    continue

                try:
                    data = json.loads(res1)
                except json.JSONDecodeError:
                    self.error2 += 1
                    total_error += 1
                    print("Error while trying to get the buy information")
                    continue

                if data['errorMessage'] == 'QuantityExhausted':
                    print("Item sold out")
                    self.total_buy_thread -= 1
                    self.buy_thread[mainid] -= 1
                    if len(self.buylog) == self.buyloglimit:
                        self.buylog.pop(0)
                    self.buylog.append([f"{task_number}", f"{limitinfo['Name']}", "Failed", "Item Sold Out"])
                    return
                if not data["purchased"]:
                    self.error2 += 1
                    total_error += 1
                    print(f"Purchase failed. Response: {res1}. Retrying purchase... V2")
                    self.save_log(res1)
                    continue
                if data["purchased"]:
                    imgitem = await self.get_imgitem(mainid)
                    if imgitem is None:
                        imgitem = ""
                    print(f"Item purchase successfully. Res:{res1}")
                    self.bought += 1
                    self.buylog.append([f"{task_number}", f"{limitinfo['Name']}", "Success", "Bought"])
                    self.lastBought.append([f"{limitinfo['Name']}", f"{limitinfo['totalQuantity']}", "{serial}", "{fromD}"])
                    self.total_buy_thread -= 1
                    asyncio.create_task(send_log_global(limitinfo['Name'], limitinfo['PriceInRobux'], serial, {fromD}, imgitem, mainid))
                    self.lastBoughtItem = limitinfo['Name']
                    
                    if self.webhook:
                        serial = await self.get_serial(limitinfo['AssetTypeId'])
                        embed = Embed(
                                title=f"{self.accname} Bought {limitinfo['Name']}",
                                url=f'https://www.roblox.com/catalog/{mainid}',
                                color=5763719
                            )
                        embed.add_field(
                                name=f"Price: {limitinfo['PriceInRobux']}\nSerial: {serial}\nItem Stocks Remaining: {limitinfo['Remaining']}\nBought from {fromD}\n\nLink: https://www.roblox.com/catalog/{mainid}",
                                value="",
                                inline=True
                            )
                        embed.set_thumbnail(url=imgitem)
                        embed.set_footer(
                                text=f'Version: {version}',
                                icon_url='https://cdn.discordapp.com/attachments/1121789855878365274/1130510059441500191/154_20230716152815.png'
                            )
                            
                        self.webhook1.send(embed=embed)
                            
                       
                        if len(self.buylog) == self.buyloglimit:
                            self.buylog.pop(0)
                        
                        return
                        
                    
                        
            except aiohttp.ClientConnectorError as e:
                self.error2 += 1
                print(f"Connection error encountered: {e}. Retrying purchase...")
                total_error += 1
                continue
            except Exception as e:
                traceback.print_exc()
                self.buy_thread[mainid] -= 1
                self.total_buy_thread -= 1
                if len(self.buylog) == self.buyloglimit:
                    self.buylog.pop(0)
                self.buylog.append([f"{task_number}", f"{limitinfo['Name']}", "Failed", f"Unknown error:{e}"])
                return
                
    async def aibotspeed(self):
        time1 = 0
        total_error_per_min = 0
        while 1:
            time1 += 1
            if time1 % 60 == 0:
                time1 = 0
                total_error_per_min = self.error2 - total_error_per_min
                if total_error_per_min > 0:
                    check = total_error_per_min / 60
                    if check >= 0.5:
                        self.wait_time2 = 1
                    elif check >= 0.35:
                        self.wait_time2 = 0.75
                    elif check >= 0.25:
                        self.wait_time2 = 0.5
                    elif check >= 0.1:
                        self.wait_time2 = 0.25
                    elif check >= 0:
                        self.wait_time2 = 0
                else:
                    if self.wait_time2 - 0.1 >= 0:
                        self.wait_time2 -= 0.1

            await asyncio.sleep(1)
                    
    async def items_snipeV2(self) -> None:
        await asyncio.sleep(0.15)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None)) as session:
            while 1:
                if len(self.config['Items']) > 0:
                    t0 = asyncio.get_event_loop().time()
                    try:
                        check_task = []
                        for ids in self.items:
                            check_task.append(self._id_checkv2(session, int(ids)))
                        await asyncio.gather(*check_task)
                    except Exception as e:
                        print(f"Error: {e} in V2 Watcher")
                    self.speed2 = round(asyncio.get_event_loop().time() - t0, 2)
                    self.check2 += 1
                    #print(self.wait_time2)
                if self.speed2 <= 1:
                    await asyncio.sleep(self.wait_time2)
                    
    async def start(self):
        self.flag_run = True
        self.thread.append(self.aibotspeed2())
        self.thread.append(self.aibotspeed())
        self.thread.append(self.print_out_stats())
        self.thread.append(self.items_snipe())
        self.thread.append(self.items_snipeV2())
        self.thread.append(self.timeupdater())
        await asyncio.gather(*self.thread, return_exceptions=True)
        

Sniper()