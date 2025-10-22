from django.urls import path
from . import views

urlpatterns = [
    path("strings", views.string_list_create, name="string_list_create"),
    path("strings/<str:string_value>", views.string_detail, name="string_detail"),
    path("strings/filter-by-natural-language", views.filter_by_natural_language, name="filter_by_natural_language"),
]
