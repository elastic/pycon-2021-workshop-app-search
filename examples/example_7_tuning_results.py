# Ensures we can import from the 'examples' directory
import json
import sys
from pathlib import Path

examples_dir = Path(__file__).absolute().parent
sys.path.append(str(examples_dir))

from example_1_making_requests import app_search
from example_2_first_engine_and_documents import APP_SEARCH_ENGINE_NAME

print(">>> See Search Settings for the Engine")
resp = app_search.get_search_settings(engine_name=APP_SEARCH_ENGINE_NAME)
print(json.dumps(resp, indent=2))


print(">>> Update Search Settings with better tuning")
resp = app_search.put_search_settings(
    engine_name=APP_SEARCH_ENGINE_NAME,
    body={
        "search_fields": {
            "title": {"weight": 3},
            "states": {"weight": 2},
            "description": {"weight": 1},
        },
        "boosts": {
            "visitors": [
                {
                    "type": "functional",
                    "factor": 1,
                    "function": "logarithmic",
                    "operation": "multiply",
                }
            ]
        },
    },
)
print(json.dumps(resp, indent=2))


print(">>> Create a Curation for 'biggest park'")
resp = app_search.create_curation(
    engine_name=APP_SEARCH_ENGINE_NAME,
    queries=["biggest park"],
    promoted_doc_ids=["park-wrangell-st-elias"],
    ignore_status=400,
)
print(json.dumps(resp, indent=2))


print(">>> Test out our new Curation")
resp = app_search.search(
    engine_name=APP_SEARCH_ENGINE_NAME, body={"query": "biggest park"}
)

# The top result is 'park-wrangell-st-elias' as expected!
print(json.dumps(resp["results"][0], indent=2))


print(">>> Create a Synonym for 'buffalo' -> 'bison'")
resp = app_search.create_synonym_set(
    engine_name=APP_SEARCH_ENGINE_NAME, body={"synonyms": ["buffalo", "bison"]}
)
print(json.dumps(resp, indent=2))


print(">>> Now search for 'buffalo' and receive results back for 'bison'")
resp = app_search.search(engine_name=APP_SEARCH_ENGINE_NAME, body={"query": "buffalo"})
print(json.dumps(resp, indent=2))

# Result descriptions have 'buffalo' and then 'bison'
for result in resp["results"]:
    print(result["id"]["raw"] + ":", result["description"]["raw"])
