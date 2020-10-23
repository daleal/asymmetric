import asyncio
import json

import pytest

from asymmetric.errors import (
    DuplicatedEndpointError,
    InvalidCallbackHeadersError,
    InvalidCallbackObjectError,
)
from asymmetric.utils import generic_call, handle_error


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
