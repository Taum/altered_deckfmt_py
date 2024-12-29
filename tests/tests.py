import unittest

from altered_deckfmt import decode, encode


class TestDeckFMT(unittest.TestCase):
    def setUp(self) -> None:
        self.decklist_files = [
            (
                "list_1offs.txt",
                "ECAU2RjKFlBScpaUlWVLJFkwysZc0wLFzMh2NTYZw0-GfIEXS4ZWtOmYNMRmyzgp6N-mcjOU",
            ),
            ("list_2sets.txt", "ECAjGhnSHpR0s6gdRaqPWRrRVp64deQESnV0UqcdPA"),
            (
                "list_uniques.txt",
                "EBAVnBjhHww4lcSeILFNjDx5S-so2TPLDRcOHGX4iUOcWt1XazI5t8wW8g",
            ),
            ("list_yzmir.txt", "EBAk3hnUK4h8daVOIvjFyx5h846zfTGuXmb6p9YuwPaHsgA"),
            ("test_extd_qty.txt", "EBAgTTMo"),
            ("test_long_uniq.txt", "EBARGz4JpNnycPbPmBy2f__8"),
            ("test_mana_orb.txt", "EBAg3hHfC8IA"),
            ("collection.txt", "EMAv-QgFIhkZyQZI0kmSYxnclGSzJhkzSaApOMnWTzKABlIylZTUqOVlLBliAy0ZastgGXDLll0y7HSml5S-ZgswmYYyr0xKZFMkBmYzNZnU0GaLNKmpTYpss2ubjN2nAzhpxAM5Gc3OhnUAzsZ2s7qeDPLnoBf8-GfIDQRoQ0MqIVEWiQFRRoq0W6MNGgGjjR2pBUhaSNJgKlDSlpY0taXiR8A0wqaAVOOnLTzp71Aqg1RKorUYBqRVJqmNTWpzVBqi1SqqVWKrLVsKZ-rjV7rB1iAqyVaKtQDWxrc1wAq6ANeGvIJYRsR2MAv-yDZLso2VbLANmKzNZps2MMoDZxs8BWgbQ1ogO0jaXtQBWsrWgdsG2PbRtsBW4bdVvG3rb8CD234GZAdwAK4lcUCuQ3JblVzO5wDdCuiA3UbrV2G7Vdxu93gbwt4gO8leXvRXpAb2N7e-ADfRvrX278N-QLAnghwYBf2EHCIJhQBww4Z8OAOILELiLxI4lcTeKHFLioDxY4tA8YOMQLGjjVxsCY4ccgmPHHrj8J7AHIFkFyI5HGg2yRZJslOTPJwDlByi5SAsqWVvLFlmy45d8wWYXMQJmSzL5oc0gWbLNvm4BzhZxAc6WdbOwDnhzy56Av7QlogB0ZaQdI2kgLSjpUC0w6ZdNAenHTtqB1CA6kdTeqHVXqx1b6uAdYAOtHWoDri1y66BNeWvXYDsF2EA7EdiuxwOnAtkWzLZ3tB2jbStqO1vbDtkD247etwA25Hcrui3TbqAd2O7QXeFvF3l70d6g2-PggF4A8IeGfEHiLxK4o8W-MXHPjtx4C5A8huSPJXk1yh5SBcseXPLxMbAeYAPNLnHzx589AuifSLpP0p6WHUgD0x6c9QuovUnqn1a6w9a-uPYAHsj2V7Ndo-2XcHuN3K7pd1e7XeLvKSMihEWITBgD_SE5EUjKSDJGkoyVpMcnGT1KBlFSkZSspqVDKmlYywZY0tKXFLzmBTEZisxqZDMqmYzNpoM0malNWmwzapuU4GcTORnLTop2M7WeDPFnlz0Z6s9mfFQSoRUMqIVFGi1Rhoy0aqONHgH_pBUkqUNLGltTBpo01abVOKnjT6qA1BaiNRqpDUxqa1OqoNUaqjVVqtVYquNXqsDWFrI1oq0taqtjW5rg1xq6VeGvNYSsQ2MrIVlGyrZasx2cbOtnq0DaKtI2orWVsG2NbKto22rcAP_bxt63AbhNxG4rccNEG5DcmuY3QbphJ73UbrV2K7Vdxu9Xgbw15G83ehvS3sr218G-LfKvo31b7N-LAlgiwZYQcIuEnCYCcWFHC4PAuGHDLhsMOLDjiBxDYksUOKrFji1xc4vEChxg4xcZWNLHFjxx9ZAAf3IPkRyNZIckuSvJjk1ydZQcpWVHKzlhyzZccu-YHMVmRzK5ms0OanNjm7zg50c62eHPNoT0RaMdIOkrSjpZ0w6a9OOnXT1qB1FaktUOrHVrq61h60da2uHXNry2A7CtiOxnY4LOWyHZID-7KtmOzXZ1tB2k7UdrhC3bYtuO3XcDuJ3I7od027HdtvD3o71t8O-bgnwi4Y8QuKPGLjjx149cgeQvJLlDyq5Y8weZPNHmtzi55dAegvQron0h6S9MenXUHqP1R6rdYuuXYHsV2R7LdoASntV2x7a9ue4PcXuj3a7w96A")
        ]

    def test_encode_string(self):
        for file, expected_result in self.decklist_files:
            with self.subTest(file=file):
                decklist = self.read_decklist(file)
                result = encode(decklist)
                self.assertEqual(result, expected_result)

    def test_decode_string(self):
        for file, encoded_decklist in self.decklist_files:
            with self.subTest(file=file):
                result = decode(encoded_decklist)
                decklist = self.read_decklist(file)
                self.assertEqual(result, decklist)

    @staticmethod
    def read_decklist(decklist_file) -> str:

        with open(f"./tests/decklists/{decklist_file}") as f:
            return f.read()


if __name__ == "__main__":
    unittest.main()
