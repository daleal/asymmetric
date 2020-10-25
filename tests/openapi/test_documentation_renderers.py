from asymmetric.openapi.documentation_renderers import get_redoc_html, get_swagger_html


class TestGetReDocHTML:
    def test_html_renders_correctly(self):
        html = get_redoc_html("Test title!")
        assert "<!DOCTYPE html>" in html
        assert "Test title!" in html


class TestGetSwaggerHTML:
    def test_html_renders_correctly(self):
        html = get_swagger_html("Test title!")
        assert "<!DOCTYPE html>" in html
        assert "Test title!" in html
