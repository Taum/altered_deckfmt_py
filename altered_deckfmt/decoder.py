import logging

from .exceptions import DecodeError
from .models import CardSet, DeckFMT, Faction, Rarity
from .utils import base64_to_string, decode_chunk

logger = logging.getLogger(__name__)


def decode(string: str) -> str:
    string = base64_to_string(string.strip())
    result = []

    _, group_count = decode_header(string)

    index = DeckFMT.SET_GROUP_START_INDEX

    for _ in range(group_count):
        index, set_code, card_count = decode_set_group(string, index)

        for _ in range(card_count):
            index, quantity = decode_card_ref_quantity(string, index)
            index, faction, number, rarity, unique_id = decode_card(string, index)
            reference = build_card_referece(set_code, faction, number, rarity, unique_id)

            logger.debug(f"Parsed {quantity} units of '{reference}'")

            result.append(f"{quantity} {reference}")

    result = "\n".join(result)
    return result


def decode_header(string: str) -> tuple[int, int]:
    # 4 bits for the version
    version = decode_chunk(string, 0, DeckFMT.VERSION_BITS)
    if version != 1:
        raise DecodeError(f"Unknown version: {version}")
    logger.debug(f"Detected version {version} of DeckFMT")

    # 8 bits for the group count
    group_count = decode_chunk(string, DeckFMT.VERSION_BITS, DeckFMT.GROUPS_COUNT_BITS)
    if group_count == 0:
        raise DecodeError(f"Invalid number of groups: {group_count}")
    logger.debug(f"Found {group_count} set groups")
    
    return version, group_count


def decode_set_group(string: str, index: int) -> tuple[int, str, int]:
    set_num = decode_chunk(string, index, DeckFMT.SET_COUNT_BITS)
    set_code = CardSet(set_num).name
    index += DeckFMT.SET_COUNT_BITS

    card_count = decode_chunk(string, index, DeckFMT.REFS_COUNT_BITS)
    index += DeckFMT.REFS_COUNT_BITS

    logger.debug(f"Encountered {card_count} cards of set '{set_code}'")

    return index, set_code, card_count

def decode_card_ref_quantity(string: str, index: int) -> tuple[int, int]:
    quantity = decode_chunk(string, index, DeckFMT.CARD_QUANTITY_BITS)
    index += DeckFMT.CARD_QUANTITY_BITS

    if quantity == 0:
        extended_quantity = decode_chunk(string, index, DeckFMT.CARD_EXTENDED_QUANTITY_BITS)
        quantity = extended_quantity + 3
        index += DeckFMT.CARD_EXTENDED_QUANTITY_BITS
    
    return index, quantity

def decode_card(string: str, index: int) -> tuple[int, str, int, str, int]:
    faction_num = decode_chunk(string, index, DeckFMT.CARD_FACTION_BITS)
    faction_code = Faction(faction_num).name
    index += DeckFMT.CARD_FACTION_BITS

    number_in_faction = decode_chunk(string, index, DeckFMT.CARD_NUMBER_BITS)
    index += DeckFMT.CARD_NUMBER_BITS

    rarity_num = decode_chunk(string, index, DeckFMT.CARD_RARITY_BITS)
    rarity_code = Rarity(rarity_num).name
    index += DeckFMT.CARD_RARITY_BITS

    if rarity_code == "U":
        unique_id = decode_chunk(string, index, DeckFMT.CARD_UNIQUE_ID_BITS)
        index += DeckFMT.CARD_UNIQUE_ID_BITS
    else:
        unique_id = None

    return index, faction_code, number_in_faction, rarity_code, unique_id


def build_card_referece(card_set: str, faction: str, number: int, rarity: str, unique_id: int) -> str:
    if faction != "NE":
        return f"ALT_{card_set}_B_{faction}_{number:02d}_{rarity}" + (f"_{unique_id}" if unique_id else "")
    else:
        # For some reason the Mana Token has its number with a single digit instead of 2
        return f"ALT_{card_set}_B_{faction}_{number}_{rarity}"
