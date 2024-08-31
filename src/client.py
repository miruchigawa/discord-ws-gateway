import os
import json
import asyncio

from websockets import connect
from websockets.client import WebSocketClientProtocol
from typing import Callable, Optional, Dict, Any, Coroutine, Awaitable

from enums import Opcode, EventType

from classes.interaction import Interaction
from classes.user import User

class Client:
    _token: str
    _session_id: str
    _resume_gateway_url: str
    _callback_ev: Dict[str, Callable[..., Coroutine[Any, Any, None]]]

    user: User

    def __init__(self, token: str) -> None:
        self._token = token
        self._session_id = ""
        self._resume_gateway_url = ""
        self._callback_ev = {}
        self.user = User({})

    def on(self, function: Callable[..., Coroutine[Any, Any, None]]):
        """
        Set event callback

        :param function: Callback function
        """

        self._callback_ev[function.__name__] = function
        return function

    async def emit(self, name: str, *args: Any, **kwargs: Any) -> Awaitable[None]:
        """
        Call event callback

        :param name: Name of event callback
        """

        (
            await self._callback_ev[name](*args, **kwargs)
            if name in self._callback_ev
            else None
        )

    async def _send_identify(self, socket: WebSocketClientProtocol) -> Awaitable[None]:
        """
        Send identify information (On first connect)

        :param socket: Socket client
        """

        packet = {
            "op": Opcode.IDENTIFY.value,
            "d": {
                "token": os.getenv("DISCORD_TOKEN"),
                "intents": 513,
                "properties": {
                    "os": "linux",
                    "browser": "chromium",
                    "device": "Linux x86_64",
                },
            },
        }

        await socket.send(json.dumps(packet))

    async def _send_recover_request(
        self, socket: WebSocketClientProtocol
    ) -> Awaitable[None]:
        """
        Send continue request (On disconnect or invalid session)

        :param socket: Socket client
        """

        packet = {
            "op": Opcode.RESUME.value,
            "d": {
                "token": os.getenv("DISCORD_TOKEN"),
                "session_id": self._session_id,
                "resume_gateway_url": self._resume_gateway_url,
            },
        }

        await socket.send(json.dumps(packet))

    async def _send_heartbeat(self, socket: WebSocketClientProtocol) -> Awaitable[None]:
        """
        Send heartbeat

        :param socket: Socket client
        """

        await socket.send(json.dumps({"op": Opcode.HEARTBEAT.value, "d": None}))

    async def _heartbeat_pool(
        self, socket: WebSocketClientProtocol, interval: int
    ) -> Awaitable[None]:
        """
        Start interval heartbeat polling

        :param socket: Socket client
        :param interval: Interval on ms
        """

        while True:
            await self._send_heartbeat(socket)
            await asyncio.sleep(interval / 1000)

    async def _handle_events(
        self, socket: WebSocketClientProtocol, packet: dict
    ) -> Awaitable[None]:
        """
        Handle dispatch events
        """

        match packet.get("t"):
            case EventType.READY:
                self._session_id = packet["d"].get("session_id", "")
                self._resume_gateway_url = packet["d"].get("resume_gateway_url", "")
                self.user = User(packet["d"].get("user", {}))
                await self.emit("on_ready")
            case EventType.GUILD_CREATE:
                pass
            case EventType.INTERACTION_CREATE:
                await self.emit("on_interaction_create", Interaction(packet.get('d', {})))
            case _:
                print(f"Unknown event {packet}")

    async def _listen_connection(
        self, socket: WebSocketClientProtocol
    ) -> Awaitable[None]:
        """
        Handle websocket packet
        """

        async for message in socket:
            packet = json.loads(message)

            match Opcode(packet.get("op")):
                case Opcode.DISPATCH:
                    await self._handle_events(socket, packet)
                case Opcode.HEARTBEAT:
                    await self._send_heartbeat(socket)
                case Opcode.RECONNECT:
                    await self._send_recover_request(socket)
                case Opcode.HELLO:
                    interval = packet["d"].get("heartbeat_interval", 0)
                    asyncio.create_task(self._heartbeat_pool(socket, interval))
                    await self._send_identify(socket)
                case Opcode.HEARTBEAT_ACK:
                    print("Client receiving HEARTBEAT_ACK")
                case _:
                    print(f"Unknown packet {packet}")

    async def _create_connection(self) -> Awaitable[None]:
        """
        Create websocket connection
        """

        async with connect("wss://gateway.discord.gg/?v=10&encoding=json") as socket:
            await self._listen_connection(socket)

    def start(self) -> None:
        """
        Start client
        """

        try:
            asyncio.run(self._create_connection())
        except KeyboardInterrupt:
            pass
