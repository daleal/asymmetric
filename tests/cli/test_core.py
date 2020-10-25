from argparse import ArgumentParser

from asymmetric.cli.core import generate_parser, generate_documentation_subparser


class TestGenerateParser:
    def test_generate_parser_creates_parser(self):
        parser = generate_parser()
        assert isinstance(parser, ArgumentParser)


class TestGenerateDocumentationSubparser:
    def test_generate_subparser(self):
        base_parser = ArgumentParser(description="Test parser.")
        subparsers = base_parser.add_subparsers(help="Test subparsers.")
        docs_parser = generate_documentation_subparser(subparsers)
        assert isinstance(docs_parser, ArgumentParser)
