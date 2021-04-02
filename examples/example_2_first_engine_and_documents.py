# Ensures we can import from the 'examples' directory
import json
import sys
from pathlib import Path

import yaml

with (Path(__file__).absolute().parent.parent / "config.yml").open() as f:
    CONFIG = yaml.safe_load(f.read())

examples_dir = Path(__file__).absolute().parent
sys.path.append(str(examples_dir))

from example_1_making_requests import CONFIG, app_search

# Go into App Search and find the private API key and
# put that value within 'APP_SEARCH_PRIVATE_KEY'
# (hint: the key should start with 'private-')
APP_SEARCH_PRIVATE_KEY = CONFIG["app_search"]["private_key"]

# This is the engine name we'll be using throughout the examples.
APP_SEARCH_ENGINE_NAME = "national-parks-pycon-2021"

# Set the API key on the client
app_search.http_auth = APP_SEARCH_PRIVATE_KEY


# Only executes when run as a script, not as an import.
if __name__ == "__main__":

    # Create the engine and tolerate 400 for duplicate engine name
    print(">>> Create engine")
    resp = app_search.create_engine(
        engine_name=APP_SEARCH_ENGINE_NAME, language="en", ignore_status=400
    )

    # If there aren't any documents in the engine
    # then we index some documents
    document_count = resp.get("document_count", 1)
    if document_count == 0:
        print(">>> Indexing documents")
        with (examples_dir / "data.json").open() as f:
            documents = json.loads(f.read())

        resp = app_search.index_documents(
            engine_name=APP_SEARCH_ENGINE_NAME, documents=documents
        )
