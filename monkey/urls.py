from django.urls import path
from .views import StringListCreateView, StringDetailView

urlpatterns = [
    path("strings", StringListCreateView.as_view(), name="string_list_create"),
    path("strings/<str:string_value>", StringDetailView.as_view(), name="string_detail"),
]

