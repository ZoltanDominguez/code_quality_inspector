"""
Script to export the ReDoc documentation page into a standalone HTML file.
Kudos to https://github.com/Redocly/redoc/issues/726
"""
import hashlib
import json
from pathlib import Path

from cqi.app.main import app
from cqi.log import get_logger

logger = get_logger(name=__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
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
    <script 
    src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js" 
    integrity="sha384-7tlX7/pVtXlXa8C4KtSgVzizyFulUwu7ODXGbKCbfmAk7cchPphAH7AYGvJMmh00" 
    crossorigin="anonymous">
    </script>
    <script>
        var spec = %s;
        Redoc.init(spec, {}, document.getElementById("redoc-container"));
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    APP_ROOT_DIR = Path(__file__).parent.parent.resolve()
    TARGET_PATH = APP_ROOT_DIR.joinpath("index.html")

    with open(TARGET_PATH, "rb") as f:
        data = f.read()
        sha256_original = hashlib.sha256(data).hexdigest()

    with open(TARGET_PATH, "w", encoding="utf-8") as fd:
        new_data = HTML_TEMPLATE % json.dumps(app.openapi())
        print(new_data, file=fd)

    with open(TARGET_PATH, "rb") as f:
        new_data = f.read()
        sha256_new = hashlib.sha256(new_data).hexdigest()

    if sha256_new != sha256_original:
        logger.error("API docs is not up to date according to app.openapi()")
    else:
        logger.info("API docs is up to date!")
