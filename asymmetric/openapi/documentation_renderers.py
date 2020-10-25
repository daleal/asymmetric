"""
A module for the interactive documentation renderers.
"""

from asymmetric.constants import OPENAPI_SPEC_ROUTE


def get_redoc_html(title: str) -> str:
    """Gets the HTML template for rendering the ReDoc interactive documentation."""
    redoc_script = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    google_fonts = (
        "https://fonts.googleapis.com/css?family=Montserrat:300,400,700|"
        "Roboto:300,400,700"
    )

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>{title}</title>
            <!-- needed for adaptive design -->
            <meta charset="utf-8"/>
            <meta
                name="viewport"
                content="width=device-width, initial-scale=1"
            >
            <link href="{google_fonts}" rel="stylesheet">
            <style>
            body {{
                margin: 0;
                padding: 0;
            }}
            </style>
        </head>
            <body>
            <redoc spec-url="{OPENAPI_SPEC_ROUTE}">
            </redoc>
            <script src="{redoc_script}"></script>
        </body>
    </html>
    """
    return html


def get_swagger_html(title: str) -> str:
    """Gets the HTML template for rendering the Swagger interactive documentation."""
    swagger_js_url = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.30.0/swagger-ui-bundle.js"
    )
    swagger_css_url = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.30.0/swagger-ui.css"
    )

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
            <title>{title}</title>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="{swagger_js_url}"></script>
            <!-- `SwaggerUIBundle` is now available on the page -->
            <script>
                const ui = SwaggerUIBundle({{
                    url: '{OPENAPI_SPEC_ROUTE}',
                    dom_id: '#swagger-ui',
                    presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    layout: "BaseLayout",
                    deepLinking: true,
                    showExtensions: true,
                    showCommonExtensions: true
                }})
            </script>
        </body>
    </html>
    """
    return html
