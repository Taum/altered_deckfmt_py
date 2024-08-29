from enum import Enum, EnumMeta

from .exceptions import DecodeError, EncodeError


class FMTEnumMeta(EnumMeta):
    def __getitem__(cls, name: str):
        try:
            return super().__getitem__(name)
        except KeyError:
            raise EncodeError(f"Code '{name}' could not be converted to {cls.__name__}")
        

class FMTEnum(Enum, metaclass=FMTEnumMeta):
    @classmethod
    def _missing_(cls, value):
        raise DecodeError(f"Value '{value}' could not be converted to {cls.__name__}")


class CardSet(FMTEnum):
    COREKS = 1
    CORE = 2


class Faction(FMTEnum):
    AX = 1
    BR = 2
    LY = 3
    MU = 4
    OR = 5
    YZ = 6
    NE = 7


class Rarity(FMTEnum):
    C = 0
    R1 = 1
    R2 = 2
    U = 3


class DeckFMT:
    VERSION_BITS = 4
    GROUPS_COUNT_BITS = 8
    SET_COUNT_BITS = 8
    REFS_COUNT_BITS = 6
    CARD_QUANTITY_BITS = 2
    CARD_EXTENDED_QUANTITY_BITS = 6
    CARD_FACTION_BITS = 3
    CARD_NUMBER_BITS = 5
    CARD_RARITY_BITS = 2
    CARD_UNIQUE_ID_BITS = 16

    SET_GROUP_START_INDEX = VERSION_BITS + GROUPS_COUNT_BITS