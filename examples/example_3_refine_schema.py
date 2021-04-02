# Ensures we can import from the 'examples' directory
import sys
from pathlib import Path

examples_dir = Path(__file__).absolute().parent
sys.path.append(str(examples_dir))

from example_1_making_requests import app_search
from example_2_first_engine_and_documents import APP_SEARCH_ENGINE_NAME

# See what the current schema for the engine looks like. Every field is 'text'!
print(">>> Current schema")
resp = app_search.get_schema(engine_name=APP_SEARCH_ENGINE_NAME)
print(resp)


# Notice how every field initially is 'text', we want
# to update fields to the proper types.
print(">>> Update to desired schema")
resp = app_search.put_schema(
    engine_name=APP_SEARCH_ENGINE_NAME,
    schema={
        "area": "number",
        "visitors": "number",
        "established": "date",
        "location": "geolocation",
    },
)
print(resp)
