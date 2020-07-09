"""
*  ____           _
* |  _ \ ___   __| |_ __ _   _ _ __ ___
* | |_) / _ \ / _` | '__| | | | '_ ` _ \
* |  __/ (_) | (_| | |  | |_| | | | | | |
* |_|   \___/ \__,_|_|   \__,_|_| |_| |_|
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Lesser General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
"""

from podrum.network.protocol.types.PlayerPermissions import PlayerPermissions
from podrum.network.protocol.DataPacket import DataPacket
from podrum.network.protocol.ProtocolInfo import ProtocolInfo

class AdventureSettingsPacket(DataPacket):
    NID = ProtocolInfo.ADVENTURE_SETTINGS_PACKET

    PERMISSION_NORMAL = 0
    PERMISSION_OPERATOR = 1
    PERMISSION_HOST = 2
    PERMISSION_AUTOMATION = 3
    PERMISSION_ADMIN = 4

    BITFLAG_SECOND_SET = 1 << 16

    WORLD_IMMUTABLE = 0x01
    NO_PVP = 0x02

    AUTO_JUMP = 0x20
    ALLOW_FLIGHT = 0x40
    NO_CLIP = 0x80
    WORLD_BUILDER = 0x100
    FLYING = 0x200
    MUTED = 0x400

    BUILD_AND_MINE = 0x01 | self.BITFLAG_SECOND_SET
    DOORS_AND_SWITCHES = 0x02 | self.BITFLAG_SECOND_SET
    OPEN_CONTAINERS = 0x04 | self.BITFLAG_SECOND_SET
    ATTACK_PLAYERS = 0x08 | self.BITFLAG_SECOND_SET
    ATTACK_MOBS = 0x10 | self.BITFLAG_SECOND_SET
    OPERATOR = 0x20 | self.BITFLAG_SECOND_SET
    TELEPORT = 0x80 | self.BITFLAG_SECOND_SET

    flags = 0
    commandPermission = self.PERMISSION_NORMAL
    flags2 = -1
    playerPermission = PlayerPermissions.MEMBER
    customFlags = 0
    entityUniqueId = None

    def decodePayload(self):
        self.flags = self.putUnsignedVarInt()
        self.commandPermission = self.putUnsignedVarInt()
        self.flags2 = self.putUnsignedVarInt()
        self.playerPermission = self.putUnsignedVarInt()
        self.customFlags = self.putUnsignedVarInt()
        self.entityUniqueId = self.getLLong()

    def encodePayload(self):
        self.putUnsignedVarInt(self.flags)
        self.putUnsignedVarInt(self.commandPermission)
        self.putUnsignedVarInt(self.flags2)
        self.putUnsignedVarInt(self.playerPermission)
        self.putUnsignedVarInt(self.customFlags)
        self.putLLong(self.entityUniqueId)

    def getFlag(self, flag):
        if (flag & self.BITFLAG_SECOND_SET) != 0:
            return (self.flags2 & flag) != 0

        return (self.flags & flag) != 0

    def setFlag(self, flag, value):
        if (flag & self.BITFLAG_SECOND_SET) != 0:
            flagSet = self.flags2
        else:
            flagSet = self.flag

        if value:
            flagSet |= flag
        else:
            flagSet &= ~flag
