import unittest

from src.generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extracts_title_from_h1(self):
        markdown = "# Mój tytuł\n\nTreść dokumentu"
        self.assertEqual(extract_title(markdown), "Mój tytuł")

    def test_finds_h1_after_other_lines(self):
        markdown = "Wstęp\n\n# Tytuł strony\nTreść"
        self.assertEqual(extract_title(markdown), "Tytuł strony")

    def test_rejects_h2_as_title(self):
        with self.assertRaises(Exception):
            extract_title("## To nie jest H1")

    def test_raises_when_h1_is_missing(self):
        for markdown in ["", "Zwykły tekst", "## Nagłówek drugiego poziomu"]:
            with self.subTest(markdown=markdown):
                with self.assertRaises(Exception):
                    extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
