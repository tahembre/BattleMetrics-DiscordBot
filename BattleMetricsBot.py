## // LETS IMPORT THE REQUIRED MODULES.
## // FIRST, WE NEED DISCORD - WE WONT USE ALL THOSE FUNCTIONS, BUT THIS IS
## // BASICLY MY TEMPLATE TO INCLUDE THE FEATURES U USE THE MOST
try:
    import time
    import discord
    from discord.ext import commands

    ## //  SECOND, WE'LL NEED CONFIGPARSER TO READ THE VALUES FROM THE INI-FILE PROVIDED
    from configparser import ConfigParser
    ## // WE DEFINE A NAME FOR THE MODULE BELOW:
    config = ConfigParser()

    ## // WE CALL THAT MODULE > READ TO READ OUT THE ENTIRE FILE ONCE:
    config.read('bmchecker.ini', encoding='utf-8')

    ## // NOW WE NEED TO SET A DEFINITION OF THE DIFFERENT VALUES WHICH WE CAN CALL THROUGHOUT THIS SCRIPT:
    discordtoken = config.get('settings', 'discordbot_token')
    servers = config.get('settings', 'battlemetrics_IDs')

    ## // ALL SET - LETS SET THE DIFFERENT OPTIONS FOR THE DISCORD MODULE:
    intents = discord.Intents.default()
    intents.members = True
    client = commands.Bot(intents=intents, command_prefix=".")

    ## // NOW, LETS IMPORT THE 2 LAST FUNCTIONS WE NEED:
    ## // REQUESTS - WE USE THIS TO SEND A REQUEST TO THE BATTLEMETRICS API TO RECEIVE THE SERVER INFORMATION:
    import requests

    ## // ASYNCIO IS A MODULE ALLOWING THE SCRIPT TO RUN MULTIPLE TASKS ALONGSIDE / MULTIPROCESSING:
    import asyncio

    ## // CREATE A FUNCTION:
    ## // ASYNC: ASYNCHRONIOUS TASK || DEF: DEFINITION, THIS IS TELLING THE PROGRAMMING LANGUAGE THIS IS THE DEFINITION
    ## // OF A TASK WE WANT TO CALL LATER || BOTSTATUS : NAME OF THE TASK
    async def botstatus():
        ## // WE NEED A VALUE WHERE WE CAN ADD THE AMOUNT OF PLAYERS FROM EACH SERVER, LETS NAME IT "COUNT"
        count = 0
        ## // NOW, WE WANT TO CHECK IF THE BATTLEMETRICS ID IN THE CONFIG GOT ONE OR MULTIPLE ENTRIES, WE DO THIS BY SPLITTING
        ## // THE VALUE AT EACH NEWLINE LIKE SHOWN BELOW:
        bm_ids = servers.split('\n')
        ## // NOW, LEN(BM_IDS) WILL RETURN WITH THE LENGTH OF THE LIST WE JUST MADE ABOVE. IF IT ONLY GOT ONE BATTLEMETRICS ID
        ## // THE LENGTH OF THE LIST IS 1 LINE, SO WE ONLY WANT TO HANDLE IT AS A LIST IF THE LENGTH IS HIGHER THAN 1:
        ## // COUNT IS GIVING YOU THE TOTAL PLAYERS ONLINE IN ALL YOUR GIVEN SERVERS (FOR MULTI SERVER OWNERS)
        if len(bm_ids) > 1:
            for ids in bm_ids:
                try:
                    res = requests.get(f'https://api.battlemetrics.com/servers/{ids}')
                    players = (res.json()['data']['attributes']['players'])
                    count += int(players)
                    maxPlayers = (res.json()['data']['attributes']['maxPlayers'])
                    servertime = (res.json()['data']['attributes']['details']['time'])
                    print(f'{players} / {maxPlayers} @ {servertime}')
                except:
                    pass
            ## // THIS IS INSIDE THE STATEMENT IF LEN(BM_IDS) > 1, BUT OUTSIDE THE FOR IDS IN BMIDS (GOING THROUGH THE LIST)
            await client.change_presence(status=discord.Status.online,
                                         activity=discord.Activity(type=discord.ActivityType.watching,
                                                                   name=f'{count} players online!'))

        ## // IF THE LENTGH OF THE LIST IS 1, WE DONT WANT TO SPLIT THE OPTION, SO WE GO AHEAD AND JUST CALL THE
        ## // BATTLEMETRICS ID FROM THE CONFIG! SINCE WE NOW ONLY GOT ONE SERVER, WE'LL ADD THE SERVERTIME ASWELL!
        if len(bm_ids) == 1:
            try:
                ## // {servers} is the value we called at line 19 to get the value from the config.

                res = requests.get(f'https://api.battlemetrics.com/servers/{servers}')

                game = (res.json()['data']['relationships']['game']['data']['id'])
                print(game)

                print(res.json()['data']['attributes']['name'])                             ## // SERVER NAME
                print(res.json()['data']['attributes']['ip'])                               ## // SERVER IP
                print(res.json()['data']['attributes']['port'])                             ## // SERVER PORT
                print(res.json()['data']['attributes']['rank'])                             ## // SERVER RANK
                print(res.json()['data']['attributes']['status'])                           ## // SERVER STATUS (OFFLINE / ONLINE / DEAD)

                players = (res.json()['data']['attributes']['players'])                     ## // CURRENT PLAYERS ONLINE
                maxPlayers = (res.json()['data']['attributes']['maxPlayers'])               ## // MAX PLAYERS / SERVER SLOTS
                servertime = (res.json()['data']['attributes']['details']['time'])          ## // INGAME TIME (IF ACCESSIBLE)



                count += int(players)
                print(f'{players} / {maxPlayers} @ {servertime}')
            except:
                pass
            if str(game) == 'ark':
                await client.change_presence(status=discord.Status.online,
                                             activity=discord.Activity(type=discord.ActivityType.watching,
                                                                       name=f'{players} / {maxPlayers} @ Day {servertime}'))
            else:
                await client.change_presence(status=discord.Status.online,
                                             activity=discord.Activity(type=discord.ActivityType.watching,
                                                                       name=f'{players} / {maxPlayers} @ {servertime}'))
    ## // WITH EVERYTHING ABOVE READY, WE'RE READY TO LAUNCH THE BOT. WE'LL CREATE A LOOP LAUNCHING THE TASK ABOVE
    ## // AND WE'LL ADD A SIMPLE PAUSE WITH ASYNCIO.SLEEP(SECONDS) TO PREVENT IT FROM GETTING THE NUMBERS EVERY 0.01 SECONDS!
    @client.event
    async def on_ready():
        while True:
            await botstatus()
            await asyncio.sleep(120)

    ## // WE'RE ALL SET - LETS FIRE UP THIS BADBOY!
    client.run(f'{discordtoken}')
except Exception as error:
    print(error)
    time.sleep(60)