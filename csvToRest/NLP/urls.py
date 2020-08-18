from django.urls import path
from .views import getsentiments

urlpatterns = [
    path('<slug:symbol>', getsentiments.as_view()),
]