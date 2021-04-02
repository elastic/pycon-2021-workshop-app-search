from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("reset", views.reset, name="reset"),
    path("add-park", views.add_park, name="add_document"),
    path("remove-park", views.remove_park, name="remove_document"),
    path("add-m2m", views.add_m2m, name="add_m2m"),
    path("remove-m2m", views.remove_m2m, name="remove_m2m"),
    path("run-task", views.run_task, name="run_task"),
    path("api/as/<path:path>", views.app_search_api, name="app_search_api"),
    path("<slug:park_id>", views.park, name="park"),
]
