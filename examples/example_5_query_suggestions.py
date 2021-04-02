# Ensures we can import from the 'examples' directory
import json
import sys
from pathlib import Path

examples_dir = Path(__file__).absolute().parent
sys.path.append(str(examples_dir))

from example_1_making_requests import app_search
from example_2_first_engine_and_documents import APP_SEARCH_ENGINE_NAME

print(">>> If a user types 'bis' what should type-ahead give?")
resp = app_search.query_suggestion(engine_name=APP_SEARCH_ENGINE_NAME, query="bis")

print("Suggested queries:")
for document in resp["results"]["documents"]:
    print(document["suggestion"])


print(">>> Use the top suggestion, see what high score results come back")
resp = app_search.search(engine_name=APP_SEARCH_ENGINE_NAME, body={"query": "biscayne"})
print(json.dumps(resp, indent=2))


print(
    ">>> Notice how the results from search API are different from query suggestion API"
)
resp = app_search.search(engine_name=APP_SEARCH_ENGINE_NAME, body={"query": "bis"})
for document in resp["results"]:
    print(document["id"]["raw"])
