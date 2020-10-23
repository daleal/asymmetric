from asymmetric.callbacks.utils import valid_callback_data


class TestValidCallbackData:
    def setup_method(self):
        self.data_superset = {
            "callback_url_header": "https://github.com/daleal/asymmetric",
            "callback_method_header": "POST",
            "custom_callback_key_header": "data",
            "custom_extra_header": "not_acceptable"
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
