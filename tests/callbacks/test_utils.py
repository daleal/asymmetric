import pytest

from asymmetric.callbacks.callback_object import CALLBACK_OBJECT_DEFAULTS
from asymmetric.callbacks.utils import (
    get_header_finders,
    valid_callback_data,
    validate_callback_data,
)
from asymmetric.errors import InvalidCallbackObjectError


class TestValidCallbackData:
    def setup_method(self):
        self.data_superset = {
            "callback_url_header": "https://github.com/daleal/asymmetric",
            "callback_method_header": "POST",
            "custom_callback_key_header": "data",
            "custom_extra_header": "not_acceptable",
        }
        self.data = {
            "callback_url_header": "https://github.com/daleal/asymmetric",
            "callback_method_header": "POST",
            "custom_callback_key_header": "data",
        }
        self.required_data = {}
        self.invalid_types = {
            "callback_url_header": "https://github.com/daleal/asymmetric",
            "callback_method_header": "POST",
            "custom_callback_key_header": None,
        }

    def test_boolean_callback(self):
        assert valid_callback_data(True) is True
        assert valid_callback_data(False) is True

    def test_valid_callback_data_superset(self):
        assert valid_callback_data(self.data_superset) is False

    def test_valid_callback_data(self):
        assert valid_callback_data(self.data) is True

    def test_valid_callback_required_data(self):
        assert valid_callback_data(self.required_data) is True

    def test_valid_callback_invalid_types(self):
        assert valid_callback_data(self.invalid_types) is False


class TestValidateCallbackData:
    def setup_method(self):
        self.data_superset = {
            "callback_url_header": "https://github.com/daleal/asymmetric",
            "callback_method_header": "POST",
            "custom_callback_key_header": "data",
            "custom_extra_header": "not_acceptable",
        }
        self.data = {
            "callback_url_header": "https://github.com/daleal/asymmetric",
            "callback_method_header": "POST",
            "custom_callback_key_header": "data",
        }
        self.required_data = {}
        self.invalid_types = {
            "callback_url_header": "https://github.com/daleal/asymmetric",
            "callback_method_header": "POST",
            "custom_callback_key_header": None,
        }

    def test_boolean_callback_validation(self):
        validate_callback_data(True)
        validate_callback_data(False)

    def test_valid_callback_data_superset_validation(self):
        with pytest.raises(InvalidCallbackObjectError):
            validate_callback_data(self.data_superset)

    def test_valid_callback_data_validation(self):
        validate_callback_data(self.data)

    def test_valid_callback_required_data_validation(self):
        validate_callback_data(self.required_data)

    def test_valid_callback_invalid_types_validation(self):
        with pytest.raises(InvalidCallbackObjectError):
            validate_callback_data(self.invalid_types)


class TestGetHeaderFinders:
    def setup_method(self):
        self.empty_callback = {}
        self.subset_callback = {"callback_url_header": "test_callback_url"}
        self.complete_callback = {
            "callback_url_header": "test_callback_url",
            "callback_method_header": "test_callback_method",
            "custom_callback_key_header": "test_custom_callback_key",
        }
        self.superset_callback = {
            "callback_url_header": "test_callback_url",
            "callback_method_header": "test_callback_method",
            "custom_callback_key_header": "test_custom_callback_key",
            "custom_callback_extra_header": "test_custom_callback_extra",
        }
        self.subset_with_extras_callback = {
            "callback_url_header": "test_callback_url",
            "callback_method_header": "test_callback_method",
            "custom_callback_extra_header": "test_custom_callback_extra",
        }

    def test_booleans_header_finders(self):
        true_headers = get_header_finders(True)
        false_headers = get_header_finders(False)
        assert true_headers == CALLBACK_OBJECT_DEFAULTS
        assert false_headers == CALLBACK_OBJECT_DEFAULTS

    def test_empty_callback_header_finders(self):
        headers = get_header_finders(self.empty_callback)
        assert headers == CALLBACK_OBJECT_DEFAULTS

    def test_subset_callback_header_finders(self):
        headers = get_header_finders(self.subset_callback)
        assert headers == {
            "callback_url_header": "test_callback_url",
            "callback_method_header": "Asymmetric-Callback-Method",
            "custom_callback_key_header": "Asymmetric-Custom-Callback-Key",
        }

    def test_complete_callback_header_finders(self):
        headers = get_header_finders(self.complete_callback)
        assert headers == {
            "callback_url_header": "test_callback_url",
            "callback_method_header": "test_callback_method",
            "custom_callback_key_header": "test_custom_callback_key",
        }

    def test_superset_callback_header_finders(self):
        headers = get_header_finders(self.superset_callback)
        assert headers == {
            "callback_url_header": "test_callback_url",
            "callback_method_header": "test_callback_method",
            "custom_callback_key_header": "test_custom_callback_key",
        }

    def test_subset_with_extras_callback_header_finders(self):
        headers = get_header_finders(self.subset_with_extras_callback)
        assert headers == {
            "callback_url_header": "test_callback_url",
            "callback_method_header": "test_callback_method",
            "custom_callback_key_header": "Asymmetric-Custom-Callback-Key",
        }
