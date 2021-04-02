from elastic_enterprise_search import AppSearch

from . import settings

client = AppSearch(settings.APP_SEARCH_URL, http_auth=settings.APP_SEARCH_PRIVATE_KEY)

# Ensure the engine is created and has the proper schema
client.create_engine(engine_name=settings.APP_SEARCH_ENGINE_NAME, ignore_status=400)
client.put_schema(
    engine_name=settings.APP_SEARCH_ENGINE_NAME,
    schema=settings.APP_SEARCH_ENGINE_SCHEMA,
)
