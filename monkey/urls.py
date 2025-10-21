from django.urls import path
from . views import StringListView, StringDetailView, NaturalLanguageFilterView


# ========================
# URLS
# ========================
urlpatterns = [
    path('strings', StringListView.as_view()),
    path('strings/<str:string_value>', StringDetailView.as_view()),
    path('strings/filter-by-natural-language', NaturalLanguageFilterView.as_view()),
]