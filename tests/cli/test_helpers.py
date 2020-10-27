from argparse import ArgumentParser

from asymmetric.cli.helpers import (
    clear_runner_args,
    setup_documentation_arguments,
    setup_runner_arguments,
)


class TestClearRunnerArgs:
    def setup_method(self):
        self.all_valid = {"x": True, "y": False, "z": "Test!"}
        self.some_valid = {"x": True, "y": None, "z": "Test!"}
        self.none_valid = {"x": None, "y": None, "z": None}

    def test_clear_all_valid_runner_args(self):
        final = clear_runner_args(self.all_valid)
        assert final == self.all_valid

    def test_clear_some_valid_runner_args(self):
        final = clear_runner_args(self.some_valid)
        assert final == {"x": True, "z": "Test!"}

    def test_clear_none_valid_runner_args(self):
        final = clear_runner_args(self.none_valid)
        assert final == {}


class TestSetupDocumentationArguments:
    def setup_method(self):
        self.base_parser = ArgumentParser(description="Test parser.")
        self.subparsers = self.base_parser.add_subparsers(help="Test subparsers.")
        self.parser = self.subparsers.add_parser("docs")
        self.parser.set_defaults(action="run")

    def test_documentation_flags(self):
        setup_documentation_arguments(self.parser)
        args = self.base_parser.parse_args(["docs", "testmodule"])
        assert "module" in args
        assert "filename" in args


class TestSetupRunnerArguments:
    def setup_method(self):
        self.base_parser = ArgumentParser(description="Test parser.")
        self.subparsers = self.base_parser.add_subparsers(help="Test subparsers.")
        self.parser = self.subparsers.add_parser("run")
        self.parser.set_defaults(action="run")

    def test_runner_flags(self):
        setup_runner_arguments(self.parser)
        args = self.base_parser.parse_args(["run", "testmodule"])
        assert "module" in args
        assert "host" in args
        assert "port" in args
        assert "uds" in args
        assert "fd" in args
        assert "reload" in args
        assert "reload_dir" in args
        assert "workers" in args
        assert "loop" in args
        assert "http" in args
        assert "ws" in args
        assert "lifespan" in args
        assert "interface" in args
        assert "env_file" in args
        assert "log_config" in args
        assert "log_level" in args
        assert "access_log" in args
        assert "use_colors" in args
        assert "no_use_colors" in args
        assert "proxy_headers" in args
        assert "no_proxy_headers" in args
        assert "forwarded_allow_ips" in args
        assert "root_path" in args
        assert "limit_concurrency" in args
        assert "backlog" in args
        assert "limit_max_requests" in args
        assert "timeout_keep_alive" in args
        assert "ssl_keyfile" in args
        assert "ssl_certfile" in args
        assert "ssl_keyfile_password" in args
        assert "ssl_version" in args
        assert "ssl_cert_reqs" in args
        assert "ssl_ca_certs" in args
        assert "ssl_ciphers" in args
        assert "header" in args
        assert "app_dir" in args
