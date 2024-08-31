from enum import Enum, StrEnum


"""
Reference: https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
"""

class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


"""
Reference: https://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-opcodes
"""


class Opcode(Enum):
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11

    @classmethod
    def __missing__(cls: any, value: any) -> None:
        return None


"""
Reference: https://discord.com/developers/docs/topics/gateway-events#receive-events
"""


class EventType(StrEnum):
    READY = "READY"
    GUILD_CREATE = "GUILD_CREATE"
    INTERACTION_CREATE = "INTERACTION_CREATE"

    @classmethod
    def __missing__(cls: any, value: any) -> str:
        return ""
