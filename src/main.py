"""
Simple discord gateway client
Reference: https://discord.com/developers/docs/topics/gateway
"""

import os

from client import Client
from classes.interaction import Interaction

client = Client(os.getenv("DISCORD_TOKEN"))

@client.on
async def on_ready() -> None:
    print(f"Client connected as {client.user.username}")


@client.on
async def on_interaction_create(interaction: Interaction) -> None:

    if interaction.is_command():
        print(f'[/] {interaction.member.username} -> {interaction.name}')
        await interaction.respond('Nyaho.')        


client.start()
