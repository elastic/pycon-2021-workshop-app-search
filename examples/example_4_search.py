# Ensures we can import from the 'examples' directory
import sys
from pathlib import Path

examples_dir = Path(__file__).absolute().parent
sys.path.append(str(examples_dir))

from example_1_making_requests import app_search
from example_2_first_engine_and_documents import APP_SEARCH_ENGINE_NAME

# See what the current schema for the engine looks like. Every field is 'text'!
print(">>> Search for 'mountains'")
resp = app_search.search(
    engine_name=APP_SEARCH_ENGINE_NAME,
    body={
        "query": "mountain",
    },
)

# Let's look at the meta, results, and scores
print(resp["meta"])
for result in resp["results"]:
    print(result["title"]["raw"], result["_meta"]["score"])


# We can also order results by fields
print(">>> Sort by area")
resp = app_search.search(
    engine_name=APP_SEARCH_ENGINE_NAME, body={"query": "", "sort": {"area": "desc"}}
)
for result in resp["results"]:
    print(result["id"]["raw"], result["area"]["raw"])


print(">>> Filter a query, specifically a geo distance filter")
resp = app_search.search(
    engine_name=APP_SEARCH_ENGINE_NAME,
    body={
        "query": "mountain",
        "filters": {
            "location": {"center": "37.085, -120.88", "distance": 1000, "unit": "km"}
        },
    },
)
for result in resp["results"]:
    print(
        f"{result['title']['raw']} ({result['location']['raw']}) {', '.join(result['states']['raw'])}"
    )


print(">>> Aggregate results by value facets")
resp = app_search.search(
    engine_name=APP_SEARCH_ENGINE_NAME,
    body={
        "query": "",
        "facets": {
            "states": [
                {
                    "type": "value",
                    "name": "top_five_states",
                    "sort": {"count": "desc"},
                    "size": 5,
                }
            ]
        },
    },
)
for bucket in resp["facets"]["states"][0]["data"]:
    print(f"{bucket['value']} ({bucket['count']})")


print(">>> Aggregate results by range facets")
resp = app_search.search(
    engine_name=APP_SEARCH_ENGINE_NAME,
    body={
        "query": "",
        "facets": {
            "visitors": [
                {
                    "type": "range",
                    "name": "visitor_amounts",
                    "ranges": [
                        {"to": 50000},
                        {"from": 50000, "to": 500000},
                        {"from": 500000, "to": 1000000},
                        {"from": 1000000},
                    ],
                }
            ]
        },
    },
)
for bucket in resp["facets"]["visitors"][0]["data"]:
    print(f"{bucket.get('from', 0)}-{bucket.get('to', '∞')} ({bucket['count']})")
