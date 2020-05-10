from discord.ext import commands
from discord.errors import LoginFailure
import json

import argparse
from pyfirmata import Arduino, util
from time import sleep


# Sets up Firmata communication with the board
port = "COM3"
board = Arduino(port)
# The iterator reads from the board
iterator = util.Iterator(board)
iterator.start()
pin13 = 'd:13:o'
digital_out = board.get_pin(pin13)
# The program doesn't initalize right away. This is a dirty way to give it time to think
sleep(2)


# Grabs credentials from JSON.
try:
    with open("secrets.json", "r") as f:
        secrets = json.load(f)
        token = secrets["token"]  # Unicode characters
except FileNotFoundError:
    print(
        '"secrets.json" not found.\n',
        "Contributors are granted access to API keys. Otherwise add your own token using --token",
    )


client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print(f"Logged in as {client}")


@client.command()
async def light_up(context):
    """
    Repeats the text send after the command

        >>> !echo I am in a good mood
        I am in a good mood
    """

    await context.send("Let there be light!")
    digital_out.write(1)
    sleep(5)
    digital_out.write(0)



def main():
    parser = argparse.ArgumentParser(
        description="Pittsburgh's Smash Brothers Discord bot"
    )
    parser.add_argument(
        "--token",
        default=token,
        help="The bot's token. You can find it at https://discord.com/developers/applications/< CLIENT ID GOES HERE>/bot. Note this is NOT the same thing as the client secret.",
    )
    args = parser.parse_args()
    # Turns on the bot.
    client.run(args.token)


main()
