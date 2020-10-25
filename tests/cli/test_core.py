import pytest
from argparse import ArgumentParser

import asymmetric
from asymmetric.cli.core import (
    dispatcher,
    generate_documentation_subparser,
    generate_parser,
)


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


class TestDispatcher:
    def test_help_flag(self, capsys):
        with pytest.raises(SystemExit):
            dispatcher(["--help"])
        captured = capsys.readouterr().out
        assert "Command line interface tool for asymmetric." in captured

    def test_version_flag(self, capsys):
        with pytest.raises(SystemExit):
            dispatcher(["--version"])
        captured = capsys.readouterr().out
        assert asymmetric.__version__ in captured

    def test_docs_generation(self, tmpdir):
        output_file = tmpdir.join('openapi.json')
        dispatcher(["docs", "--filename", output_file.strpath, "asymmetric"])
        content = output_file.read()
        print(content)
        assert True

    def test_invalid_cli_call(self, capsys):
        with pytest.raises(SystemExit):
            dispatcher([])
        captured = capsys.readouterr().out
        assert "argument is required" in captured
