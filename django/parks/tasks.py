import time

from app import app_search, settings
from elastic_enterprise_search import NotFoundError

from . import models

APP_SEARCH_META_ENGINE_NAME = "national-parks-django-meta"
APP_SEARCH_SOURCE_ENGINE_PREFIX = "national-parks-django-source-"


def periodic_index_task():
    # If this task is run periodically, then App Search
    # will be kept up-to-date with the latest data for search.
    # The infrastructure for running this task via celery,
    # APScheduler, or cron is left as an exercise for the reader.

    # Create a new source engine
    source_engine_name = APP_SEARCH_SOURCE_ENGINE_PREFIX + str(int(time.time()))
    app_search.client.create_engine(engine_name=source_engine_name)
    app_search.client.put_schema(
        engine_name=source_engine_name, schema=settings.APP_SEARCH_ENGINE_SCHEMA
    )

    # Get a list of current source engines to delete later
    try:
        current_source_engines = app_search.client.get_engine(
            engine_name=APP_SEARCH_META_ENGINE_NAME
        )["source_engines"]
    except NotFoundError:
        current_source_engines = []

    # Query all the models in the DB!
    documents = []
    for park in models.Park.objects.all():
        documents.append(park.to_app_search())

        # App Search has a limit of 100 documents (<10MB per request)
        # so we ensure that don't hit that limit.
        if len(documents) >= 50:
            app_search.client.index_documents(
                engine_name=source_engine_name, documents=documents
            )
            documents = []

    # Try creating the meta engine if it doesn't exist
    # already with the new source engine.
    resp = app_search.client.create_engine(
        engine_name=APP_SEARCH_META_ENGINE_NAME,
        type="meta",
        source_engines=[source_engine_name],
        ignore_status=400,
    )

    # If the engine wasn't created we add the engine source
    if resp.status != 200:
        # Add the new source engine
        app_search.client.add_meta_engine_source(
            engine_name=APP_SEARCH_META_ENGINE_NAME, source_engines=[source_engine_name]
        )

    # Delete all previous source engines
    if current_source_engines:
        app_search.client.delete_meta_engine_source(
            engine_name=APP_SEARCH_META_ENGINE_NAME,
            source_engines=current_source_engines,
        )
        for engine_name in current_source_engines:
            app_search.client.delete_engine(
                engine_name=engine_name, ignore_status=404
            )
