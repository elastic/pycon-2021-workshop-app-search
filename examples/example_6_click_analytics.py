# Ensures we can import from the 'examples' directory
import json
import sys
from pathlib import Path

examples_dir = Path(__file__).absolute().parent
sys.path.append(str(examples_dir))

from example_1_making_requests import app_search
from example_2_first_engine_and_documents import APP_SEARCH_ENGINE_NAME

print(">>> Submit a search and save the request ID")
query_text = "waterfall"
resp = app_search.search(engine_name=APP_SEARCH_ENGINE_NAME, body={"query": query_text})
print(json.dumps(resp, indent=2))

# Save the 'request_id' for later
request_id = resp["meta"]["request_id"]
print(f"request_id: {request_id}")


print(">>> Simulate a click on the top document")
clicked_document_id = resp["results"][0]["id"]["raw"]
print(f"document_id: {clicked_document_id}")

app_search.log_clickthrough(
    query_text=query_text,
    engine_name=APP_SEARCH_ENGINE_NAME,
    document_id=clicked_document_id,
    request_id=request_id,
    tags=["example-click"],
)

# Check out App Search Analytics for the tag 'example-click'
