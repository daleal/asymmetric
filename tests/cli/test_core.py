from argparse import ArgumentParser

from asymmetric.cli.core import generate_parser


class TestGenerateParser:
    def test_generate_parser_creates_parser(self):
        parser = generate_parser()
        assert isinstance(parser, ArgumentParser)
