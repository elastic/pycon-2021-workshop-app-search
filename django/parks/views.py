import json
import re

from app import app_search, settings

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from . import models, tasks


def index(request):
    return HttpResponse("Hello, world. You're at the parks index.")


def park(request, park_id):
    park = get_object_or_404(models.Park, id=park_id)
    return HttpResponse(
        f"""
    <html><body>
        <h1>{park.title}</h1>
        <p>{park.description}</p>
        <ul>
        <li><a href="{park.url}">Website</a></li>
        <li>Area: {park.area}km2</li>
        <li>Location: {park.latitude}, {park.longitude}</li>
        <li>States: {', '.join(state.name for state in park.states.all())}</li>
        <li>World Heritage Site: {park.world_heritage_site}</li>
        <li>Visitors: {park.visitors}</li>
        </ul>
    </body></html>"""
    )


def search(request):
    return HttpResponse(render_to_string("search.html"))


def remove_park(request):
    models.Park.objects.get(id="park-acadia").delete()
    return HttpResponse("Removed 'park-acadia'")


def add_park(request):
    state = models.State(name="Maine")
    state.save()

    park = models.Park(
        area=198.5,
        description="Covering most of Mount Desert Island and other coastal islands, Acadia features the tallest mountain on the Atlantic coast of the United States, granite peaks, ocean shoreline, woodlands, and lakes. There are freshwater, estuary, forest, and intertidal habitats.",
        established="1919-02-26T06:00:00Z",
        id="park-acadia",
        latitude=44.35,
        longitude=-68.21,
        title="Acadia",
        url="https://www.nps.gov/acad/index.htm",
        visitors=3303393,
        world_heritage_site=False,
    )
    park.save()
    park.states.add(state)

    return HttpResponse("Added 'park-acadia'")


def remove_m2m(request):
    park = models.Park.objects.get(id="park-great-smoky-mountains")
    park.states.remove(models.State(name="Tennessee"))

    return HttpResponse("Removed 'Tennessee' from 'park-great-smoky-mountains'")


def add_m2m(request):
    park = models.Park.objects.get(id="park-great-smoky-mountains")
    park.states.add(models.State(name="Tennessee"))

    return HttpResponse("Added 'Tennessee' to 'park-great-smoky-mountains'")


def reset(request):
    # Delete all existing objects
    models.Park.objects.all().delete()
    models.State.objects.all().delete()

    # Load new ones into the database
    with (settings.BASE_DIR / "examples/data.json").open() as f:
        documents = json.loads(f.read())

    for document in documents:
        latitude, longitude = map(
            float,
            re.match(
                r"^(-?[0-9]+(?:\.[0-9]+)?)[,\s]+(-?[0-9]+(?:\.[0-9]+)?)$",
                document.pop("location"),
            ).groups(),
        )

        document.update({"latitude": latitude, "longitude": longitude})

        states = document.pop("states")
        states = [models.State(name=state) for state in states]
        [state.save() for state in states]

        park = models.Park.objects.create(**document)
        park.save()
        for state in states:
            park.states.add(state)

    return HttpResponse("Reset successful")


def run_task(request):
    tasks.periodic_index_task()
    return HttpResponse(
        f"Task has been run, check '{tasks.APP_SEARCH_META_ENGINE_NAME}' in App Search"
    )


@csrf_exempt
def app_search_api(request, path):
    # Forwards requests to App Search, used mostly for
    # Reference UI so you don't have to rebuild it yourself
    # for the sake of this demo.

    # Don't use this in production!!!
    resp = app_search.client.perform_request(
        method=request.method,
        path=request.path,
        body=request.body,
    )
    return JsonResponse(resp.body, status=resp.status)
