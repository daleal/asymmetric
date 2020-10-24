import json
import logging

import pytest
from starlette.requests import Request

from asymmetric.loggers import log, log_request, log_request_body


class TestLog:
    def setup_method(self):
        self.messages = {
            "debug": "This is a debug message",
            "info": "This is a info message",
            "warning": "This is a warning message",
            "error": "This is a error message",
            "critical": "This is a critical message",
        }

    def test_debug_log(self, caplog):
        self.valid_log_helper(caplog, "debug")

    def test_info_log(self, caplog):
        self.valid_log_helper(caplog, "info")

    def test_warning_log(self, caplog):
        self.valid_log_helper(caplog, "warning")

    def test_error_log(self, caplog):
        self.valid_log_helper(caplog, "error")

    def test_critical_log(self, caplog):
        self.valid_log_helper(caplog, "critical")

    def test_invalid_debug_log(self, caplog):
        self.invalid_log_helper(caplog, "debug")

    def test_invalid_info_log(self, caplog):
        self.invalid_log_helper(caplog, "info")

    def test_invalid_warning_log(self, caplog):
        self.invalid_log_helper(caplog, "warning")

    def test_invalid_error_log(self, caplog):
        self.invalid_log_helper(caplog, "error")

    def valid_log_helper(self, caplog, level):
        text = self.log_helper(caplog, level, level)
        assert "[[asymmetric]]" in text
        assert level in text

    def invalid_log_helper(self, caplog, level):
        text = self.log_helper(caplog, level, "critical")
        assert "[[asymmetric]]" not in text
        assert level not in text

    def log_helper(self, caplog, level, expected_level):
        expected_level = getattr(logging, expected_level.upper())
        with caplog.at_level(expected_level):
            log(self.messages[level], level=level)
        return caplog.text


class TestLogRequest:
    def setup_method(self):
        def sample_function():
            return "Hello, test!"

        async def empty_receive():
            return {"type": "http.request"}

        self.function = sample_function
        self.function_name = "sample_function"
        self.method = "POST"
        self.route = "/v1/test/log/request"
        self.request = Request({"type": "http", "method": self.method}, empty_receive)

    @pytest.mark.asyncio
    async def test_log_request(self, caplog):
        with caplog.at_level(logging.INFO):
            await log_request(self.request, self.route, self.function)
        assert self.method in caplog.text
        assert self.route in caplog.text
        assert self.function_name in caplog.text


class TestLogRequestBody:
    def setup_method(self):
        self.body = {
            "valid": True,
            "name": "Dani",
            "age": 22,
        }

    def test_log_request_body(self, caplog):
        with caplog.at_level(logging.INFO):
            log_request_body(self.body)
        for key in self.body.keys():
            assert str(key) in caplog.text
