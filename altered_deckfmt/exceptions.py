

class AlteredDeckFMT(Exception):
    pass


class EncodeError(AlteredDeckFMT):
    pass


class DecodeError(AlteredDeckFMT):
    pass