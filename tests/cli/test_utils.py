from types import ModuleType

import pytest

from asymmetric.cli.utils import (
    document_openapi,
    get_asymmetric_object,
    get_main_module,
)
from asymmetric.core import _Asymmetric
from asymmetric.errors import AppImportError


class TestGetMainModule:
    def test_get_existing_module(self):
        module = get_main_module("asymmetric.core")
        assert isinstance(module, ModuleType)

    def test_get_incorrect_module_extension(self):
        with pytest.raises(ImportError):
            get_main_module("asymmetric/core.py")

    def test_get_incorrect_module_path(self):
        with pytest.raises(ImportError):
            get_main_module("asymmetric/core/bugs")

    def test_get_incorrect_module(self):
        with pytest.raises(ModuleNotFoundError):
            get_main_module("asymmetric.core.bugs")


class TestGetAsymmetricObject:
    def test_correct_extraction(self):
        asymmetric_object = get_asymmetric_object("asymmetric")
        assert isinstance(asymmetric_object, _Asymmetric)

    def test_incorrect_extraction(self):
        with pytest.raises(AppImportError):
            get_asymmetric_object("asymmetric.core")


class TestDocumentOpenAPI:
    def test_file_output(self, tmpdir):
        output_file = tmpdir.join('openapi.json')
        document_openapi("asymmetric", output_file.strpath)
        content = output_file.read()
        assert "openapi" in content
        assert "paths" in content
        assert "Asymmetric" in content
