import discord
from keep_alive import run  # Importiere den Webserver
import threading  # Hier das threading-Modul importieren
import time
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

GUILD_ID = os.getenv('GUILD_ID')
ROLE_ID = os.getenv('ROLE_ID')

TRIGGER_WORD_UP = '@Servers Up'  # Trigger-Text für Server online
TRIGGER_WORDS_CLOSED = [
    "All other servers are now closed",
    "all servers are now closed"
]  # Trigger-Text für Server offline

ANNOUNCEMENT_CHANNEL_ID = os.getenv('ANNOUNCEMENT_CHANNEL_ID')
TARGET_CHANNEL_ID = os.getenv('TARGET_CHANNEL_ID')

# 🔹 Intents aktivieren
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)


# Starte den Webserver in einem neuen Thread
t = threading.Thread(target=run)
t.start()

# Variable zur Vermeidung von Spam: Speichert den Zeitpunkt der letzten Nachricht
last_sent_time = 0
cooldown_time = 10  # Zeit in Sekunden, um doppelte Nachrichten zu verhindern



@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user}')
    guild = client.get_guild(int(GUILD_ID))
    if guild:
        print(f'Bot ist auf dem Server: {guild.name}')
    else:
        print('Der Bot konnte den Server nicht finden.')

@client.event
async def on_message(message):
    global last_sent_time  # Verwende die globale Variable für den letzten Versandzeitpunkt
    
    # Debug: Zeige die erhaltene Nachricht
    print(f"Neue Nachricht erhalten: {message.content}")
    
    # Debug: Zeige den Kanal, von dem die Nachricht kommt
    print(f"Nachricht kommt aus Kanal: {message.channel.name} (ID: {message.channel.id})")
    
    # Überprüfen, ob die Nachricht vom richtigen Kanal kommt und ob der Bot nicht auf seine eigene Nachricht reagiert
    if message.channel.id == int(ANNOUNCEMENT_CHANNEL_ID) and message.author != client.user:
        print(f"Nachricht kommt aus dem Announcement-Kanal!")

        # Überprüfen, ob der Kanal ein Announcement-Kanal ist (nur für Nachrichten aus Announcement-Kanälen)
        if isinstance(message.channel, discord.TextChannel) and message.channel.type == discord.ChannelType.news:
            print(f"Es handelt sich um eine Nachricht aus einem Announcement-Kanal!")

        # Überprüfen, ob die Nachricht im Cooldown ist
        current_time = time.time()
        if current_time - last_sent_time < cooldown_time:
            print(f"Zu schnell! Der Bot wartet noch auf Cooldown.")
            return  # Verhindert, dass der Bot die Nachricht erneut sendet

        # Prüfen, ob das Triggerwort für "Servers Up" enthalten ist
        if TRIGGER_WORD_UP in message.content:
            print(f"Triggerwort '{TRIGGER_WORD_UP}' gefunden!")
            target_channel = client.get_channel(int(TARGET_CHANNEL_ID))
            if target_channel:
                print(f"Nachricht wird in den Ziel-Kanal {target_channel.name} gesendet.")
                await target_channel.send(f"# 🚀 Server sind wieder offen\nDie Wartungsarbeiten sind beendet und die Server wieder geöffnet!\n<@&{ROLE_ID}>")
                last_sent_time = current_time  # Zeit des letzten Sendens speichern
        
        # Prüfen, ob das Triggerwort für "closed" enthalten ist
        elif any(trigger in message.content for trigger in TRIGGER_WORDS_CLOSED):
            print(f"Triggerwort für 'closed' gefunden!")
            target_channel = client.get_channel(int(TARGET_CHANNEL_ID))
            if target_channel:
                print(f"Nachricht wird in den Ziel-Kanal {target_channel.name} gesendet.")
                await target_channel.send(
                    f"# :warning: Server sind derzeit geschlossen\n"
                    f"Aktuell sind die Server wegen Wartungsarbeiten geschlossen. Sobald sie wieder offen sind, erfährst du das hier!\n"
                    f"Aktuellen Serverstatus überprüfen: https://www.starstable.com/de/server-status\n"
                    f"<@&{ROLE_ID}>"
                )
                last_sent_time = current_time

        else:
            print(f"Kein relevantes Triggerwort in der Nachricht gefunden.")

client.run(TOKEN)