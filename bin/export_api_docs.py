"""
Script to export the ReDoc documentation page into a standalone HTML file.
Kudos to https://github.com/Redocly/redoc/issues/726
"""

import json
from pathlib import Path

from cqi.app.main import app

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>My Project - ReDoc</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <style>
        body {
            margin: 0;
            padding: 0;
        }
    </style>
    <style data-styled="" data-styled-version="4.4.1"></style>
</head>
<body>
    <div id="redoc-container"></div>
    <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"> </script>
    <script>
        var spec = %s;
        Redoc.init(spec, {}, document.getElementById("redoc-container"));
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    APP_ROOT_DIR = Path(__file__).parent.parent.resolve()
    TARGET_PATH = APP_ROOT_DIR.joinpath("api_docs.html")
    with open(TARGET_PATH, "w", encoding="utf-8") as fd:
        print(HTML_TEMPLATE % json.dumps(app.openapi()), file=fd)
