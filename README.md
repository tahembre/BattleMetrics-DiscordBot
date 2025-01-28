# Discord Server Info Bot  

This bot displays server information (such as players online, maximum players, and in-game time) as its status on Discord. It uses the BattleMetrics API to fetch data and updates the bot's status regularly.  

---

## Features  
- Fetches player count, maximum player capacity, and in-game time for servers listed in the configuration file (`bmchecker.ini`).  
- Updates Discord bot status to reflect the number of players online or other server-specific information.  
- Handles multiple servers seamlessly, providing aggregated player data for all listed servers.  
- Logs additional server details (e.g., name, IP, port, rank, and status) to the console for debugging purposes.  

---

## Supported Games  

The bot currently supports the following games:  

- **Players online and In-game Time**:  
  - Scum  
  - DayZ  
  - Ark: Survival Ascended  

- **Players online and Days on server**:  
  - Ark: Survival Evolved  

Other games are also supported by the script. You can modify the JSON request in the script to accommodate additional games and their specific data fields.

---

## Prerequisites  
Before running the bot, ensure you have:  
1. Python installed (version 3.8 or higher recommended).  
2. A Discord bot token created from the [Discord Developer Portal](https://discord.com/developers/applications).  
3. A `bmchecker.ini` file configured with your Discord bot token and BattleMetrics server IDs (details below).  

---

## Configuration (`bmchecker.ini`)  

Create a `bmchecker.ini` file in the same directory as the script with the following structure:  

```ini  
[settings]  
discordbot_token = YOUR_DISCORD_BOT_TOKEN  
battlemetrics_IDs = SERVER_ID1  
# If you have multiple servers, separate their IDs with a newline:  
# SERVER_ID2  
# SERVER_ID3  
