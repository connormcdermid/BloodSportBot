import os
import poplib  # default package
import email  # default package
import discord  # package: discord.py
from dotenv import load_dotenv  # package: python-dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

client = discord.Client()


pop_conn = poplib.POP3_SSL("pop.gmail.com")
pop_conn.user(EMAIL_USERNAME)
pop_conn.pass_(EMAIL_PASSWORD)

# Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
# concat message pieces
messages = [b"\n".join(mssg[1] for mssg in messages)]
# parse message into an email object
messages = [email.message_from_bytes(mssg) for mssg in messages]

pop_conn.quit()  # exit the POP connection

@client.event
async def on_ready():
    print("{} has established a connection to Discord".format(client.user))
    print("{} has established a connection to the following channels in the following guilds: ".format(client.user))
    for guild in client.guilds:
        print("{}(id: {})".format(guild.name, guild.id))
        for channel in guild.channels:
            print("{}".format(channel.name))

    announcements_channel = client.get_channel(764200085054947378)

    for message in messages:
        try:
            await channel.send("<@&864510792354758697> A new chapter has been released! Check it out here: {}".format(
                [mssg['subject'] for mssg in messages]
            ))
        except discord.Forbidden:
            print("Failed to send message: incorrect permissions")
            exit(2)
        except discord.HTTPException:
            print("Failed to send message: Client failed to reach Discord")
            exit(1)
        finally:
            print("Message sent.")
            exit(0)


client.run(TOKEN)