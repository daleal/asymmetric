import logging

from asymmetric.loggers import log


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
        self.log_helper(caplog, "debug")

    def test_info_log(self, caplog):
        self.log_helper(caplog, "info")

    def test_warning_log(self, caplog):
        self.log_helper(caplog, "warning")

    def test_error_log(self, caplog):
        self.log_helper(caplog, "error")

    def test_critical_log(self, caplog):
        self.log_helper(caplog, "critical")

    def log_helper(self, caplog, level):
        with caplog.at_level(logging.DEBUG):
            log(self.messages[level], level=level)
        assert "[[asymmetric]]" in caplog.text
        assert level in caplog.text
