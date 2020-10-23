import asyncio
import json

import pytest
from starlette.requests import Request

from asymmetric.errors import (
    DuplicatedEndpointError,
    InvalidCallbackHeadersError,
    InvalidCallbackObjectError,
)
from asymmetric.utils import (
    filter_params,
    generic_call,
    get_body,
    handle_error,
    valid_plain_dict,
)


class TestGenericCall:
    def setup_method(self):
        self.artificial_delay = 0.01  # seconds
        self.params = {
            "x": 2,
            "y": 2,
            "z": 3,
        }

    @pytest.mark.asyncio
    async def test_sync_generic_call(self):
        value = await generic_call(self.sync_generic_call, self.params)
        assert value == 10

    @pytest.mark.asyncio
    async def test_async_generic_call(self):
        value = await generic_call(self.async_generic_call, self.params)
        assert value == 10

    def sync_generic_call(self, x, y, z):
        return x * (y + z)

    async def async_generic_call(self, x, y, z):
        await asyncio.sleep(self.artificial_delay)
        return x * (y + z)


class TestHandleError:
    def setup_method(self):
        self.message = "This is a test messsage"

    def test_duplicated_endpoint_error_handling(self):
        duplicated_endpoint_error = DuplicatedEndpointError(self.message)
        response = handle_error(duplicated_endpoint_error)
        assert json.loads(response.body)["message"] == self.message
        assert response.status_code == 500

    def test_incalid_callback_headers_error_handling(self):
        incalid_callback_headers_error = InvalidCallbackHeadersError(self.message)
        response = handle_error(incalid_callback_headers_error)
        assert json.loads(response.body)["message"] == self.message
        assert response.status_code == 500

    def test_invalid_callback_object_error_handling(self):
        invalid_callback_object_error = InvalidCallbackObjectError(self.message)
        response = handle_error(invalid_callback_object_error)
        assert json.loads(response.body)["message"] == self.message
        assert response.status_code == 500


class TestFilterParams:
    def setup_method(self):
        # Functions
        self.function = lambda x, y, z: x + y + z
        self.function_kwargs = lambda x, y, z, **kwargs: x + y + z
        self.function_no_params = lambda: None

        # Params
        self.params_superset = {"a": 1, "b": 2, "c": 3, "d": 4, "x": 5, "y": 6, "z": 7}
        self.params = {"x": 1, "y": 2, "z": 3}
        self.params_subset = {"x": 1, "y": 2}

    def test_params_superset_filter(self):
        """Tests that the params shrink to just the ones of the function."""
        params = filter_params(self.function, self.params_superset)
        assert params == {"x": 5, "y": 6, "z": 7}

    def test_params_filter(self):
        """Tests that params don't change once filtered."""
        params = filter_params(self.function, self.params)
        assert params == self.params

    def test_params_subset_filter(self):
        """Tests that the params shrink to just the ones present on the function."""
        params = filter_params(self.function, self.params_subset)
        assert params == {"x": 1, "y": 2}

    def test_params_superset_kwargs_filter(self):
        """Tests that params don't change once filtered."""
        params = filter_params(self.function_kwargs, self.params_superset)
        assert params == self.params_superset

    def test_params_kwargs_filter(self):
        """Tests that params don't change once filtered."""
        params = filter_params(self.function_kwargs, self.params)
        assert params == self.params

    def test_params_subset_kwargs_filter(self):
        """Tests that params don't change once filtered."""
        params = filter_params(self.function_kwargs, self.params_subset)
        assert params == self.params_subset

    def test_no_params_filter(self):
        """Tests that params are completely filtered."""
        params_superset = filter_params(self.function_no_params, self.params_superset)
        params = filter_params(self.function_no_params, self.params)
        params_subset = filter_params(self.function_no_params, self.params_subset)
        assert params_superset == {}
        assert params == {}
        assert params_subset == {}


class TestGetBody:
    def setup_method(self):
        async def json_receive():
            return {"type": "http.request", "body": b'{"message": "This is a test!"}'}

        async def empty_receive():
            return {"type": "http.request"}

        self.json_request = Request({"type": "http"}, json_receive)
        self.empty_request = Request({"type": "http"}, empty_receive)

    @pytest.mark.asyncio
    async def test_get_body(self):
        body = await get_body(self.json_request)
        assert body == {"message": "This is a test!"}

    @pytest.mark.asyncio
    async def test_get_empty_body(self):
        body = await get_body(self.empty_request)
        assert body == {}


class TestValidPlainDict:
    def setup_method(self):
        self.validator = {
            "asymmetric": {"required": True, "type": bool},
            "name": {"required": False, "type": str},
            "age": {"required": True, "type": int},
        }
        self.data_superset = {
            "asymmetric": True,
            "name": "Dani",
            "age": 22,
            "lang": "Python",
        }
        self.data = {"asymmetric": True, "name": "Dani", "age": 22}
        self.required_data = {"asymmetric": True, "age": 22}
        self.data_subset = {"age": 22}
        self.invalid_types = {"asymmetric": True, "name": "Dani", "age": 22.5}

    def test_with_data_superset(self):
        valid = valid_plain_dict(self.data_superset, self.validator)
        assert valid is False

    def test_with_data(self):
        valid = valid_plain_dict(self.data, self.validator)
        assert valid is True

    def test_with_required_data(self):
        valid = valid_plain_dict(self.required_data, self.validator)
        assert valid is True

    def test_with_data_subset(self):
        valid = valid_plain_dict(self.data_subset, self.validator)
        assert valid is False

    def test_with_invalid_types(self):
        valid = valid_plain_dict(self.invalid_types, self.validator)
        assert valid is False
