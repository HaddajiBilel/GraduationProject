from django.urls import path
from .views import getPrediction, trainModel

urlpatterns = [
    path('prediction/<slug:symbol>/', getPrediction.as_view()),
    path('train/<slug:symbol>/', trainModel.as_view()),
]