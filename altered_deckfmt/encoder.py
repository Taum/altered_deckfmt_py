from .exceptions import EncodeError
from .models import CardSet, DeckFMT, Faction, Rarity
from .utils import encode_chunk, parse_decklist, string_to_base64


def encode(string: str, sep: str = "\n") -> str:
    cards = parse_decklist(string, sep)

    result = encode_header(len(cards))

    for card_set, cards in cards.items():
        result += encode_set_group(card_set, len(cards))
        for quantity, card in cards:
            result += encode_card_ref_quantity(quantity)
            result += encode_card(card)

    return string_to_base64(result)


def encode_header(card_sets: int) -> str:
    result = _encode_version(1)

    if card_sets <= 0:
        raise EncodeError(f"Cannot encode '{card_sets}' set groups")

    result += _encode_group_count(card_sets)
    return result


def encode_set_group(card_set: str, card_count: int) -> str:
    result = _encode_set(card_set)

    if card_count <= 0:
        raise EncodeError(f"Cannot encode '{card_count}' cards")

    result += _encode_refs_count(card_count)
    return result


def encode_card_ref_quantity(quantity: int) -> str:
    if quantity > 3:
        return "00" + encode_chunk(quantity - 3, DeckFMT.CARD_EXTENDED_QUANTITY_BITS)
    elif quantity <= 0:
        raise EncodeError(f"Cannot encode '{quantity}' copies of a card")
    else:
        return encode_chunk(quantity, DeckFMT.CARD_QUANTITY_BITS)


def encode_card(reference: str) -> str:
    faction, number, rarity, *extra = reference.split("_")[3:]
    result = encode_chunk(Faction[faction].value, DeckFMT.CARD_FACTION_BITS)
    result += encode_chunk(int(number), DeckFMT.CARD_NUMBER_BITS)
    result += encode_chunk(Rarity[rarity].value, DeckFMT.CARD_RARITY_BITS)
    if rarity == "U":
        result += encode_chunk(int(extra[0]), DeckFMT.CARD_UNIQUE_ID_BITS)

    return result


def _encode_version(version: int) -> str:
    return encode_chunk(version, DeckFMT.VERSION_BITS)


def _encode_group_count(card_count: int) -> str:
    return encode_chunk(card_count, DeckFMT.GROUPS_COUNT_BITS)


def _encode_set(card_set: str) -> str:
    return encode_chunk(CardSet[card_set].value, DeckFMT.SET_COUNT_BITS)


def _encode_refs_count(card_count: int) -> str:
    return encode_chunk(card_count, DeckFMT.REFS_COUNT_BITS)
