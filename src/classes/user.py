from typing import Optional


class User:
    def __init__(self, data: dict) -> None:
        self.id: str = data.get('id', '')
        self.username: str = data.get('username', '')
        self.discriminator: str = data.get('discriminator', '')
        self.avatar: Optional[str] = data.get('avatar')
        self.bot: bool = data.get('bot', False)
        self.system: bool = data.get('system', False)
        self.public_flags: int = data.get('public_flags', 0)


    def mention(self) -> str:
        return f"<@{self.id}>"

    
    def get_avatar_url(self) -> str:
        return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png" if self.avatar else f"https://cdn.discordapp.com/embed/avatars/{(int(self.discriminator) % 5)}.png"

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username}#{self.discriminator}>"


class Member(User):
    def __init__(self, data: dict) -> None:
        super().__init__(data.get('user', {}))
        self.nick: Optional[str] = data.get('nick')
        self.roles: list[str] = data.get('roles', [])
        self.joined_at: Optional[str] = data.get('joined_at')
        self.premium_since: Optional[str] = data.get('premium_since')

    def display_name(self) -> str:
        return self.nick if self.nick else self.username

    def __repr__(self) -> str:
        return f"<Member id={self.id} username={self.username}#{self.discriminator} nick={self.nick}>"
