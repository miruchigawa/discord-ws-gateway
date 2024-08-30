"""
Simple discord gateway client
Reference: https://discord.com/developers/docs/topics/gateway
"""

import os
import requests
from client import Client

client = Client(os.getenv("DISCORD_TOKEN"))


@client.on
async def on_ready() -> None:
    print(f"Client connected as {client.user.username}")


@client.on
async def on_interaction_create(packet: dict) -> None:
    token = packet["d"].get("token", "")
    id = packet["d"].get("id", "")

    data = {"type": 4, "data": {"content": "Nyaho."}}

    requests.post(
        f"https://discord.com/api/v10/interactions/{id}/{token}/callback", json=data
    )


client.start()
