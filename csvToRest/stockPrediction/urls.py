from django.urls import path
from .views import getPrediction

urlpatterns = [
    path('prediction/<slug:symbol>/', getPrediction.as_view()),
    
]