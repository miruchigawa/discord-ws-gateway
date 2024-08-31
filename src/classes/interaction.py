import requests
from typing import Optional

from .user import User, Member
from enums import InteractionType


class Interaction:
    def __init__(self, data: dict) -> None:
        self._id: str = data.get("id", "")
        self._type: InteractionType = InteractionType(data.get("type"))
        self._token: str = data.get("token", "")
        self._data: dict = data.get("data", {})

        self.name: str = self._data.get("name", "")

        self.member: Optional[Member] = (
            Member(data.get("member", {})) if "member" in data else None
        )
        self.user: User = User(data.get("user", {}))

    def is_command(self) -> bool:
        return self._type == InteractionType.APPLICATION_COMMAND

    async def respond(self, content: str) -> None:
        data = {"type": 4, "data": {"content": content}}

        requests.post(
            f"https://discord.com/api/v10/interactions/{self._id}/{self._token}/callback",
            json=data,
        )
